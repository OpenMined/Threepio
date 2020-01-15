# Threepio Documentation Crawler

This documentation web crawler is used to generate a set of static JSON files which we can use to help perform certain automatic translations between PyTorch, Tensorflow, and Tensorflow.js.

## Installation

For this project, we use [poetry](https://python-poetry.org/). It's similar the package manager [pip](https://pip.pypa.io/en/stable/) with some built in virtualenv capabilities.

```bash
poetry install
poetry shell # This activates the virtualenv
```

## Usage

```bash
cd docs && sh run_crawlers.sh
```
The static json files are generated in the `output` directory.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.