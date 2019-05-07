#!/usr/bin/env node
'use strict';

const analyzeCSV = require('./analyze');
const { summaryReport } = require('./report');
const packageJson = require('./package.json');

// Here's the main program. This is where we handle all interfacing with the outside world (file system, user interaction, ...)
const readline = require('readline-sync');
const fs = require('fs');
const path = require('path');
const os = require('os');

const instructions = `
This app analyzes user responses to the 
SurveyMonkey survey "Johnson 120 IPIP-NEO-PI-R". 
The result is a report that gives each user's 
score for the Big 5 personality traits and the 30 facets.

To get the data:
- log in to https://www.surveymonkey.com
- go to the "Johnson 120 IPIP-NEO-PI-R" project
- go to Analyze Results
- do Save As > Export File > All individual responses
- select File Format XLS
- do Export
- when it says Your export is complete, click Download
- in Finder, go to the Downloads folder
- locate the file you just downloaded, something like Data_All_190503.zip
- double click the downloaded file to unzip it
- open the resulting folder, something like Data_All_190503
- open the CSV folder
- drag the file "Johnson 120 IPIP-NEO-PI-R.csv" to this window
- click in this window, then press Return
`;

/* eslint-disable no-console */
function main() {

	// Fun with console colors. For more, see https://stackoverflow.com/questions/9781218/how-to-change-node-jss-console-font-color.
	// We color our messages so that they stand out from all the spam the appears in the console window
	// of the standalone app created by pkg.
	const reset = "\x1b[0m";
	const highlight = "\x1b[36m";
	const highlight2 = "\x1b[32m";
	const bright = "\x1b[1m";

	console.log(`${highlight}--- Scorer ${packageJson.version} for Johnson 120 IPIP-NEO-PI-R survey ---\n${instructions}${reset}`);

	// Find the path we're reading from. It might be a command-line parameter, or we might have to prompt for it.
	let csvPath;
	if (process.argv.length === 3) {
		csvPath = process.argv[2];
	} else {
		csvPath = readline.question(`${highlight}Please enter location of csv file:${reset}`);
		// remove any extra backslash characters that are added into the path string when a user drags a file from finder to consolewindow.
		csvPath = csvPath.split("\\").join(""); 
	}

	// Now the action begins ... 

	// Read the data file
	fs.readFile(csvPath, 'utf8', function (err, csvData) {
		if (err) throw err;

		// Analyze the data
		const allScores = analyzeCSV(csvData);

		// Create the report
		const report = summaryReport(allScores);

		// Write the report to the output file
		const outputPath = path.join(os.homedir(), 'Desktop', 'IPIP-scores.txt')
		fs.writeFile(outputPath, report, (err) => {
			if (err) {
				console.log(`${highlight2}err${reset}`);
			} else {
				console.log(`${highlight2}\nReport file ${highlight}${bright}IPIP-scores.txt${reset}${highlight2} written to Desktop\n${reset}`);
				console.log(`(${outputPath})\n`);
			}
		});
	});
}
/* eslint-enable no-console */

main();


