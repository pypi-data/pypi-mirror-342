# load-environ-typed-kubernetes

Extends load-environ-typed to get info right from Kubernetes API

## Getting started

```python
from typing import Dict

from load_environ_typed import load
from load_environ_typed_kubernetes.loaders import KubernetesLoader

from dataclasses import dataclass

@dataclass
class MyEnviron:
	my_config_map: Dict[str, str]
	my_secret: Dict[str, str]

kubernetes = KubernetesLoader(in_cluster=True)

environ = load(MyEnviron, loaders={
	'my_config_map': kubernetes.load_config_map,
	'my_secret': kubernetes.load_secret,
})
```

## Contributing

Make sure you have kubectl installed via https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/.

Install a local kubernetes cluster, for example using https://kind.sigs.k8s.io/.

```sh
kind create cluster --name load-environ-typed-kubernetes

kubectl create namespace load-environ-typed-kubernetes-test

# Create the configmap and secrets
kubectl --namespace load-environ-typed-kubernetes-test apply -f tests/configmap.yaml
kubectl --namespace load-environ-typed-kubernetes-test apply -f tests/secret.yaml

# Create a role that can access the configmap and secrets
kubectl --namespace load-environ-typed-kubernetes-test apply -f tests/serviceaccount.yaml
kubectl --namespace load-environ-typed-kubernetes-test apply -f tests/role.yaml
kubectl --namespace load-environ-typed-kubernetes-test apply -f tests/rolebinding.yaml
```

Check out this repo, and then use the following steps to test it:

```sh
python3 -m venv venv
venv/bin/pip install .
venv/bin/pip install -r requirements-dev.txt
make test
```

Run a test container on Kubernetes:

```sh
docker build -f tests/docker/Dockerfile . -t load-environ-typed-kubernetes-test:0.0.1

kind load docker-image --name load-environ-typed-kubernetes load-environ-typed-kubernetes-test:0.0.1

kubectl --namespace load-environ-typed-kubernetes-test apply -f tests/pod.yaml
```

Alternatively:

```sh
make reload-pod-on-kind
```

## Deploying

First, update pyproject.toml with the new version number, and commit that.

Then:

```sh
rm -f dist/* # Clean old build files
venv/bin/python -m build
venv/bin/python -m twine upload dist/*
```
