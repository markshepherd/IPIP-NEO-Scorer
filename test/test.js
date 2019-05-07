#!/usr/bin/env node
'use strict';

const analyzeCSV = require('../analyze');
const { summaryReport } = require('../report');

const fs = require('fs');

const csvPath = "test/Johnson 120 IPIP-NEO-PI-R.csv";
const expectedPath = "test/Expected IPIP-scores.txt";

const red = "\x1b[31m";
const green = "\x1b[32m";
const reset = "\x1b[0m";

/* eslint-disable no-console */
function runTest() {
	fs.readFile(csvPath, 'utf8', function (err, csvData) {
		if (err) throw err;
		const allScores = analyzeCSV(csvData);
		const report = summaryReport(allScores);

		fs.readFile(expectedPath, 'utf8', function (err, expectedReport) {
			if (err) throw err;

			const result = report === expectedReport;
			if (result) {
				console.log(`${green}Test passed${reset}`);
			} else {
				console.log(`${red}Test failed${reset}`);
			}
		});
	});
}
/* eslint-enable no-console */

runTest();
