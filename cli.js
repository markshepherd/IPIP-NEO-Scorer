#!/usr/bin/env node
'use strict';
const doit = require('./doit');

if (process.argv.length !== 3) {
	console.log('Please specify exactly 1 file.');
	process.exit();
}

doit(process.argv[2]);