import * as tf from '@tensorflow/tfjs';
import Command from '../../src/command';

export const add = {
  inputs: [
    new Command(
      'torch.add(input,other,out=None',
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

export const matmul = {
  inputs: [
    new Command(
      'torch.matmul(input, other)',
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
  inputs: [
    new Command(
      'torch.mean(input,dim,out=None)',
      'mean',
      [tf.tensor([0.2294, -0.5481, 1.3288])],
      []
    )
  ],
  answers: [tf.tensor([0.3367])]
};

export const mul = {
  inputs: [
    new Command(
      'torch.mul(input, other)',
      'mul',
      [tf.tensor([10, 20, 30]), 100],
      [['out', 'None']]
    )
  ],
  answers: [tf.tensor([1000, 2000, 3000])]
};

export const div = {
  inputs: [
    new Command(
      'torch.div(input, other)',
      'div',
      [tf.tensor([10, 20, 30, 40]), 0.5],
      []
    )
  ],
  answers: [tf.tensor([20, 40, 60, 80])]
};

export const eq = {
  inputs: [
    new Command(
      'torch.eq(input, other)',
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
  inputs: [
    new Command('torch.sum(input, dim)', 'sum', [tf.tensor([1, 2, 3])], [])
  ],
  answers: [tf.tensor([6])]
};

export const argmax = {
  inputs: [
    new Command(
      'torch.argmax(input, dim)',
      'argmax',
      [tf.tensor([0, 10, 2])],
      [['dim', 1]]
    )
  ],
  answers: [tf.tensor([1])]
};

export const t = {
  inputs: [
    new Command(
      'torch.t(input)',
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
      'torch.softmax(input, dim=None, other)',
      'softmax',
      [tf.tensor([2, 1, 0.1])],
      []
    )
  ],
  answers: [tf.tensor([0.659, 0.2424, 0.0985])]
};

export const relu = {
  inputs: [new Command('torch.nn.functional.relu', 'relu', [[1, -2, 3]], [])],
  answers: [tf.tensor([1, 0, 3])]
};
