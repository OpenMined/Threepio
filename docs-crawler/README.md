# Threepio Automatic Translation Generator

This translation generator is used to generate a set of static JSON files which we can use to help perform certain automatic translations between PyTorch, Tensorflow, and Tensorflow.js.

## Installation

For this project, we use [poetry](https://python-poetry.org/). It's similar the package manager [pip](https://pip.pypa.io/en/stable/) with some built in virtualenv capabilities.

```bash
poetry install
poetry shell # This activates the virtualenv
```

## Usage

To generate the most recent automatic translations, we must complete two steps:

 - Crawl the most recent version of the documentation sites
 - Generate translations from the updated definitions


### Crawl the docs

#### Run Instructions on osX / Linux

#### Run Instructions on osX / Linux

```bash
cd docs && sh run_crawlers.sh
```
#### Run Instructions on Windows

```bash
cd docs && run_crawlers.bat
```


The static json files are generated and stored in the `output` directory.

### Generate the definitions

Currently generating the definitions is perfomed by the script `aggregate_crawler_output.py`

To run it you simply

```bash
cd docs && python aggregate_crawler_output.py
```

This will generate and store new output files in `threepio/static/` (for js) and `threepio/pythreepio/static/` (for python).

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

For adding manual translations, you will want to look in our [translations.py](https://github.com/OpenMined/Threepio/blob/master/docs-crawler/docs/translations.py) file and follow the existing translation schema.
