![Threepio logo](/threepio.png)

![Coverage](https://img.shields.io/codecov/c/github/OpenMined/threepio)
![License](https://img.shields.io/github/license/OpenMined/threepio)
![OpenCollective](https://img.shields.io/opencollective/all/openmined)

# Threepio

Threepio makes it _dead simple_ to translate commands between machine learning frameworks such as **PyTorch, Tensorflow.js, and Tensorflow Python**.
It acts as a core component in [PySyft](https://github.com/OpenMined/PySyft) and [syft.js](https://github.com/OpenMined/syft.js).
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

Threepio is made up of two main components:
- :spider: [Documentation Crawler](/docs-crawler) - This generates the majority of our automatic translations for Threepio
- :snake: [Python translation library](/pythreepio) - This is the python library for using threepio

~And has clients in both Python and Javascript!~
And has a client available in Python!

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
** Threepio.js has been deprecated. For existing javascript code, please refer to commit [0a538a3f](https://github.com/OpenMined/Threepio/commit/0a538a3f1ed70b39be541766211f6b84e2136fc3) **

#### Usage

Please check out our [usage document](/js/README.md) for further guidelines.

## Support

For support in using this library, please join the **#lib_threepio** Slack channel. If you'd like to follow along with any code changes to the library, please join the **#code_threepio** Slack channel. [Click here to join our Slack community!](https://slack.openmined.org)

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## Contributors

Thanks to these awesome people:

<br>
<table>
  <tr>
    <td align="center">
      <a href="https://github.com/Nolski">
        <img src="https://avatars2.githubusercontent.com/u/2600677?s=460&u=811946f54689f01b8393b654d272e16f3f3edcb7&v=4" width="170px;" alt="Mike Nolan avatar">
        <br /><sub><b>Mike Nolan</b></sub></a><br />
        <sub>OM FL Workers Team / Author</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/AmrMKayid">
        <img src="https://avatars2.githubusercontent.com/u/18689888?s=460&u=a06bdf9b6b680199616f20d818d4995bf1fe34fa&v=4"  width="170px;" alt="Amr Kayid avatar">
        <br /><sub><b>Amr Kayid</b></sub></a><br />
        <sub>Contributor</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/vvmnnnkv">
        <img src="https://avatars0.githubusercontent.com/u/12518480?s=460&u=6fb6c713741b863c49a0ba0b78dd3ced2d1629ce&v=4"  width="170px;" alt="Vova Manannikov avatar">
        <br /><sub><b>Vova Manannikov</b></sub></a><br />
        <sub>OM FL Workers Team</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/cereallarceny">
        <img src="https://avatars2.githubusercontent.com/u/1297930?s=460&u=e7b99423492a3b853d610381bc1f4c430988947a&v=4"  width="170px;" alt="Patrick Cason avatar">
        <br /><sub><b>Patrick Cason</b></sub></a><br />
        <sub>OM FL Workers Team Lead</sub>
      </a>
    </td>
  </tr>
  <tr>
    <td align="center">
      <a href="https://github.com/ateniolatobi">
        <img src="https://avatars0.githubusercontent.com/u/28807442?s=460&u=c55b6dc59f3b075081d039e47867e02c1127ced3&v=4" width="170px;" alt="Tvictor avatar">
        <br /><sub><b>Tvictor</b></sub></a><br />
        <sub>OM FL Workers Team</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/ramesht007">
        <img src="https://avatars2.githubusercontent.com/u/36106177?s=460&u=09a9cee652a005ef6f4aed14844c659b56dfcdc7&v=4" width="170px;" alt="Raemsht Shukla avatar">
        <br /><sub><b>Ramesht Shukla</b></sub></a><br />
        <sub>OM FL Workers Team</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/juharris">
        <img src="https://avatars2.githubusercontent.com/u/1594505?s=460&u=ad2e7ce918028dce4c0f6c33275357e9c7c4819d&v=4"  width="170px;" alt="Justin D. Harris avatar">
        <br /><sub><b>Justin D. Harris</b></sub></a><br />
        <sub>Contributor</sub>
      </a>
    </td>
    <td align="center">
      <a href="https://github.com/pedroespindula">
        <img src="https://avatars2.githubusercontent.com/u/38431219?s=460&u=003868dcbbbad26cf23f8eb14d06501354b946c7&v=4"  width="170px;" alt="Pedro Espíndula avatar">
        <br /><sub><b>Pedro Espíndula</b></sub></a><br />
        <sub>Contributor</sub>
      </a>
    </td>    
  </tr>
  <tr>
  <td align="center">
      <a href="https://github.com/anirbansaha782">
        <img src="https://avatars1.githubusercontent.com/u/55926653?s=460&v=4"  width="170px;" alt="Anirban Aaha avatar">
        <br /><sub><b>Anirban Aaha</b></sub></a><br />
        <sub>Contributor</sub>
      </a>
    </td>
  </tr>
  
  
</table>
<br>

## License
[Apache License 2.0](https://choosealicense.com/licenses/apache-2.0/)
