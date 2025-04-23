# Luminary Cloud Python SDK Development Guide

- [API Reference](#api-reference)
- [Project structure](#project-structure)
- [Setting up your development environment](#setting-up-your-development-environment)
- [Generating Python proto files](#generating-python-proto-files)
- [Adding a new API service](#adding-a-new-api-service)
- [Documentation](#documentation)
- [Writing docstrings](#writing-docstrings)
  - [Deprecation warnings](#deprecation-warnings)
  - [Experimental features](#experimental-features)
- [Proto wrappers](#proto-wrappers)
- [Wrapping proto enums](#wrapping-proto-enums)
- [Logging](#logging)

## API Reference

You can find the internal API reference for the SDK at https://docs.eng.luminarycloud.com/python-sdk/reference/index.html.

## Project structure

An explanation of some of the more important files and folders in the project:

- `luminarycloud/`: Package source for the SDK.
- `docs/`
  - `source/`: Source for the documentation website.
    - `conf.py`: Configuration for auto-generating the API reference.
    - `releases/`: Release notes.

Related to testing and example code:

- `tests`: Pytest unit tests. See [Unit tests](#unit-tests).
- `notebooks`: Jupyter notebooks for the SDK. See [Notebooks](#notebooks).
- `examples`: Example scripts for the SDK. See [Example scripts](#example-scripts).
- `testdata/`: Files used by notebooks and example scripts. This folder is mounted to `/sdk/testdata` when running the SDK through docker compose.
- `docker-compose.yml`: Essentially, the configuration for the various docker compose stuff you can run.

Related to packaging and publishing:

- `requirements.txt`: Core dependencies for the SDK.
- `requirements-dev.txt`: Packages needed for development, but not for running the SDK itself.
- `pyproject.toml`: Configuration for packaging and publishing the SDK.
- `DESCRIPTION.md`: Package description as it shows up on PyPI.

## Setting up your development environment

If you haven't already, follow the instructions in the [README](README.md) to learn how to install and run the SDK. Since you're a developer, you'll probably want to install everything in `requirements-dev.txt` as well.

If you're using an IDE (like VSCode), remember to point your Python language
server to the Python interpreter that has the SDK installed so that you can
get syntax highlighting, IntelliSense, etc.

You can use the following tools to help you develop and test features for the
SDK. It's encouraged to generate these files as you develop your feature so
that they may also serve as documentation for future developers.

The instructions below assume you're running the SDK through docker compose. If
you're using a different method to run the SDK (such as using a virtualenv),
you'll have to adjust the commands accordingly.

### Example scripts

There is an `examples/` directory containing some informal examples of different
SDK features. These are not for public consumption, they are not included in any
documentation, and they are not exercised in CI. So there's no guarantee that
they remain up to date. But it's often useful to write some example scripts that
you can run and iterate on during development, and including those scripts in
your PRs help show off the intended functionality of your work.

Example scripts can be run like so:

```sh
docker compose run --build sdk python /sdk/examples/your_script.py
```

You can easily point a script to a preview environment by adding the following
code to the top of it:

```py3
import luminarycloud as lc
from sdk_util import get_client_for_env

lc.set_default_client(get_client_for_env("my-preview-env-name"))
```

Note that the client points to `main` by default when running through docker
compose, so there's no need to explicitly point there if there are no server
side changes. If you need to point to production, then replace
`my-preview-env-name` with `prod`.

### Unit tests

As you develop your feature, you might want to write unit tests in the `tests/` directory. You can run the tests using the following command.

```sh
docker compose run --build sdk pytest
```

You can also run a specific test or tests by filtering test names by a keyword. You can do this by using the `-k` flag. For example:

```sh
docker compose run --build sdk pytest -k "your_test_name"
```

Note that unit tests are unit tests, not integration tests. They are not meant
to test the SDK against a live environment. You'll have to mock out any
responses you want to test.

### Notebooks

You can spin up a Jupyter notebook server using the following command.

```sh
docker compose up --build notebook
```

Any notebooks you create will be saved in the `notebooks/` directory.

Similarly to the example scripts, you can easily point the notebook to main or a preview environment by adding the following code to the first cell of your notebook.

```py3
import luminarycloud as lc
from sdk_util import get_client_for_env

lc.set_default_client(get_client_for_env("my-preview-env-name"))
```

Again, note that the client points to main by default when running it through
docker compose, so there's no need to do this if there are no server side
changes. If you need to point to production, then replace `my-preview-env-name`
with `prod`.

## Generating Python proto files

As you develop API features, you may tweak the proto files in `$CORE/proto`,
and if you do, you'll need to (re)generate the corresponding Python files.

Run the following command to generate the *.py and *.pyi files from the proto files in `$CORE/proto`. Remember to `deactivate` any active virtualenvs before running this command (or you may end up with incorrect behavior).

```sh
$CORE/./bazel/gazelle.py
```

## Adding a new API service

If you add a new service to the API and you want to expose it via the SDK, you'll need to add the
auto-generated proto stub to [luminarycloud/_client/client.py](./luminarycloud/_client/client.py).
Check that file for examples of how it's done with existing services. Basically, the generated stub
is imported and added to the set of base classes for the `Client` class, and then it's initialized
in the `__register_rpcs()` method

## Documentation

The [SDK documentation](https://docs.eng.luminarycloud.com/python-sdk) is a combination of handwritten documentation and an
auto-generated API reference.

The handwritten documentation is in the `docs/source/` directory. As new
features are added and existing features are updated, this part of the
documentation should be updated by hand to reflect the changes.

Also, with each release, a new page should be added to `docs/source/releases/`
to document the changes in the release. It may be helpful to have placeholder
notes for the next release and keep it updated with every PR.

On the other hand, the API reference is generated from the SDK source code,
but it also relies on good docstrings. The section below explains more about
that.

## Writing docstrings

The docstrings in the SDK are both used to generate the API reference and used by the Python language server to provide IntelliSense. It's one of the main ways we communicate to users how to use the various SDK features, so it's important to write good docstrings.

The docstrings are written in numpydoc style, which you can read more about
[here](https://numpydoc.readthedocs.io/en/latest/format.html).

Note that documentation will only be generated for the public API, which only
includes the classes and functions that are imported in the `__init__.py` files in the root directory and any explicitly imported subpackages. You should still
document any private functions and classes.

### Deprecation warnings

Remember to include a deprecation warning in the docstring if a function or class is deprecated, in accordance to [this Sphinx directive](https://numpydoc.readthedocs.io/en/latest/format.html#deprecation-warning).

```
.. deprecated:: 1.6.0
          `ndobj_old` will be removed in NumPy 2.0.0, it is replaced by
          `ndobj_new` because the latter works also with array subclasses.
```

You should also use the `deprecated` decorator in [`_helpers/warnings/deprecated.py`](./luminarycloud/_helpers/warnings/deprecated.py) to mark the function or class as deprecated.

### Experimental features

If a feature is temporary and/or not expected to be stable in the near term, you should include the following warning in its docstring:

```
.. warning:: This feature is experimental and may change or be removed without notice.
```

You should also use the `experimental` decorator in [`_helpers/warnings/experimental.py`](./luminarycloud/_helpers/warnings/experimental.py) to mark the class or function as experimental.

## Proto wrappers

We try to avoid exposing users to protobuf messages directly. Instead, we wrap them.

The [`_wrapper.py`](./luminarycloud/_wrapper.py) module provides a decorator for classes that wrap a protobuf message. This is useful for representing API resources in a more friendly way and attaching instance methods for performing actions on the resource.

When introducing a new API resource, it is recommended to use this decorator to create a class to represent it. See the [API Development Guide](https://docs.eng.luminarycloud.com/api/DEVELOPMENT.html#terminology) for more information on what it means to define an API resource.

See the docstring for `ProtoWrapper` in [`_wrapper.py`](./luminarycloud/_wrapper.py) for more information on what it does exactly.

The main things you need to know:
- Declaring an attribute in the wrapper class that matches the name of the protobuf message field will automatically generate accessors for that field.
- Omitting the attribute will prevent the accessors from being generated, so this is a good way to hide fields (if you really need to do that).
- If you need to write a custom accessor, you can do so by writing your own accessor method instead of an attribute declaration. For example, the [`Project`](./luminarycloud/project.py) class has an accessor to convert the `create_time` field from a protobuf timestamp to a Python `datetime` object when it is being read.

## Wrapping proto enums

We also try to avoid exposing users to protobuf enums directly. Part of the
reason for this is that protobuf enum values don't really have a type annotation
other than protobuf's `ValueType` which just means "an enum value" and isn't
very helpful.

Instead, we wrap them in a class that inherits from `IntEnum`. This allows us
to provide a more friendly interface for the user while still being able to
access the underlying raw enum value.

We put all of these wrapper classes in the `luminarycloud/enum/` directory.
Enums related to solver parameters are in the `luminarycloud/enum/params/`
directory.

## Logging

The SDK uses the built-in `logging` module to log messages, through a logger
named "luminarycloud".

To log a message, add the following code to the top of your file:

```py3
import logging

logger = logging.getLogger("luminarycloud")
```

Then, use `logging.info()`, `logging.debug()`, etc. to log messages at the
appropriate level.

Most logs should be at the `DEBUG` and `INFO` levels.

- `DEBUG`: Detailed information, written to help us debug problems. These can be as detailed as you like, and don't necessarily need to make sense to external users.
- `INFO`: High-level information about what the SDK is doing. Any I/O operations should be logged at the `INFO` level.

The default log level is `WARNING`, so most of the logs will be suppressed and
have very minimal impact on performance.

> [!NOTE]
> To minimize wastage, don't use template strings in your log
> messages. In other words, don't do this:
>
> ```py3
> logger.info(f"Message with a variable: {variable}")
> ```
>
> Instead, do this:
>
> ```py3
> logger.info("Message with a variable: %s", variable)
> ```

I recommend being conservative with logging warnings and errors. When you're
_raising_ an error, don't log it. It's possible the user is catching and
dealing with the error, so logging it will just be noisy and unhelpful.

In general, I don't think there's ever a good reason for the SDK to log an
error directly.

We do use warnings to indicate that a function is deprecated - but that's because we intentionally want to be a little bit annoying about it. For the most part, only use warnings to alert about strange or unexpected behavior or conditions that users need to be aware of.
