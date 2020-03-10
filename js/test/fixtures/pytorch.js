import * as tf from '@tensorflow/tfjs';
import Command from '../../src/command';

export const add = new Command(
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
  [['out', 'None']]
);

export const matmul = new Command(
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
  [['out', 'None']]
);

export const mean = new Command(
  'torch.mean(input,dim,out=None)',
  'mean',
  [tf.tensor([0.2294, -0.5481, 1.3288])],
  []
);

export const mul = new Command(
  'torch.mul(input, other)',
  'mul',
  [tf.tensor([10, 20, 30]), 100],
  [['out', 'None']]
);

export const div = new Command(
  'torch.div(input, other)',
  'div',
  [tf.tensor([10, 20, 30, 40]), 0.5],
  [['out', 'None']]
);

export const eq = new Command(
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

  [['out', 'None']]
);

export const sum = new Command(
  'torch.sum(input, dim)',
  'sum',
  [tf.tensor([1, 2, 3])],
  [['out', 'None']]
);

export const argmax = new Command(
  'torch.argmax(input, dim)',
  'argmax',
  [tf.tensor([0, 10, 2])],
  [['out', 'None']]
);

export const t = new Command(
  'torch.t(input)',
  't',
  [
    tf.tensor([
      [1, 2, 3],
      [4, 5, 6]
    ])
  ],
  [['out', 'None']]
);

export const softmax = new Command(
  'torch.softmax(input, dim=None, other)',
  'softmax',
  [tf.tensor([2, 1, 0.1])],
  [['out', 'None']]
);

export const relu = new Command(
  'torch.nn.functional.relu',
  'relu',
  [[1, -2, 3]],
  []
);
