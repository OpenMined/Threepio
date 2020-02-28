import Threepio from '../src/threepio';
import { add } from './fixtures/pytorch';
const { test, describe, expect } = global; // import jest from global

describe('Threepio', () => {
  const brokenAdd = {
    ...add,
    kwargs: undefined
  };
  const threepio = new Threepio({});

  test('returns itself', () => {
    expect(threepio).toBeInstanceOf(Threepio);
  });

  test('translate basic function', () => {
    threepio.translate('tfjs', add);
  });

  test('ensure error', () => {
    expect(() => threepio.translate(brokenAdd)).toThrow(Error);
  });
});
