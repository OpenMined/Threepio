import * as tf from '@tensorflow/tfjs';
import Threepio from '../src/threepio';
import {
  add,
  add2,
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
  const threepio = new Threepio('torch', 'tfjs', tf);

  const checkAnswer = (result, answer) => {
    const eq = tf
      .equal(result, answer)
      .all()
      .dataSync();
    expect(eq).toEqual(new Uint8Array([1]));
  };

  const processTests = command => {
    for (const [i, input] of command.inputs.entries()) {
      const translation = threepio.translate(input);
      const result = translation.executeRoutine();
      const answer = command.answers[i];
      checkAnswer(result, answer);
    }
  };

  test('returns itself', () => {
    expect(threepio).toBeInstanceOf(Threepio);
  });

  test('translates add', () => {
    processTests(add);
  });

  test('translates __add__', () => {
    processTests(add2);
  });

  test('translates matmul', () => {
    processTests(matmul);
  });

  test('translates mean', () => {
    processTests(mean);
  });

  test('translates mul', () => {
    processTests(mul);
  });

  test('translates div', () => {
    processTests(div);
  });

  test('translates eq', () => {
    processTests(eq);
  });

  test('translates sum', () => {
    processTests(sum);
  });

  test('translates argmax', () => {
    processTests(argmax);
  });

  // TODO: Write tests for kwargs use of dim

  test('translates transpose', () => {
    processTests(t);
  });

  test('translates softmax', () => {
    for (const [i, input] of softmax.inputs.entries()) {
      const translation = threepio.translate(input);
      const result = translation.executeRoutine().arraySync();
      const answer = softmax.answers[i].arraySync();
      for (const [j, entry] of result.entries()) {
        for (const [k, r] of entry.entries()) {
          expect(r).toBeCloseTo(answer[j][k], 3);
        }
      }
    }
  });

  test('translates relu', () => {
    processTests(relu);
  });
});
