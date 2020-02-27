import * as tf from '@tensorflow/tfjs';
import Command from '../../src/command';

export const add = new Command(
  'torch.add(input,other,out=None',
  'add',
  [tf.tensor([1]), tf.tensor([1])],
  [['out', 'None']]
);

export const matmul = new Command(
  'torch.matmul(input, other)',
  'matmul',
  [tf.tensor([1]), tf.tensor([1])],
  [['out', 'None']]
);

export const mean = new Command(
  'torch.mean(input,dim,out=None)',
  'mean',
  [tf.tensor([1]), 1],
  []
);

export const mul = new Command(
  'torch.mul(input, other)',
  'mean',
  [tf.tensor([1]), tf.tensor([1])],
  [['out', 'None']]
);

export const div = new Command(
  'torch.div(input, other)',
  'div',
  [tf.tensor([1]), tf.tensor([1])],
  [['out', 'None']]
);

export const eq = new Command(
  'torch.eq(input, other)',
  'eq',
  [tf.tensor([1]), tf.tensor([1])],
  [['out', 'None']]
);

export const sum = new Command(
  'torch.sum(input, dim)',
  'sum',
  [tf.tensor([1]), 1],
  [['out', 'None']]
);

export const argmax = new Command(
  'torch.argmax(input, dim)',
  'argmax',
  [tf.tensor([1]), 1],
  [['out', 'None']]
);

// MISSING
export const t = new Command(
  'torch.t(input)',
  't',
  [tf.tensor([1])],
  [['out', 'None']]
);

export const softmax = new Command(
  'torch.softmax(input, dim=None, other)',
  'softmax',
  [tf.tensor([1]), 1],
  [['out', 'None']]
);

export const relu = new Command(
  'todo',
  'relu',
  [tf.tensor([1]), tf.tensor([1])],
  [['out', 'None']]
);

export const numToTensor = new Command('todo', 'todo', [], []);
export const to = new Command('todo', 'todo', [], []);
export const size = new Command('todo', 'todo', [], []);
export const sub = new Command('todo', 'todo', [], []);
