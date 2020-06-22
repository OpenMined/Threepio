![open mined-logo](https://github.com/OpenMined/design-assets/blob/master/logos/OM/horizontal-primary-trans.png)

![Coverage](https://img.shields.io/codecov/c/github/OpenMined/threepio)
![License](https://img.shields.io/github/license/OpenMined/threepio)
![OpenCollective](https://img.shields.io/opencollective/all/openmined)

# Threepio

Threepio makes it _dead simple_ to translate commands between machine learning frameworks such as **PyTorch, Tensorflow.js, and Tensorflow Python**.
It acts as a core component in PySyft and Syft.js.
Some of the life changing features this library provides are:

 - :robot: Automatic bi-directional translation between same named commands `add`, `abs`, etc.
 - :brain: Smart argument mapping between automaticaly translated commands
 - :repeat: Word level translation between libraries
 - :wrench: Custom command translation
 - :herb: One to many command translation
 - :zap: Translation of tensor methods _(in progress)_
 - :mag: Support for fuzzy match in automatic command translation _(in progress)_
 - :card_index_dividers: Support for framework versioning in automatic translation _(in progress)_
 - :mage_man: Support for automatic argument type casting (tensorflow tensor -> pytorch tensor) _(in progress)_

Threepio is made up of three main components:
- :spider: [Documentation Crawler](/docs-crawler) - This generates the majority of our automatic translations for Threepio
- :snake: [Python translation library](/pythreepio) - This is the python library for using threepio
- :coffee: [JS translation library](/js) - This is the javascript library for using threepio

And has clients in both Python and Javascript!

## Installation

Depending on your language, installation will differ.

### Python
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install threepio.

```bash
pip install 3p0
```

#### Usage

Please check out our [usage document](/pythreepio/README.md) for further guidelines.

### Javascript
Use the package manager [npm](https://www.npmjs.com/) to install threepio.

```bash
npm install @openmined/threepio
```

#### Usage

Please check out our [usage document](/js/README.md) for further guidelines.

## Support

For support in using this library, please join the **#lib_threepio** Slack channel. If you'd like to follow along with any code changes to the library, please join the **#code_threepio** Slack channel. [Click here to join our Slack community!](https://slack.openmined.org)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Contributors

Please make sure to fill this section in with **all former and current** contributors to the project. [Documentation on how to do this is located here.](https://github.com/all-contributors/all-contributors)

## License
[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/)
