#!/usr/bin/env node


const analyzeCSV = require("../src/analyze");
const {summaryReport, exportScores} = require("../src/report");

const fs = require("fs");

const csvPath = "test/Johnson 120 IPIP-NEO-PI-R.csv";
const expectedReportPath = "test/Expected Report.txt";
const expectedScoresPath = "test/Expected Scores.csv";

const red = "\x1b[31m";
const green = "\x1b[32m";
const reset = "\x1b[0m";

/* eslint-disable no-console */
function runTest () {
	fs.readFile(csvPath, "utf8", (err, csvData) => {
		if (err) { throw err; }
		const allScores = analyzeCSV(csvData);
		let failureCount = 0;

		const report = summaryReport(allScores);
		const expectedReport = fs.readFileSync(expectedReportPath, "utf8");
		if (report !== expectedReport) {
			failureCount += 1;
		}

		const exportedScores = exportScores(allScores);
		const expectedScores = fs.readFileSync(expectedScoresPath, "utf8");
		if (exportedScores !== expectedScores) {
			failureCount += 1;
		}

		if (failureCount === 0) {
			console.log(`${green}Test passed${reset}`);
		} else {
			console.log(`${red}Test failed${reset}`);
		}
	});
}
/* eslint-enable no-console */

runTest();
