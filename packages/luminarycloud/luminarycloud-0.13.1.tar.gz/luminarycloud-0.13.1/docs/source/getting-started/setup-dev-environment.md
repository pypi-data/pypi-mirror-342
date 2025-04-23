# Set Up Development Environment

This tutorial explains how to install the SDK in a new
virtual environment, or an existing Python environment.

## Create a Python virtualenv (Recommended)

:::{important}
It's highly recommended to use a virtualenv to minimize installation issues
and avoid impacting your existing Python environment. However, you can skip
this step if you'd like to use an existing Python environment.
:::

Ensure that you have Python (3.12+) installed, then run the following command to
create a virtualenv:

::::{tab-set}
:::{tab-item} macOS/Linux
:sync: macos-linux
```sh
python -m venv my-venv
```
:::
:::{tab-item} Windows
:sync: windows
```powershell
py -m venv my-venv
```
:::
::::

After creating your virtualenv, activate it by running:
::::{tab-set}
:::{tab-item} macOS/Linux
:sync: macos-linux
```sh
source my-venv/bin/activate
```
:::
:::{tab-item} Windows
:sync: windows
```powershell
.\my-venv\Scripts\activate
```
:::
::::

Once you've completed the example program, you can exit the virtualenv with `deactivate`.

## Install the Python SDK

:::{note}
If you skipped creating a virtualenv, you may need to
substitute `python3` instead `python` for the commands in this guide.
:::

Install the Luminary Cloud Python SDK with pip:
::::{tab-set}
:::{tab-item} macOS/Linux
:sync: macos-linux
```sh
python -m pip install luminarycloud
```
:::
:::{tab-item} Windows
:sync: windows
```powershell
py -m pip install luminarycloud
```
:::
::::

## Using the virtualenv

Now you have a ready-to-use Python virtualenv with the Luminary Cloud
SDK installed. A common workflow could be something like:

::::{tab-set}
:::{tab-item} macOS/Linux
:sync: macos-linux
```sh
# activate the virtualenv
source my-venv/bin/activate

# run a python script that uses the SDK
python my_first_simulation.py

# deactivate the virtualenv when you're done
deactivate
```
:::
:::{tab-item} Windows
:sync: windows
```powershell
# activate the virtualenv
my-venv\Scripts\activate

# run a python script that uses the SDK
py .\my_first_simulation.py

# deactivate the virtualenv when you're done
deactivate
```
:::
::::


## Next Steps

For a tutorial on writing your first Python script to run a simulation, click
the **Next** link below.
