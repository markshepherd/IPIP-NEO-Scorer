#!/usr/bin/env node
'use strict';

var fs = require('fs');
const { getItems, getInfo } = require('@alheimsins/b5-johnson-120-ipip-neo-pi-r');
const { getTemplate } = require('@alheimsins/b5-result-text');

// questionInfo gives us information about each of the questions, 
// - what domain and facet the question is associated with
// - what score is assigned to each possible answer
const questionInfo = getItems('en');

// Outputs the final report for one completed survey by a given user.
//
// 'result' is in the form
//   {
//      domain1: {
//		  facet1: {score: <num>, count: <num>},
//		  facet2: {...},
//        ...
//      domain2: {
//	      ....
//   }
// where score is the total score across all questions for the given domain+facet
// and count is the number of questions associated with the given domain+facet
//
function printReport(emailaddress, result) {
	var outputString = "";

	outputString += `\n${emailaddress}\n`;

	// The template contains a list of all the domains and facets and their human-readable names. 
	// The order of items in the template defines the order of the report.
	const template = getTemplate();

	// Iterate over the domains in the template
	for (var i = 0; i < template.length; i++) {
		var domain = template[i];

		// Iterate over the facets of this domain, collecting total score and count.
		var totalScore = 0;
		var totalCount = 0;
		for (var j = 0; j < domain.facets.length; j++) {
			var facet = domain.facets[j];

			// Grab the result data for this domain+facet; just use zero if no data.
			const score = result[domain.domain][facet.facet] || {score: 0, count: 0};

			// Collect our information
			totalScore += score.score;
			totalCount += score.count;
		}

		// Print the domain summary line
		outputString += `\n    ${domain.domain}. ${domain.title}: ${totalScore} / ${totalCount * 5}\n`;

		// Iterate over facets and print a line for each one.
		for (var k = 0; k < domain.facets.length; k++) {
			var facet = domain.facets[k];
			const score = result[domain.domain][facet.facet] || {score: 0, count: 0};
			outputString += `        ${facet.facet}. ${facet.title}: ${score.score} / ${score.count * 5}\n`;
		}
	}

	return outputString;
}

// Given the text of a question and the text of an answer to that question,
// returns a 3-item array [<domain>, <facet>, <score>].
function decode(question, answer) {
	// Search questionInfo for the question
	for (var i = 0; i < questionInfo.length; i++) {
		const info = questionInfo[i];
		if (info.text === question) {
			// Found the question! Now try to matdh the answer.
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

// Process the csv data that comes from Survey Monkey > Analyze Results > Save As > Export File > All Rndividual Responses.
// We 
function doit(csvData) {
	var outputString = "";
	const lines = csvData.split(/[\n\r]+/);

	// the first line of the csv data contains a list of all the questions 
	const firstLineTokens = lines[0].split(/,/);
	const questions = [];
	for (var k = 9; k < firstLineTokens.length; k++) {
		questions.push(firstLineTokens[k]);
	}

	// Each line of the file represents one completed survey by one user. 
	// The first few tokens are misc metadata, including the user's email address.
	// The rest of the tokens are the responses to eadh question.
	for (var i = 1; i < lines.length; i++) {
		// It's a CSV file, so tokens are separated by commas.
		const tokens = lines[i].split(/,/);
		const emailAddress = tokens[5];

		if (emailAddress) {
			// If the line has an email address, compute that user's score.
			// result looks like -- {domain1: {facet1: score, facet2: score, ...}, domain2: ...}
			const result = {};		

			for (var j = 9; j < tokens.length; j++) {
				const answer = tokens[j];
				const question = questions[j - 9];
				const [domain, facet, score] = decode(question, answer);

				var facetScores = result[domain];
				if (!facetScores) {
					facetScores = {};
					result[domain] = facetScores;
				}

				var facetScore = facetScores[facet];
				if (!facetScore) {
					facetScore = {score: 0, count: 0};
					facetScores[facet] = facetScore;
				}

				facetScore.count += 1;
				facetScore.score += score;
			}

			outputString += printReport(emailAddress, result);
		}
	}

	return outputString;
}

var path;
if (process.argv.length === 3) {
	path = process.argv[2];
} else {
	const readline = require('readline-sync');
	path = readline.question("Please enter path to csv file:");
	path = path.split("\\").join("");
}

fs.readFile(path, 'utf8', function (err, csvData) {
	if (err) throw err;
	const report = doit(csvData);
	fs.writeFile("./IPIP-scores.txt", report, (err) => {
  		if (err) {
  			console.log('\x1b[36m%s\x1b[0m', err);
  		} else {
  			console.log('\x1b[36m%s\x1b[0m', `Report written to ${process.cwd()}/IPIP-scores.txt`);
  		}
	});
});


