FROM python:3.7

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

RUN pip3 install -r requirements.txt

CMD cd app && echo "start" && python3.7 main.py