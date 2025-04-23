# pytest-inmanta-srlinux

[![pypi version](https://img.shields.io/pypi/v/pytest-inmanta-srlinux.svg)](https://pypi.python.org/pypi/pytest-inmanta-srlinux/)

A pytest plugin to help with testing end-to-end connectivity using inmanta and srlinux.

## Get config

This module have the ability to fetch the configuration of a srlinux router in a netconf xml format.

For example:

```bash
python -m pytest_inmanta_srlinux.get_config --host <your host> --paths interface routing_policy
```
