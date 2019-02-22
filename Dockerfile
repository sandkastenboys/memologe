FROM balenalib/armv7hf-alpine:3.9
FROM python:3

ARG BUILD_DATE
ARG VCS_REF
ARG VERSION

LABEL maintainer="Digging Tool <espriworkemail@gmail.com>" \
  org.label-schema.build-date=$BUILD_DATE \
  org.label-schema.name="Memologe" \
  org.label-schema.description="Get notified when important things happen" \
  org.label-schema.vcs-ref=$VCS_REF \
  org.label-schema.vendor="Digging Tool / EinSpaten" \
  org.label-schema.version=$VERSION \
  org.label-schema.schema-version="1.0"


WORKDIR /app

COPY . /app

RUN python3 -m pip install -U discord.py
RUN pip3 install -r requirements.txt

RUN [ "cross-build-end" ]


ENV NAME World

CMD ["python3", "main.py"]