'use strict'

const assert = require('node:assert/strict')
const { stripHarnessLines, MARKERS } = require('../extensions/strip-test-harness')

const typeql = MARKERS.typeql

assert.deepEqual(
  stripHarnessLines([
    '#!test[schema]',
    '#{{',
    'define entity person;',
    '#}}',
    '#!test[read]',
    'match $p isa person;',
  ], typeql),
  ['match $p isa person;']
)

assert.deepEqual(
  stripHarnessLines(['#!test[write]', 'insert $x isa thing;'], typeql),
  ['insert $x isa thing;']
)

assert.deepEqual(
  stripHarnessLines(['#!test', '#{{ hidden', 'more', '#}}', 'visible'], typeql),
  ['visible']
)

assert.deepEqual(
  stripHarnessLines(['#!test[read]', '# Regular comment', 'match $a;'], typeql),
  ['# Regular comment', 'match $a;']
)

assert.deepEqual(stripHarnessLines(['plain query;'], typeql), ['plain query;'])

assert.deepEqual(
  stripHarnessLines([
    '#!test[schema]',
    '#{{',
    'define entity person;',
    '#}}',
    '#---',
    'match $p isa person;',
  ], typeql),
  ['match $p isa person;']
)

console.log('strip-test-harness: all assertions passed')
