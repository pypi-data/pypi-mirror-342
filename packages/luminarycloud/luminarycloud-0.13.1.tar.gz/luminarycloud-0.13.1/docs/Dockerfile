# This Dockerfile is used by python/sdk/docker-compose.yml for building the sdk
# docs locally and for hosting the docs internally by
# .github/workflows/generate-docs-site.yml.
#
# The docs built by this script can then be zipped and uploaded to
# gs://luminarycloud-learning/sample-projects/lc-sdk/sdk_docs.zip Jobmaster
# fetches from this URL upon start up and serves the docs. See
# `fetchLatestSDKDocs` in `go/core/jobmaster/httpserver.go`.

FROM sphinxdoc/sphinx:5.3.0

RUN apt-get update && apt-get install -y zip

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


VOLUME ["/docs", "/luminarycloud", "/sdk"]

CMD LATEST_VERSION=$(grep -oP '(?<=version = ")[\d.]+' /sdk/pyproject.toml) && \
    echo "LATEST_VERSION: ${LATEST_VERSION}" && \
    rm -rf /docs/build && sphinx-build /docs/source /docs/build && \
    find /docs/build -type f -exec sed -i "s/LATEST_VERSION/${LATEST_VERSION}/g" {} +
