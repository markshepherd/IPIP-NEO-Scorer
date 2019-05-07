#!/usr/bin/env node
'use strict';

const analyzeCSV = require('./analyze');
const { summaryReport, makePDF, exportRawData } = require('./report');
const packageJson = require('./package.json');

// Here's the main program. This is where we handle all interfacing with the outside world (file system, user interaction, ...)
const readline = require('readline-sync');
const moment = require('moment');
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
async function main() {
	// We color our messages so that they stand out from all the spam that appears in the console window
	// of the standalone app created by 'pkg'.
	// For more colors, see https://stackoverflow.com/questions/9781218/how-to-change-node-jss-console-font-color
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

	// Create a folder for the results
	const timeDate = moment(new Date()).format('MMM D Y h.mm a');
	const outputFolder = path.join(os.homedir(), 'Documents', 'IPIP Scores', timeDate);
	const oututFolderDescription = `Documents > IPIP Scores > ${timeDate}`;
	try {
		fs.mkdirSync(outputFolder, { recursive: true });
    } catch (err) {
		if (err.code !== 'EEXIST') {
			throw err;

			// Not sure if we need this...
			// To avoid `EISDIR` error on Mac and `EACCES`-->`ENOENT` and `EPERM` on Windows.
			// if (err.code === 'ENOENT') { // Throw the original parentDir error on curDir `ENOENT` failure.
			// 	`EACCES: permission denied, mkdir '${outputFolder}'`);
			// }

			// const caughtErr = ['EACCES', 'EPERM', 'EISDIR'].indexOf(err.code) > -1;
			// if (!caughtErr || caughtErr && curDir === path.resolve(targetDir)) {
			// 	throw err; // Throw if it's just the last created dir.
			// }
		}
    }

	// Now the action begins ... 

	// Read the data file
	const csvData = fs.readFileSync(csvPath, 'utf8');
	fs.writeFile(path.join(outputFolder, 'Survey answers.csv'), csvData, (err) => {
		if (err) {
			console.log(`${highlight2}${err}${reset}`);
		}
	});

	// Analyze the data
	const allScores = analyzeCSV(csvData);

	// Make the PDFs
	await makePDF(allScores, outputFolder);

	// Create the report and write it to the output file
	const report = summaryReport(allScores);
	fs.writeFile(path.join(outputFolder, 'Summary Report.txt'), report, (err) => {
		if (err) {
			console.log(`${highlight2}e${err}${reset}`);
		}
	});

	// Export the raw data in csv format
	const rawData = exportRawData(allScores);
	fs.writeFile(path.join(outputFolder, 'Raw Data.csv'), rawData, (err) => {
		if (err) {
			console.log(`${highlight2}e${err}${reset}`);
		}
	});
	
	console.log(`${highlight2}\nResults are in ${highlight}${bright}${oututFolderDescription}${reset}${highlight2}\n${reset}`);
}
/* eslint-enable no-console */

main();


