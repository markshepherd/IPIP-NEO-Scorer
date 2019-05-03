#!/usr/bin/env node
'use strict';

const { getItems } = require('@alheimsins/b5-johnson-120-ipip-neo-pi-r');
const { getTemplate } = require('@alheimsins/b5-result-text');

// questionInfo contains information about each question:
// - what domain and facet the question is associated with
// - what score is assigned to each possible answer
const questionInfo = getItems('en');

// Create a report for one completed survey by one user. The report is 
// returned in the form of a string.
//
// 'scores' is the user's aggregated score for all domains and facets, in the form
//   {
//      domain1: {
//		  facet1: {score: <num>, count: <num>},
//		  facet2: {...},
//        ...
//      domain2: {
//	      ....
//   }
// 'score' is the total score across all questions for the given domain+facet
// and 'count' is the number of questions associated with the given domain+facet
//
function createOneReport(emailaddress, scores) {
	var outputString = "";

	outputString += `\n${emailaddress}\n`;

	// Fetch the template which contains a list of all the domains and facets, including their human-readable names. 
	// The order of items in the template defines the order of the report.
	const template = getTemplate();

	// Iterate over the domains in the template
	for (var i = 0; i < template.length; i++) {
		var domain = template[i];

		// Iterate over the facets of this domain. Accumulate the score and count
		// of each facet into a total score and count for this domain.
		var totalScore = 0;
		var totalCount = 0;
		for (var j = 0; j < domain.facets.length; j++) {
			var facet = domain.facets[j];

			// Grab the scores data for this domain+facet; just use zero if no data.
			const score = scores[domain.domain][facet.facet] || {score: 0, count: 0};

			// Collect our information
			totalScore += score.score;
			totalCount += score.count;
		}

		// Print the domain summary line
		outputString += `\n    ${domain.domain}. ${domain.title}: ${totalScore} / ${totalCount * 5}\n`;

		// Iterate over facets and print a line for each facet.
		for (var k = 0; k < domain.facets.length; k++) {
			var facet = domain.facets[k];
			const score = scores[domain.domain][facet.facet] || {score: 0, count: 0};
			outputString += `        ${facet.facet}. ${facet.title}: ${score.score} / ${score.count * 5}\n`;
		}
	}

	return outputString;
}

// For a given question and answer to that question, 
// find the domain & facet that the question pertains to, and determine
// the score for the answer. The return value is a 3-item array [<domain>, <facet>, <score>].
function getScoreInfoForAnswer(question, answer) {
	// Search questionInfo for the question
	for (var i = 0; i < questionInfo.length; i++) {
		const info = questionInfo[i];
		if (info.text === question) {
			// Found the question! Now try to match the answer.
			for (var j = 0; j < info.choices.length; j++) {
				const choice = info.choices[j];
				if (choice.text === answer) {
					// We found the answer. Return our array of information.
					return [info.domain, info.facet, choice.score];
				}
			}
		}
	}
	// Question or answer not found. Return harmless data.
	return ['XXX', 1, 4];
}

