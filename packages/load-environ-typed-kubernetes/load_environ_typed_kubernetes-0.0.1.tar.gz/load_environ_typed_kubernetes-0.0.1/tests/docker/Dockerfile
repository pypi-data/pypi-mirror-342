FROM alpine:3.21

RUN apk add python3 py3-dateutil py3-durationpy py3-google-auth py3-pip py3-certifi py3-requests py3-requests-oauthlib py3-six py3-websocket-client py3-yaml \
	&& pip3 install --break-system-packages kubernetes load_environ_typed==0.3.0

ADD load_environ_typed_kubernetes/ load_environ_typed_kubernetes/
ADD tests/docker/app.py /app.py

CMD ["python3", "app.py"]
