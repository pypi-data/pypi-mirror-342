# How to run the Python SDK unit tests (locally)

```sh
# setup a minimal virtual just for the unit tests (don't reuse one since it may
# have an older SDK version, or other version of dependencies)
virtualenv /tmp/venv-pytest
source /tmp/venv-pytest/bin/activate
pip install -r python/sdk/requirements-dev.txt

cd python/sdk/tests
# to run all unit tests, just run pytest without any args
pytest

# run tests in a specific file
pytest wrappers/test_simulation.py

# deactivate the venv after using
deactivate
```