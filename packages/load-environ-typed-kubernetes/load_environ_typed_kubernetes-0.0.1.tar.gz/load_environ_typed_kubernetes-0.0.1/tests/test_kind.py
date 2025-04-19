from typing import Dict

import unittest

from load_environ_typed import load
from load_environ_typed_kubernetes.loaders import KubernetesLoader

from dataclasses import dataclass


@dataclass
class MyEnviron:
    my_config_map: Dict[str, str]
    my_config_map_binary: Dict[str, bytes]
    my_secret: Dict[str, str]
    my_secret_binary: Dict[str, bytes]


class TestUsingKindCluster(unittest.TestCase):
    def test_all_loaders(self) -> None:
        """
        Test the setup with the kind cluster as described in the README.md
        """

        kubernetes = KubernetesLoader(in_cluster=False)

        environ = load(MyEnviron, environ={
            'MY_CONFIG_MAP':
                'load-environ-typed-kubernetes-test.loader-test-config-map',
            'MY_CONFIG_MAP_BINARY':
                'load-environ-typed-kubernetes-test.loader-test-config-map',
            'MY_SECRET':
                'load-environ-typed-kubernetes-test.loader-test-secret',
            'MY_SECRET_BINARY':
                'load-environ-typed-kubernetes-test.loader-test-secret',
        }, loaders={
            'my_config_map': kubernetes.load_config_map,
            'my_config_map_binary': kubernetes.load_config_map_binary,
            'my_secret': kubernetes.load_secret,
            'my_secret_binary': kubernetes.load_secret_binary,
        })

        assert {
            'tree-of-a-kind': '6',
            'four-of-a-kind': '6',
            'run-of-3': '3',
            'run-of-4': '4',
            'run-of-5': '5',
            'flush-4-card': '4',
            'flush-5-card': '5',
        } == environ.my_config_map

        assert {
            'demo.bin':
                b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\t\n\x0b\x0c\r\x0e\x0f',
        } == environ.my_config_map_binary

        assert {
            'db-host': 'localhost',
            'db-password': "don't let me get me",
            'db-port': '1234'
        } == environ.my_secret

        assert {
            'db-host': b'localhost',
            'db-password': b"don't let me get me",
            'db-port': b'1234'
        } == environ.my_secret_binary
