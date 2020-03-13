import * as tf from '@tensorflow/tfjs';
import Command from '../src/command';
const { test, describe, expect } = global; // Import jest from global

describe('Command', () => {
  test('instantiate broken command', () => {
    const args = [tf.tensor([1])];
    const kwargs = [['out', false]];
    const cmd = new Command('torch.matmul', 'matmul', args, kwargs);
    expect(cmd).toBeInstanceOf(Command);
  });

  test('throws error', () => {
    const args = [tf.tensor([1])];
    expect(() => new Command('matmul', args)).toThrow(Error);
  });
});
