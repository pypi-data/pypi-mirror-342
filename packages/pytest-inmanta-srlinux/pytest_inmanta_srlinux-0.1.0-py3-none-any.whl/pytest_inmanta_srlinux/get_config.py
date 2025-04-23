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

import argparse

import inmanta_plugins.yang.gnmi.client  # type: ignore
from inmanta_plugins.yang.gnmi.handler import GnmiHandler  # type: ignore
from lxml import etree

from pytest_inmanta_srlinux.namespaces import namespaces

root_path_index = {
    "acl": None,
    "bfd": None,
    "interface": "name",
    "network-instance": "name",
    "routing-policy": None,
    "system": None,
    "qos": None,
    "tunnel": None,
    "tunnel-interface": "name",
}


def build_get_request(paths: list[str]) -> dict:
    """
    Build the get_request for Gnmi request
    """

    formated_paths = []

    for path in paths:
        key_path_name = path.replace("interface", "interfaces")

        key = {}
        if root_path_index[path] is not None:
            key[root_path_index[path]] = "*"

        formated_paths.append(
            {
                "origin": None,
                "elem": [
                    {
                        "name": f"srl_nokia-{key_path_name}:{path}",
                        "key": key,
                    }
                ],
            }
        )

    return {
        "prefix": None,
        "path": formated_paths,
    }


def get_configuration(
    host: str, port: int, username: str, password: str, insecure: bool, paths: list[str]
) -> etree._Element:

    router_connection = inmanta_plugins.yang.gnmi.client.gNMIclient(
        target=(host, port),
        username=username,
        password=password,
        insecure=insecure,
    )

    get_request = build_get_request(paths)

    config = GnmiHandler.get_config(
        router_connection,
        get_request,
        namespaces,
    )
    return config


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="Tool to get netconf like configuration of srlinux."
    )

    parser.add_argument("--host", type=str, help="Srlinux host", required=True)
    parser.add_argument("--port", type=int, help="Gnmi port", default=57400)
    parser.add_argument("--username", type=str, help="Username", default="admin")
    parser.add_argument("--password", type=str, help="Username", default="admin")
    parser.add_argument("--insecure", action="store_true")

    parser.add_argument(
        "--paths",
        nargs="+",
        help="List of the root path to get (by default the tool gets the full config)",
        default=list(root_path_index.keys()),
    )

    args = parser.parse_args()

    assert all(path in root_path_index for path in args.paths)

    config = get_configuration(
        host=args.host,
        port=args.port,
        username=args.username,
        password=args.password,
        insecure=args.insecure,
        paths=args.paths,
    )

    xml = etree.tostring(
        config,
        pretty_print=True,
        encoding="unicode",
    )

    print(xml)
