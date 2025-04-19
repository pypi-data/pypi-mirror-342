<div align="center">

<img src="https://raw.githubusercontent.com/k1shk1n/outlify/main/assets/header.svg" alt="outlify header" width="600">

Structured cli output — beautifully, simply, and dependency-free.

[Overview](#overview) •
[Install](#install) •
[Usage](#usage) •
[License](#license)

<img src="https://raw.githubusercontent.com/k1shk1n/outlify/main/assets/footer.svg" alt="outlify footer" width="600">

[![PyPI](https://img.shields.io/pypi/v/outlify)](https://pypi.org/project/outlify/)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/outlify)
![Build](https://github.com/k1shk1n/outlify/actions/workflows/checks.yaml/badge.svg)
![Repo Size](https://img.shields.io/github/repo-size/k1shk1n/outlify)
[![ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

</div>

## Overview
**Outlify** is designed with a focus on streamlined log output, making it perfect for cli tools.
It emphasizes lightweight operation and minimal dependencies, ensuring smooth integration
into any project. The second key aspect of **Outlify** is its beautiful and user-friendly
log formatting, designed to enhance readability and provide a pleasant experience
for developers and their users.

## Install
**Outlify** is available as a Python package and can be easily installed via `pip` from [PyPI](https://pypi.org/project/outlify/).

To install, simply run the following command:
```bash
pip install outlify
```
This will automatically install the latest version of **Outlify**.

## Usage
You can view demos of any available modules by running the following command:
```bash
python -m outlify.module_name
```

For example, to view the demo for the **Panel** module:
```bash
python -m outlify.panel
```

### Panels 
To highlight important text by displaying it within a panel, use `Panel`. Here's how:
```python
from outlify.panel import Panel

print(Panel('A very important text', title='Warning'))
```

To display parameters in a structured format, use the `ParamsPanel`:
```python
from outlify.panel import ParamsPanel

parameters = {'parameter1': 'value1', 'parameter2': 'value2'}
print(ParamsPanel(parameters, title='Startup Parameters'))
```

For more details on how to use Panels, see [Panel](docs/components/panel.md)

## License
Licensed under the [MIT License, Copyright (c) 2025 Vladislav Kishkin](LICENSE)