// Analyzes the csv data and creates a report. The report is returned in the form of a string.
function createReport(csvData) {
	var outputString = "";

	// Split the input csv data into lines.
	const lines = csvData.split(/[\n\r]+/);

	// The first line of the csv data contains a list of all the questions.
	const firstLineTokens = lines[0].split(/,/);
	const questions = [];
	for (var k = 9; k < firstLineTokens.length; k++) {
		questions.push(firstLineTokens[k]);
	}

	// Each subsequent line of the csv represents one completed survey by one user. 
	// The first few tokens are misc metadata, including the user's email address.
	// The rest of the tokens are the responses to each question.
	for (var i = 1; i < lines.length; i++) {
		// It's a CSV file, so tokens are separated by commas.
		const tokens = lines[i].split(/,/);
		const emailAddress = tokens[5];

		if (emailAddress) {
			// If the line has an email address, compute that user's score.
			// We ignore lines that don't have an email address.

			// Loop over the answers to all the questions. For each answer,
			// we determine which domain/facet it relates to, then we add that 
			// answer's score into the total score for that domain/facet for that user.
			// This data is accumulated in the 'scores' data structure which looks like this:
			// {
			//		domain1: {facet1: {score: xxx, count, xxx}, facet2: ...}, 
			//		domain2: ...
			//	}
			const scores = {};		

			for (var j = 9; j < tokens.length; j++) {
				const answer = tokens[j];
				const question = questions[j - 9];
				const [domain, facet, score] = getScoreInfoForAnswer(question, answer);

				// Find the scores for this domain. If it doesn't yet exist, create it.
				var facetScores = scores[domain];
				if (!facetScores) {
					facetScores = {};
					scores[domain] = facetScores;
				}

				// Find the score for this facet. If it doesn't yet exist, create it.
				var facetScore = facetScores[facet];
				if (!facetScore) {
					facetScore = {score: 0, count: 0};
					facetScores[facet] = facetScore;
				}

				// Aggregate this answer's score into the facet's score.
				facetScore.count += 1;
				facetScore.score += score;
			}

			// The aggregated data is complete. Generate a report for this user.
			outputString += createOneReport(emailAddress, scores);
		}
	}

	return outputString;
}


// Here's the main program. This is the only code that deals with the outside world (file system, user interaction, ...)
const readline = require('readline-sync');
const fs = require('fs');
const path = require('path');
const os = require('os');

const instructions = `
This app analyzes user responses to the 
SurveyMonkey survey "Johnson 120 IPIP-NEO-PI-R". 
The result is a report that gives each user's 
score for the Big 5 personality traits and the 30 facets.

To get the data:
- log in to https://www.surveymonkey.com
- go to the "Johnson 120 IPIP-NEO-PI-R" project
- go to Analyze Results
- do Save As > Export File > All individual responses
- select File Format XLS
- do Export
- when it says Your export is complete, click Download
- in Finder, go to the Downloads folder
- locate the file you just downloaded, something like Data_All_190503.zip
- double click the downloaded file to unzip it
- open the resulting folder, something like Data_All_190503
- open the CSV folder
- drag the file "Johnson 120 IPIP-NEO-PI-R.csv" to this window
- click in this window, then press Return
`;

function main() {
	// Fun with console colors. For more, see https://stackoverflow.com/questions/9781218/how-to-change-node-jss-console-font-color.
	// We color our messages so that they stand out from all the spam the appears in the console window
	// of the standalone app created by pkg.
	const reset = "\x1b[0m";
	const highlight = "\x1b[36m";
	const highlight2 = "\x1b[32m"

	console.log(highlight + '--- Scorer for Johnson 120 IPIP-NEO-PI-R survey results ---\n' + instructions + reset);

	// Find the path we're reading from. It might be a command-line parameter, or we might have to prompt for it.
	var csvPath;
	if (process.argv.length === 3) {
		csvPath = process.argv[2];
	} else {
		csvPath = readline.question(highlight + "Please enter location of csv file:" + reset);
		// remove any extra backslash characters that are added into the path string when a user drags a file from finder to consolewindow.
		csvPath = csvPath.split("\\").join(""); 
	}

	// Now the action begins ... 

	// First, read the data file
	fs.readFile(csvPath, 'utf8', function (err, csvData) {
		if (err) throw err;

		// Second, create the report
		const report = createReport(csvData);

		// Third, write the report to the output file
		const outputPath = path.join(os.homedir(), 'Desktop', 'IPIP-scores.txt')
		fs.writeFile(outputPath, report, (err) => {
	  		if (err) {
				console.log(highlight2 + err + reset);
	  		} else {
				console.log(highlight2 + `\nReport written to ${outputPath}\n` + reset);
	  		}
		});
	});
}

main();


