"""
Copyright 2025 Inmanta

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Contact: code@inmanta.com
"""

import collections.abc
import contextlib
import json
import logging
import os
import time

import paramiko
import paramiko.client
import pingparsing
import pydantic
import pygnmi  # type: ignore
import pygnmi.client  # type: ignore
import pytest
from pytest_inmanta.plugin import Project

from inmanta.resources import Resource

LOGGER = logging.getLogger()


class Ping(pydantic.BaseModel):
    destination: str
    packet_duplicate_count: int
    packet_duplicate_rate: float | None
    packet_loss_count: int
    packet_loss_rate: float
    packet_receive: int
    packet_transmit: int
    rtt_avg: float | None
    rtt_max: float | None
    rtt_mdev: float | None
    rtt_min: float | None


class Route(pydantic.BaseModel):
    type: str
    dst: str
    dev: str
    protocol: str | int
    scope: str | int
    flags: list[str]
    gateway: str | None = None
    pref_src: str | None = None
    metric: int | None = None


class BgpNotConvergedException(Exception):
    pass


class SrlinuxDevice:
    def __init__(
        self,
        mgmt_ip: str,
        mgmt_port: int = 57400,
        name: str | None = None,
        skip_verify: bool = True,
        insecure: bool = False,
        certificate_chain: str | None = None,
        private_key: str | None = None,
        root_certificates: str | None = None,
        gnmi_username_env_var: str = "GNMI_DEVICE_USER",
        gnmi_password_env_var: str = "GNMI_DEVICE_PASSWORD",
        linux_username_env_var: str = "LINUX_DEVICE_USER",
        linux_password_env_var: str = "LINUX_DEVICE_PASSWORD",
        linux_ssh_host: str | None = None,
        linux_ssh_port: int = 22,
        *,
        project: Project,
        monkeypatch: pytest.MonkeyPatch,
    ):
        """
        Construct an object representing an srlinux device, where we can
        push and cleanup configs.  The interaction with the device is done using the nokia_srlinux
        adapter, and works in two stages:
        1. Use the compiler to convert a model into a config
        2. Push the config to the device

        :param mgmt_ip: Management ip of the device
        :param mgmt_port: Management port of the device
        :param name: A friendly name to identify the device, defaults to the mgmt_ip
        :param skip_verify: Disable SSL certificate validation on the encrypted gRPC channel.
        :param insecure: Use an insecure channel to the device.
        :param certificate_chain: The path to the PEM-encoded certificate chain.
        :param private_key: The path to the PEM-encoded private key.
        :param root_certificates: The path to the PEM-encoded root certificates.
        :param gnmi_username_env_var: environment variable for username of the user that can use the gnmi api
        :param gnmi_password_env_var: environment variable for password of the user that can use the gnmi api
        :param linux_username_env_var: environment variable for username of the user that can ssh in linux context
        :param linux_password_env_var: environment variable for password of the user that can ssh in linux context
        :param linux_ssh_host: The hostname that should be used to ssh on the device, defaults to the mgmt_ip
        :param linux_ssh_port: The port number that should be used to ssh on the device
        """
        # Get all options to setup a connection with the gnmi api
        self.mgmt_ip = mgmt_ip
        self.mgmt_port = mgmt_port
        self.name = name if name is not None else self.mgmt_ip
        self.skip_verify = skip_verify
        self.insecure = insecure
        self.certificate_chain = certificate_chain
        self.private_key = private_key
        self.root_certificates = root_certificates
        self.gnmi_username_env_var = gnmi_username_env_var
        self.gnmi_password_env_var = gnmi_password_env_var

        # Get all options to open a shell on the underlying linux host
        self.linux_username = os.environ[linux_username_env_var]
        self.linux_password = os.environ[linux_password_env_var]
        self.linux_ssh_host = (
            linux_ssh_host if linux_ssh_host is not None else self.mgmt_ip
        )
        self.linux_ssh_port = linux_ssh_port

        # Save testing tools
        self.project = project
        self.monkeypatch = monkeypatch

        # List of all the models that should be deployed with purged=True when
        # self.cleanup() is called
        self.deployed_models: list[
            tuple[str, collections.abc.Mapping[str, object] | None]
        ] = []

    @property
    def device_properties(self) -> collections.abc.Mapping[str, object]:
        return {
            "gnmi": {
                "mgmt_ip": self.mgmt_ip,
                "port": self.mgmt_port,
                "name": self.name,
                "skip_verify": self.skip_verify,
                "insecure": self.insecure,
                "certificate_chain": self.certificate_chain,
                "private_key": self.private_key,
                "root_certificates": self.root_certificates,
            },
            "credentials": {
                "username_env_var": self.gnmi_username_env_var,
                "password_env_var": self.gnmi_password_env_var,
            },
        }

    def deploy(
        self,
        model: str,
        *,
        purged: bool = False,
        purge_on_cleanup: bool = False,
        input: collections.abc.Mapping[str, object] | None = None,
    ) -> Resource:
        """
        Compile and deploy the given model, if the model requires some input parameters, via
        environment variables, they can be added to the env_vars parameter.

        :param model: The model to compile and deploy, only a single resource should
            be emitted by the model.
        :param purged: Set the value of the environment variable PURGED that is available
            to the model, allowing to easily reuse a model for cleaning up.
        :param purge_on_cleanup: Whether the model should be saved and compiled with PURGED
            env var set to true when calling the cleanup method.
        :param env_vars: A mapping of environment variables to make available to the model.
        """
        model_input = {
            "device": self.device_properties,
            "purged": purged,
            **(input or {}),
        }

        # Compile the model, pass the input within a single environment variable
        with self.monkeypatch.context() as ctx:
            ctx.setenv("INPUT", json.dumps(model_input))

            self.project.compile(model, no_dedent=False)

        # Find the single gnmi resource exported by the model, and deploy it
        resource = self.project.deploy_resource("yang::GnmiResource")

        if purge_on_cleanup:
            # If the model should be reused for cleanup, safe it here
            self.deployed_models.append((model, input))

        return resource

    def cleanup(self) -> None:
        """
        Cleanup the device by deploying all the saved models, and set purged=True
        """
        for model, input in reversed(self.deployed_models):
            self.deploy(
                model,
                purged=True,
                purge_on_cleanup=False,
                input=input,
            )

        # All models have been cleanup up, reset the list
        self.deployed_models = []

    @contextlib.contextmanager
    def ssh_connection(self) -> collections.abc.Iterator[paramiko.SSHClient]:
        """
        Setup an ssh connection with the remote linux host.
        """
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(
                self.linux_ssh_host,
                self.linux_ssh_port,
                self.linux_username,
                self.linux_password,
            )
            yield ssh
        finally:
            ssh.close()

    def exec(self, command: str) -> tuple[str, str]:
        """
        Execute a command in a linux shell and return its output, in two
        strings: stdout and stderr
        """
        with self.ssh_connection() as ssh:
            _, stdout, stderr = ssh.exec_command(command)
            return stdout.read().decode(), stderr.read().decode()

    def client(self) -> pygnmi.client.gNMIclient:
        username = os.getenv(self.gnmi_username_env_var)
        password = os.getenv(self.gnmi_password_env_var)
        return pygnmi.client.gNMIclient(
            target=(self.mgmt_ip, self.mgmt_port),
            username=username,
            password=password,
            skip_verify=self.skip_verify,
        )

    def get(self, path: str) -> dict:
        with self.client() as gc:
            response = gc.get(
                path=[path],
                encoding="json_ietf",
                datatype="state",
            )

        return response["notification"]

    def ping(
        self,
        destination: str,
        network_instance: str | None = None,
        interface: str | None = None,
        count: int = 4,
        interval: float = 0.5,
        timeout: int = 3,
        packetsize: int | None = None,
    ) -> Ping:
        """
        Send a ping towards the given destination.

        :param destination: The target to send the icmp packet to
        :param network_instance: The network instance in which the ping command
            should be executed
        :param interface: The name of the interface that should be used to ping the target
        :param count: The amount of icmp packets that should be sent
        :param interval: The amount of seconds to wait in between each sent packet
        :param timeout: The maximum time in seconds we should wait for a response
        :param packetsize: The size of the icmp packet payload, when provided, also
            activate mtu discovery
        """
        command = [
            "ping",
            f"-c{count}",
            f"-i{interval}",
            f"-W{timeout}",
        ]

        if interface is not None:
            command += ["-I", interface]

        if packetsize is not None:
            command += ["-s", str(packetsize), "-M", "do"]

        if network_instance is not None:
            # Execute the ping command within a network namespace
            command = [
                "ip",
                "netns",
                "exec",
                f"srbase-{network_instance}",
                *command,
            ]

        command += [destination]

        stdout, stderr = self.exec(" ".join(command))
        if not stdout:
            raise RuntimeError(f"Failed to ping: {stderr}")

        stats = pingparsing.PingParsing().parse(stdout).as_dict()
        return pydantic.TypeAdapter(Ping).validate_python(stats)

    def get_routes(self, network_instance: str | None = None) -> dict[str, Route]:
        """
        Get all the routes which exist on the remote host, in a network instance.
        """
        command = ["ip", "-j", "-details", "route"]

        if network_instance is not None:
            command = [
                "ip",
                "netns",
                "exec",
                f"srbase-{network_instance}",
                *command,
            ]

        stdout, stderr = self.exec(" ".join(command))
        if not stdout:
            raise RuntimeError(f"Failed to get routes: {stderr}")

        route_type = pydantic.TypeAdapter(Route)
        return {
            route.dst: route
            for raw_route in json.loads(stdout)
            if (route := route_type.validate_python(raw_route))
        }

    def get_bgp_sessions(
        self,
        network_instance: str,
    ) -> list[dict]:
        data = self.get(
            f"/network-instance[name={network_instance}]/protocols/bgp/neighbor[peer-address=*]"
        )
        bgp_sessions = []
        for d in data:
            for update in d["update"]:
                for neighbor in update["val"]["neighbor"]:
                    bgp_sessions.append(neighbor)
        return bgp_sessions

    def wait_for_bgp_state(
        self,
        network_instance: str,
        peer_addresses: list[str] | None = None,
        state: str = "established",
        timeout=300,
        retry_interval=5,
    ) -> None:
        """
        Wait for bgp session-state to be established for the specified peer addresses
        If `peer_addresses` is set to None, wait for all of them

        :param network_instance: the name of the network instance to check
        :param peer_addresses: peer addresses to check
        :param timeout: total timeout in second to wait until throwing an error
        :param retry_interval: time pause between each query in second
        """

        def is_done() -> bool:
            bgp_sessions = self.get_bgp_sessions(network_instance)
            for session in bgp_sessions:
                if peer_addresses is None or session["peer-address"] in peer_addresses:
                    if session["session-state"] != state:
                        return False
            return True

        n_tries = timeout // retry_interval

        for _ in range(n_tries):

            if is_done():
                return

            time.sleep(retry_interval)

        raise BgpNotConvergedException(
            f"The Bgp sessions for the network instance `{network_instance}` didn't converged"
        )

    def get_bfd_sessions(self) -> list[dict]:
        data = self.get("/bfd")
        bfd_sessions = []
        for d in data:
            for update in d["update"]:
                for subinterface in update["val"]["subinterface"]:
                    bfd_sessions.append(subinterface)
        return bfd_sessions
