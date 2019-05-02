#!/usr/bin/env node
'use strict';
const program = require('commander');

program
  .version('0.0.1')
  .description('Scores answers from IPIP NEO survey.')
  .option('-f, --foo', 'Blah B')
  .parse(process.argv);

if (program.foo) {
	console.log(`FOO ${program.args}`);
} else {
	console.log(`NO FOO ${program.args}`);
}

