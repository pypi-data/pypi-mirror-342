PYTHON := venv/bin/python3
KIND := kind
KUBECTL := kubectl
KNS := load-environ-typed-kubernetes-test

test: py-typecheck py-unittest py-sast py-lint

py-typecheck:
	$(PYTHON) -m mypy --strict load_environ_typed_kubernetes tests

py-unittest:
	$(PYTHON) -m coverage run -m unittest tests/test_*.py
	$(PYTHON) -m coverage html

py-sast:
	$(PYTHON) -m pyflakes load_environ_typed_kubernetes tests

py-lint:
	$(PYTHON) -m pycodestyle --ignore=E721,W503 load_environ_typed_kubernetes tests

reload-pod-on-kind:
	docker build -f tests/docker/Dockerfile . -t $(KNS):0.0.1
	$(KIND) load docker-image --name load-environ-typed-kubernetes $(KNS):0.0.1
	-$(KUBECTL) --namespace $(KNS) delete pod loader-test-pod
	$(KUBECTL) --namespace $(KNS) apply -f tests/pod.yaml
	sleep 2
	$(KUBECTL) --namespace $(KNS) logs loader-test-pod
