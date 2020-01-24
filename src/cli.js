#!/usr/bin/env node


const analyzeCSV = require("./analyze");
const {summaryReport, makePDF, exportScores} = require("./report");
const packageJson = require("../package.json");

// Here's the main program. This is where we handle all interfacing with the outside world (file system, user interaction, ...)
const readline = require("readline-sync");
const moment = require("moment");
const fs = require("fs");
const path = require("path");
const os = require("os");

const instructions = `
This app analyzes user responses to the 
SurveyMonkey survey "Personality and Motivation in Persons with Alcohol Problems". 
The result is a report that gives each user's 
score for the Big 5 personality traits and the 30 facets.

To get the data:
- log in to https://www.surveymonkey.com
- go to the "Personality and Motivation in Persons with Alcohol Problems" project
- go to Analyze Results
- do Save As > Export File > All individual responses
- select File Format CSV
- do Export
- when it says Your export is complete, click Download
- in Finder, go to the Downloads folder
- locate the file you just downloaded, something like Data_All_190503.zip
- double click the downloaded file to unzip it
- open the CSV folder
- drag the file "Personality and Motivation in Persons with Alcohol Problems.csv" to this window
- click in this window, then press Return
`;

const resultDescription = `
Scores.csv
- a spreadsheet containing each user's 5 domain scores and 30 facet scores

Report.txt
- a report giving each user's scores, annotated to help evaluate reliability

<UserID>.pdf
- for each user, a detailed custom report explaining the user's scores

Survey Answers.csv
- a copy of the input data file
`;

/* eslint-disable no-console */
async function main () {
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
		// Remove any extra backslash characters that are added into the path string when a user drags a file from finder to consolewindow.
		csvPath = csvPath.split("\\").join("");
	}

	// Create a folder for the results
	const timeDate = moment(new Date()).format("MMM D Y h.mm a");
	const oututFolderDescription = `Documents > IPIP Scores > ${timeDate}`;
	let outputFolder = path.join(os.homedir(), "Documents", "IPIP Scores");
	try {
		fs.mkdirSync(outputFolder);
	} catch (err) {
		if (err.code !== "EEXIST") {
			throw err;
		}
	}
	outputFolder = path.join(outputFolder, timeDate);
	try {
		fs.mkdirSync(outputFolder);
	} catch (err) {
		if (err.code !== "EEXIST") {
			throw err;
		}
	}

	// Now the action begins ...

	// Read the data file
	const csvData = fs.readFileSync(csvPath, "utf8");

	// Take a copy of the data file
	fs.writeFile(path.join(outputFolder, "Survey Answers.csv"), csvData, (err) => {
		if (err) {
			console.log(`${highlight2}${err}${reset}`);
		}
	});

	// Analyze the data
	const allScores = analyzeCSV(csvData);

	// Create the report and write it to the output file
	const report = summaryReport(allScores);
	fs.writeFile(path.join(outputFolder, "Report.txt"), report, (err) => {
		if (err) {
			console.log(`${highlight2}e${err}${reset}`);
		}
	});

	// Export the raw data in csv format
	const exportedScores = exportScores(allScores);
	fs.writeFile(path.join(outputFolder, "Scores.csv"), exportedScores, (err) => {
		if (err) {
			console.log(`${highlight2}e${err}${reset}`);
		}
	});

	// Make the PDFs
	await makePDF(allScores, outputFolder);

	// Done!
	console.log(`${highlight2}\n\nResults are in ${highlight}${bright}${oututFolderDescription}${reset}${highlight2}\n${reset}`);
	console.log(`${highlight}${resultDescription}${reset}`);
}
/* eslint-enable no-console */

main();


