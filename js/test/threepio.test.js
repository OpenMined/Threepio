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
  argmax,
  t,
  softmax,
  relu
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
    const translation = threepio.translate('tfjs', add);
    const result = translation.executeRoutine();
    const answer = tf.tensor([
      [1, 1],
      [1, 1]
    ]);
    checkAnswer(result, answer);
  });

  test('translates matmul', () => {
    const translation = threepio.translate('tfjs', matmul);
    const result = translation.executeRoutine();
    const answer = tf.tensor([
      [0, 1],
      [1, 0]
    ]);
    checkAnswer(result, answer);
  });

  test('translates mean', () => {
    const translation = threepio.translate('tfjs', mean);
    const result = translation.executeRoutine();
    const answer = tf.tensor([0.3367]);
    checkAnswer(result, answer);
  });

  test('translates mul', () => {
    const translation = threepio.translate('tfjs', mul);
    const result = translation.executeRoutine();
    const answer = tf.tensor([1000, 2000, 3000]);
    checkAnswer(result, answer);
  });

  test('translates div', () => {
    const translation = threepio.translate('tfjs', div);
    const result = translation.executeRoutine();
    const answer = tf.tensor([20, 40, 60, 80]);
    checkAnswer(result, answer);
  });

  test('translates eq', () => {
    const translation = threepio.translate('tfjs', eq);
    const result = translation.executeRoutine();
    const answer = tf.tensor([
      [1, 0],
      [0, 1]
    ]);
    checkAnswer(result, answer);
  });

  test('translates sum', () => {
    const translation = threepio.translate('tfjs', sum);
    const result = translation.executeRoutine();
    const answer = tf.tensor([6]);
    checkAnswer(result, answer);
  });

  test('translates argmax', () => {
    const translation = threepio.translate('tfjs', argmax);
    const result = translation.executeRoutine();
    const answer = tf.tensor([1]);
    checkAnswer(result, answer);
  });

  test('translates transpose', () => {
    const translation = threepio.translate('tfjs', t);
    const result = translation.executeRoutine();
    const answer = tf.tensor([
      [1, 4],
      [2, 5],
      [3, 6]
    ]);
    checkAnswer(result, answer);
  });

  test('translates softmax', () => {
    const translation = threepio.translate('tfjs', softmax);
    const result = translation.executeRoutine().dataSync();
    const answer = tf.tensor([0.659, 0.2424, 0.0985]).dataSync();
    for (const [i, r] of result.entries()) {
      expect(r).toBeCloseTo(answer[i], 3);
    }
  });

  test('translates relu', () => {
    const translation = threepio.translate('tfjs', relu);
    const result = translation.executeRoutine().dataSync();
    const answer = tf.tensor([1, 0, 3]);
    checkAnswer(result, answer);
  });
});
