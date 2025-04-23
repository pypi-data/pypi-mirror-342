<!--
This is not a standalone page in the docs site.

The contents of this file are included in other pages (e.g.
python/sdk/docs/source/releases/index.md) using Sphinx's `include` directive. See docs:
  - https://docutils.sourceforge.io/docs/ref/rst/directives.html#include
  - https://myst-parser.readthedocs.io/en/latest/faq/index.html#include-rst-files-into-a-markdown-file
 -->

## Install & Upgrade Guide

To install the SDK for the first time:
```sh
pip install luminarycloud
```

Or, to upgrade an existing SDK installation, use the same Python environment
where you previously installed the SDK and run:
```sh
pip install luminarycloud --upgrade
```

:::{tip}
To check if you're using the same Python environment as your previous SDK
installation, run the `pip list` command. The output of the command should
include `luminarycloud` with an earlier SDK version.

After successfully upgrading the SDK using the instructions above, the `pip
list` output should show `luminarycloud` with the latest version.
:::

If you prefer to download the release artifacts instead, visit the [project page
on the Python Package Index (PyPI)](https://pypi.org/project/luminarycloud).

