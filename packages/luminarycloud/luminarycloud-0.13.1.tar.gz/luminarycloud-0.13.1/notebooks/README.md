# Luminary Python SDK Notebooks

- [Quickstart (notebook in web browser)](#quickstart-notebook-in-web-browser)
- [Advanced (notebook in VSCode)](#advanced-notebook-in-vscode)
  - [Workspace Setup](#workspace-setup)
  - [Install the Luminary Cloud Python SDK](#install-the-luminary-cloud-python-sdk)
- [Configuration](#configuration)

## Quickstart (notebook in web browser)

Follow this Quickstart section if you just want to start running the example
notebooks and using the SDK as easily as possible.

**Pre-requisite:** Install Docker <https://www.docker.com>

Run the following command in a terminal:

```sh
> cd core/python/sdk
# always use the --build flag to ensure that the latest sdk is built and used
> docker compose up --build notebook
...
sdk-notebook-1  |     To access the server, open this file in a browser:
sdk-notebook-1  |         file:///root/.local/share/jupyter/runtime/jpserver-1-open.html
sdk-notebook-1  |     Or copy and paste one of these URLs:
sdk-notebook-1  |         http://localhost:8888/lab?token=...
sdk-notebook-1  |         http://127.0.0.1:8888/lab?token=...
```

This may take a while the first time, but you should eventually see output
similar to the above. Open the URL in your browser to access the notebook
interface.

![notebook screencast](https://user-images.githubusercontent.com/6025130/228690368-501423ef-6a12-4a7c-97fb-2ef319b3b971.gif)

## Advanced (notebook in VSCode)

This process is more involved, but allows you to edit and run notebooks directly
in VSCode.

### Workspace Setup

This document assumes you're running on Linux or macOS.

**You only need to run these steps once**

1. Install VSCode and create the workspace
   1. Install from: <https://code.visualstudio.com>

   2. Optional: Create a new workspace folder and copy this `e2e-workflow-example.ipynb` file into it.

   3. Once your workspace in VSCode and open `e2e-workflow-example.ipynb` and
   install the extensions that VSCode recommends.

2. Create a new virtualenv and configure VSCode
   1. In VSCode open up a terminal (CTRL-\` or CMD+SHIFT+P and search for
   "Terminal: Create New Terminal")

   2. Run the following commands in the terminal:

      ```sh
      # create a new virtualenv called "sdk-venv" in our project directory
      python3 -m venv ./sdk-venv
      ```

   3. CMD+SHIFT+P and search for "Python: Select Interpreter", select it

   4. If you see a "Recommended" option with `./sdk-venv/bin/python`, select it.
   Otherwise, choose "Enter interpreter path..." and type the same path.

   5. Click the trash icon in the terminal pane to delete it, and create a new
   terminal using the same method as before.

   6. You should now see `(sdk-venv)` at the beginning of your terminal prompt.
   This indicates that we're operating in our new virtual environment.

   7. Run the following commands to install some other python dependencies

      ```sh
      # python notebook related dependencies and libraries for post-processing examples
      pip install ipython ipykernel pandas matplotlib
      ```

### Install the Luminary Cloud Python SDK

> NOTE: ask the API team for the latest SDK (`*.whl` file) or build it yourself (see [$CORE/python/sdk/README.md](../README.md))

Run this in your terminal in VSCode. This only needs to be run once, or when there is a new SDK version.

```sh
# note: you may need to update the filename for newer version
pip install --force-reinstall ./luminarycloud-0.0.1-py3-none-any.whl
```

You can confirm that the SDK was installed by running:

```sh
pip list | grep luminarycloud
```

The output should look like this:

```
luminarycloud            0.0.1
```

## Configuration

Auth0 configuration and default target domain (i.e. the API env to make calls
to, e.g. main, test0, etc) are configured in the first codeblock in of
e2e-workflow-example.ipynb.

More details [here](../README.md#configuration).

## Jupytext notebook conversion

The Piper tutorial notebook is stored in Jupytext Python format (py) and converted to Jupyter notebook format (ipynb), which is easier for developers to edit and work with.

You will need to install Jupytext:

```sh
pip install jupytext
```

More about Jupytext:  [https://jupytext.readthedocs.io/en/latest/index.html](https://jupytext.readthedocs.io/en/latest/index.html)

You can open a Jupytext notebook in JupyterLab by right-clicking on the file and selecting "Open with Notebook".

After you edit the `piper-tutorial.py` example, update the notebook file by running:

```sh
jupytext --to ipynb --update --output generated/piper-tutorial.ipynb piper-tutorial.py
```

You can convert a Jupyter notebook to a Jupytext notebook (if needed) by running:

```sh
jupytext --to py some-notebook.ipynb
```
