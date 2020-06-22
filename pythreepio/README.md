
![Tests](https://img.shields.io/github/workflow/status/OpenMined/threepio/PyThreepio)
![License](https://img.shields.io/github/license/OpenMined/threepio)
![OpenCollective](https://img.shields.io/opencollective/all/openmined)

# Threepio Python Client

Threepio is a multi-language library for translating commands between PyTorch, TensorFlow, and TensorFlow.js 
This section of the code-base is for the [Python Client](https://pypi.org/project/3p0/).


## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install threepio.

```bash
pip install 3p0
```

## Usage

```python
import tensorflow as tf
from pythreepio import Threepio, Command

# Create a threepio translating from pytorch -> tensorflow python
threepio = Threepio("torch", "tf", tf)

# Create your command to translate
args = [
    tf.constant([[1, 0], [0, 1]]),
    tf.constant([[0, 1], [1, 0]])
]
kwargs = {}
cmd = Command("add", args, kwargs)

# Translate the command
translated_cmd = threepio.translate(cmd, lookup_command=True)

...

# When you're ready, execute the translation
translated_cmd.execute_routine() # -> [[1, 1], [1, 1]]
```

## Command Support

Support for commands is currently limited. Officially supported commands are listed in our [tests](https://github.com/OpenMined/Threepio/tree/master/pythreepio/tests).