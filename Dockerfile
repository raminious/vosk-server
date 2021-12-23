FROM ubuntu:20.04

ARG MODEL_NAME="vosk-model-ru-0.22"
ARG MODEL_URL="https://alphacephei.com/vosk/models/${MODEL_NAME}.zip"
ARG RUNTIME_PACKAGES="python3 locales python3-pkg-resources"
ARG BUILD_PACKAGES="wget ca-certificates python3-pip unzip"

ADD *.py requirements.txt /opt/vosk-server/
ADD entrypoint.sh /opt/entrypoint.sh

RUN apt-get update -y && \
    apt-get -y install --no-install-recommends $RUNTIME_PACKAGES && \
    apt-mark manual $(apt-mark showauto) && \
    apt-get -y install --no-install-recommends $BUILD_PACKAGES && \
    cd /usr/share/locale/ && ls | grep -v 'ru\|en\|locale.alias' | xargs rm -rf && cd /opt && \
    locale-gen ru_RU.UTF-8 && \
    cd vosk-server && python3 -m pip install -r requirements.txt && rm -f requirements.txt && \
    wget -q $MODEL_URL -O model.zip && \
    unzip -q model.zip && mv $MODEL_NAME model && rm -rf model.zip && \
    apt-get remove --purge -y $BUILD_PACKAGES $(apt-mark showauto) && \
    apt-get autoremove -y && \
    apt-get -y install --no-install-recommends $RUNTIME_PACKAGES && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp /usr/share/doc/* /usr/share/info/* /usr/lib/python*/test \
    /usr/local/lib/python*/dist-packages/pip* /root/.cache/*

ENV LC_ALL ru_RU.UTF-8
ENV LANG ru_RU.UTF-8
ENV LANGUAGE ru_RU.UTF-8

EXPOSE 5000/tcp

WORKDIR /opt/vosk-server

ENTRYPOINT ["/bin/bash", "/opt/entrypoint.sh"]
