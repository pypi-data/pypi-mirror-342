# syntax = docker/dockerfile:1.0-experimental

FROM ghcr.io/neuronsphere/hmd-img-jupyter-multiarch:stable

RUN --mount=type=secret,id=pipconfig,uid=1000,dst=/home/jovyan/.pip/pip.conf \
    pip install papermill==2.4.0 nbformat

COPY meta-data/ /meta-data
COPY src/ /src
COPY src/docker/requirements.txt ${FUNCTION_DIR}
RUN --mount=type=secret,id=pipconfig,uid=1000,dst=/home/jovyan/.pip/pip.conf \
    pip install -r requirements.txt

WORKDIR /app

COPY src/docker/entrypoint.py entrypoint.py
COPY src/notebooks/ /app/notebooks/


ENTRYPOINT [ "python", "entrypoint.py" ]