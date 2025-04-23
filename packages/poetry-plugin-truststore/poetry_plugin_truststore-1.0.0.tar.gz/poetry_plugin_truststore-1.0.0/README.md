Truststore for Poetry
=====================

Adding system certificate store support to in [Poetry](https://python-poetry.org) using [Truststore](https://pypi.org/project/truststore/) package 


## Installation

The easiest way to install the `truststore` plugin is via the `self add` command of Poetry.

```bash
poetry self add poetry-plugin-truststore
```

If you used `pipx` to install Poetry you can add the plugin via the `pipx inject` command.

```bash
pipx inject poetry poetry-plugin-truststore
```

Otherwise, if you used `pip` to install Poetry you can add the plugin packages via the `pip install` command.

```bash
pip install poetry-plugin-truststore
```

## Usage

The plugin basically runs `truststore.inject_into_ssl()` when you use poetry, making sure Truststore do its patching magic.

You can check if plugin is correctly installed by using almost any poetry command with `-v` flag, like:
```bash
poetry version -v
```
And check if there is a message
> Using system cert store via Truststore x.y.z
