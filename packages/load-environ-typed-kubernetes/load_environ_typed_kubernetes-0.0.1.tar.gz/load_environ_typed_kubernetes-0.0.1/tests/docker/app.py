from typing import Dict

import datetime
import sys
import time

from load_environ_typed import load
from load_environ_typed_kubernetes.loaders import KubernetesLoader

from dataclasses import dataclass


@dataclass
class MyEnviron:
    my_config_map: Dict[str, str]
    my_config_map_binary: Dict[str, bytes]
    my_secret: Dict[str, str]
    my_secret_binary: Dict[str, bytes]


def main() -> None:
    print(datetime.datetime.now().isoformat(), "Loading environment...")

    kubernetes = KubernetesLoader(in_cluster=True)

    environ = load(MyEnviron, loaders={
        'my_config_map': kubernetes.load_config_map,
        'my_config_map_binary': kubernetes.load_config_map_binary,
        'my_secret': kubernetes.load_secret,
        'my_secret_binary': kubernetes.load_secret_binary,
    })

    print(datetime.datetime.now().isoformat(), environ)

    sys.stdout.flush()

    time.sleep(9999)


if __name__ == '__main__':
    main()
