import * as tf from '@tensorflow/tfjs';
import Threepio from '../src/threepio';
import {
  add,
  matmul,
  mean,
  mul,
  div,
  eq,
  sum,
  argmax
} from './fixtures/pytorch';
const { test, describe, expect } = global; // import jest from global

describe('Threepio', () => {
  const threepio = new Threepio({});

  const checkAnswer = (result, answer) => {
    const eq = tf
      .equal(result, answer)
      .all()
      .dataSync();
    expect(eq).toEqual(new Uint8Array([1]));
  };

  test('returns itself', () => {
    expect(threepio).toBeInstanceOf(Threepio);
  });

  test('translates add', () => {
    const execAdd = threepio.translate('tfjs', add);
    const result = execAdd.executeRoutine();
    const answer = tf.tensor([
      [1, 1],
      [1, 1]
    ]);
    checkAnswer(result, answer);
  });

  test('translates matmul', () => {
    const execadd = threepio.translate('tfjs', matmul);
    const result = execadd.executeRoutine();
    const answer = tf.tensor([
      [0, 1],
      [1, 0]
    ]);
    checkAnswer(result, answer);
  });

  test('translates mean', () => {
    const execadd = threepio.translate('tfjs', mean);
    const result = execadd.executeRoutine();
    const answer = tf.tensor([0.3367]);
    checkAnswer(result, answer);
  });

  test('translates mul', () => {
    const execadd = threepio.translate('tfjs', mul);
    const result = execadd.executeRoutine();
    const answer = tf.tensor([1000, 2000, 3000]);
    checkAnswer(result, answer);
  });

  test('translates div', () => {
    const execadd = threepio.translate('tfjs', div);
    const result = execadd.executeRoutine();
    const answer = tf.tensor([20, 40, 60, 80]);
    checkAnswer(result, answer);
  });

  test.skip('translates eq', () => {
    const execadd = threepio.translate('tfjs', eq);
    const result = execadd.executeRoutine();
    const answer = tf.tensor([
      [1, 0],
      [0, 1]
    ]);
    checkAnswer(result, answer);
  });

  test('translates sum', () => {
    const execadd = threepio.translate('tfjs', sum);
    const result = execadd.executeRoutine();
    const answer = tf.tensor([6]);
    checkAnswer(result, answer);
  });

  test('translates argmax', () => {
    const execadd = threepio.translate('tfjs', argmax);
    const result = execadd.executeRoutine();
    const answer = tf.tensor([1]);
    checkAnswer(result, answer);
  });
});
