# Quickstart with a Python Notebook

This tutorial explains how to use a containerized Python environment with the Luminary
Cloud SDK pre-installed to access a pre-written sample notebook in your web
browser.

This is the fastest way to starting writing and executing code to run simulations.
It's the best option if you're looking to quickly get a feel for the Luminary
Cloud Python SDK.

```{eval-rst}
.. important::

  If you have never logged in to the `Luminary web app
  <https://app.luminarycloud.com>`_, please to log in and accept the terms and
  conditions before proceeding.
```

## Download Files

Download and unzip the
[luminarycloud-quickstart files](https://storage.googleapis.com/luminarycloud-learning/sample-projects/lc-sdk/api-files/luminarycloud-quickstart.zip). Throughout this guide, the unzipped directory will be referred to as
`luminarycloud-quickstart`.

:::{caution}
  To avoid potential problems, make sure there are no
  spaces in the file path.

  For example, **do not** put the file in a location like this:

  ``C:/My Projects/luminarycloud-quickstart``

  Instead use:

  ``C:/MyProjects/luminarycloud-quickstart`` or ``C:/My_Projects/luminarycloud-quickstart``
:::


## Install Podman

We'll use Podman to build and run a container on your computer. It is an open source
alternative to Docker and is covered by the [Apache License
2.0](https://www.apache.org/licenses/LICENSE-2.0). The container will have a pre-installed Python environment with everything needed to
run SDK examples in an interactive notebook.

Follow the installation instructions on the
[Podman website](https://podman.io/docs/installation) for your operating system.

:::{tip}
  **Non-linux users** should run the following commands after the
  initial Podman installation or after restarting their machine.

  ```
  podman machine init
  podman machine start
  ```
:::

:::{tip}
  **Linux users.** If you are trying to run podman as a non-root user, you may need to allocate
  ID ranges in `/etc/subuid` and `/etc/subgid` to allow podman to create user
  namespaces in rootless mode. Run the following commands, replacing `USERNAME`
  with your actual username:
  ```
  sudo usermod --add-subuids 10000-75535 USERNAME
  sudo usermod --add-subgids 10000-75535 USERNAME
  podman system migrate
  ```
:::

## Build the Image

1. Change directories to where you downloaded the `luminarycloud-quickstart` zip file:
```
cd <path to downloaded luminarycloud-quickstart directory>
```

2. Build the image:
```
podman build -t sdk-notebook .
```

3. Check that the `sdk-notebook` image was built:
```
podman images
```

The output should look like this:
```
REPOSITORY                TAG         IMAGE ID      CREATED        SIZE
localhost/sdk-notebook    latest      e3636dfd5648  7 seconds ago  1.39 GB
```

## Run the Notebook Server

1. Start the container using the `sdk-notebook` image. This command will keep an active process in your terminal while the server is
running:
```
podman run -v ./notebooks:/notebooks -p 8888:8888 -p 10001:10001 sdk-notebook --ip=0.0.0.0 --allow-root --no-browser --port=8888 /notebooks
```

:::{tip}
  If you get an error like ``Error: statfs ... no such file or directory``,
  restart the Podman virtual machine by running the following:

  ```
  podman machine stop && podman machine start
  ```

  Then retry the ``podman run ...`` command above.
:::

 2. To access the notebook, look for a URL like this in the command output and open it in your browser (Google Chrome recommended):

`http://127.0.0.1:8888/lab?token=...`

```{image} /assets/notebook_interface.png
:width: 600px
```

3. In the left-hand sidebar, find a sample notebook called `quickstart-notebook.ipynb`. Double-click to open it.

4. Continue the quickstart tutorial by following the instructions in the notebook.

To stop the notebook server, save your files and return to the terminal where
the notebook server is running. Use `CTRL-C` to interrupt the process and stop
the server.

## Using the Notebook Interface

This quickstart tutorial utilizes Podman to provide a simple way to quickly run
a Python notebook with the Luminary Cloud SDK pre-installed. This method does
not affect your existing Python installation(s) and avoids potential dependency
conflicts.

Since the notebook runs within a container, it does not have direct access to
the "host" filesystem. Follow the steps in the sections below to move files into
and out of the container.

### Manage Files in the File Browser (Recommended)

The `notebooks` directory in the `luminarycloud-quickstart` folder is
mounted at the root of the container's filesystem (i.e. `/notebooks`).
You can use your operating system's standard file browser (File Explorer in
Windows, Finder in macOS, etc.) to manage files. Any files added to the
`notebooks` directory or its subdirectories will be available in the notebook.

:::{important}
  You may need to refresh the page in your browser to see the changes reflected.
:::

### Manage Files in the Notebook Interface

Any file you see in the left-hand sidebar of the notebook interface can be
downloaded to your host filesystem by right-clicking on the file and selecting
`Download`.

```{image} /assets/notebook_download_file.png
:width: 600px
```

To upload a file from the host filesystem, click the `Upload` button at the top of
the left-hand sidebar.

```{image} /assets/notebook_upload_file.png
:width: 600
```

:::{tip}
  You can also drag and drop files into the sidebar to upload them.
:::
