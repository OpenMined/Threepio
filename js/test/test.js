const test = require('ava');

const Threepio = require('..');

test.beforeEach(t => {
  const threepio = new Threepio({});
  Object.assign(t.context, { threepio });
});

test('returns itself', t => {
  t.true(t.context.threepio instanceof Threepio);
});
