# syntax = docker/dockerfile:1.0-experimental

FROM ghcr.io/neuronsphere/hmd-ms-librarian:stable

COPY requirements.txt ${FUNCTION_DIR}


RUN --mount=type=secret,id=pipconfig,dst=/etc/pip.conf \
    pip install -r requirements.txt

