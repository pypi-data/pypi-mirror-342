FROM python:3.10 AS base

WORKDIR /sdk

RUN apt-get update && apt-get install -y gcc python3-dev

RUN pip install --upgrade pip
RUN pip install build

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY requirements-dev.txt .
RUN pip install -r requirements-dev.txt

FROM base AS sdk

COPY luminarycloud luminarycloud
COPY MANIFEST.in setup.py pyproject.toml DESCRIPTION.md ./
RUN python -m build .
RUN pip install dist/luminarycloud-*.whl
COPY sdk_util.py ./sdk_util.py

FROM base AS notebook

COPY --from=base /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
RUN pip install jupyterlab ipython ipykernel
RUN pip install pandas matplotlib

COPY --from=sdk /sdk/dist/luminarycloud-*.whl /sdk/dist/
RUN pip install dist/luminarycloud-*.whl

COPY sdk_util.py ./sdk_util.py

CMD jupyter lab --allow-root
