import * as tf from '@tensorflow/tfjs';
import Command from '../../src/command';

export const abs = {
  inputs: [new Command('abs', [tf.tensor([1, -2, 3, -4])], {})],
  answers: [tf.tensor([1, 2, 3, 4])]
};

export const add = {
  inputs: [
    new Command(
      'add',
      [
        tf.tensor([
          [1, 0],
          [0, 1]
        ]),
        tf.tensor([
          [0, 1],
          [1, 0]
        ])
      ],
      []
    )
  ],
  answers: [
    tf.tensor([
      [1, 1],
      [1, 1]
    ])
  ]
};

export const add2 = {
  inputs: [
    new Command(
      '__add__',
      [
        tf.tensor([
          [1, 0],
          [0, 1]
        ]),
        tf.tensor([
          [0, 1],
          [1, 0]
        ])
      ],
      []
    )
  ],
  answers: [
    tf.tensor([
      [1, 1],
      [1, 1]
    ])
  ]
};

export const matmul = {
  inputs: [
    new Command(
      'matmul',
      [
        tf.tensor([
          [1, 0],
          [0, 1]
        ]),
        tf.tensor([
          [0, 1],
          [1, 0]
        ])
      ],
      []
    )
  ],
  answers: [
    tf.tensor([
      [0, 1],
      [1, 0]
    ])
  ]
};

export const mean = {
  inputs: [new Command('mean', [tf.tensor([0.2294, -0.5481, 1.3288])], [])],
  answers: [tf.tensor([0.3367])]
};

export const mul = {
  inputs: [new Command('mul', [tf.tensor([10, 20, 30]), 100], [])],
  answers: [tf.tensor([1000, 2000, 3000])]
};

export const div = {
  inputs: [new Command('div', [tf.tensor([10, 20, 30, 40]), 0.5], [])],
  answers: [tf.tensor([20, 40, 60, 80])]
};

export const eq = {
  inputs: [
    new Command(
      'eq',
      [
        tf.tensor([
          [1, 2],
          [3, 4]
        ]),
        tf.tensor([
          [1, 1],
          [4, 4]
        ])
      ],
      []
    )
  ],
  answers: [
    tf.tensor([
      [1, 0],
      [0, 1]
    ])
  ]
};

export const sum = {
  inputs: [new Command('sum', [tf.tensor([1, 2, 3])], [])],
  answers: [tf.tensor([6])]
};

export const argmax = {
  inputs: [
    new Command(
      'argmax',
      [
        tf.tensor([
          [0, 10, 2],
          [1, 20, 30],
          [10, 0, 0]
        ])
      ],
      { dim: -1 }
    )
  ],
  answers: [tf.tensor([1, 2, 0])]
};

export const t = {
  inputs: [
    new Command(
      't',
      [
        tf.tensor([
          [1, 2, 3],
          [4, 5, 6]
        ])
      ],
      []
    )
  ],
  answers: [
    tf.tensor([
      [1, 4],
      [2, 5],
      [3, 6]
    ])
  ]
};

export const softmax = {
  inputs: [
    new Command(
      'softmax',
      [
        tf.tensor([
          [2, 1, 0.1],
          [2, 1, 0.1],
          [2, 1, 0.1]
        ])
      ],
      { dim: -1 }
    )
  ],
  answers: [
    tf.tensor([
      [0.659, 0.2424, 0.0985],
      [0.659, 0.2424, 0.0985],
      [0.659, 0.2424, 0.0985]
    ])
  ]
};

export const relu = {
  inputs: [new Command('relu', [[1, -2, 3]], [])],
  answers: [tf.tensor([1, 0, 3])]
};

export const sub = {
  inputs: [
    new Command(
      'sub',
      [
        [2, 3, 4],
        [1, 2, 3]
      ],
      {}
    )
  ],
  answers: [tf.tensor([1, 1, 1])]
};

export const select = {
  inputs: [
    new Command(
      'select',
      [
        [
          [
            [1, 2],
            [3, 4]
          ],
          [
            [5, 6],
            [7, 8]
          ]
        ],
        0,
        1
      ],
      {}
    )
  ],
  answers: [
    // Same as t.gather(1, 0).
    tf.tensor([
      [5, 6],
      [7, 8]
    ])
  ]
};

export const rsub = {
  inputs: [new Command('__rsub__', [[1, 2, 3], 1], {})],
  answers: [tf.tensor([0, -1, -2])]
};

export const truediv = {
  inputs: [
    new Command(
      'truediv',
      [
        [1, 2, 3],
        [1, 2, 3]
      ],
      {}
    )
  ],
  answers: [tf.tensor([1, 1, 1])]
};
