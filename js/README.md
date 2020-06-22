![Tests](https://img.shields.io/github/workflow/status/OpenMined/threepio/Node.js%20CI)
![License](https://img.shields.io/github/license/OpenMined/threepio)
![OpenCollective](https://img.shields.io/opencollective/all/openmined)

# Threepio Javascript Client

Threepio is a multi-language library for translating commands between PyTorch, TensorFlow, and TensorFlow.js 
This section of the code-base is for the [Javascript Client](https://www.npmjs.com/package/@openmined/threepio).


## Installation

Use the package manager [npm](https://npmjs.com) to install threepio.

```bash
npm install --save @openmined/threepio
```

## Usage

```javascript
import * as tf from '@tensorflow/tfjs';
import Threepio from '../src/threepio';

// Create your command to translate
const args = [
    tf.tensor([
        [1, 0],
        [0, 1]
    ]),
    tf.tensor([
        [0, 1],
        [1, 0]
    ])
];
const kwargs = {};
const cmd = new Command("add", args, kwargs);

// Create a threepio translating from pytorch -> tensorflow python
const threepio = new Threepio('torch', 'tfjs', tf);


// Translate the command
const translation = threepio.translate(input);

...

// When you're ready, execute the translation
translation.executeRoutine(); // -> [[1, 1], [1, 1]]
```

## Command Support

Support for commands is currently limited. Officially supported commands are listed in our [tests](https://github.com/OpenMined/Threepio/tree/master/js/tests).