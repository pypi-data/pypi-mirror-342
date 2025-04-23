FROM python:3.12 AS base

WORKDIR /luminarycloud

COPY ./luminarycloud-*.whl dist/
RUN pip install --upgrade pip
RUN pip install dist/luminarycloud-*.whl
RUN pip install jupyterlab pandas matplotlib

ENTRYPOINT ["jupyter", "lab"]
