#!/usr/bin/env node
'use strict';

const { getItems } = require('@alheimsins/b5-johnson-120-ipip-neo-pi-r');
const { getTemplate } = require('@alheimsins/b5-result-text');

// const choices = require(`@alheimsins/b5-johnson-120-ipip-neo-pi-r/data/en/choices`)

// questionInfo contains information about each question:
// - what domain and facet the question is associated with
// - what score is assigned to each possible answer
const questionInfo = getItems('en');
// const info = getInfo();
// debugger;

// function calcVariance(arrayOfNumbers) {
// 	if (arrayOfNumbers.length <= 1) {
// 		return 0;
// 	}
// 	let sum = 0;
// 	for (let i = 0; i < arrayOfNumbers.length; i++) {
// 		sum += arrayOfNumbers[i];
// 	}
// 	const mean = sum / arrayOfNumbers.length;
// 	let sumOfSquares = 0;
// 	for (let j = 0; j < arrayOfNumbers.length; j++) {
// 		const diff = arrayOfNumbers[j] - mean;
// 		sumOfSquares += diff * diff;
// 	}
// 	const variance = sumOfSquares / arrayOfNumbers.length;
// 	const standardDeviation = Math.sqrt(variance);

// 	return {mean, variance, standardDeviation};
// }

// function calcSpread(arrayOfNumbers) {
// 	let low = 999;
// 	let high = -999;
// 	for (let number of arrayOfNumbers) {
// 		if (number < low) low = number;
// 		if (number > high) high = number;
// 	}
// 	return high - low;
// }

// returns Boolean, true if consistent, false if inconsistent
// todo: generalize this so it works for any survey, not just johnson 120.
function calcConsistency(arrayOfNumbers) {
	const mid = 3;
	// const 
	let lowCount = 0;
	let highCount = 0;
	for (let number of arrayOfNumbers) {
		if (number < mid) lowCount++;
		if (number > mid) highCount++;
	}
	if (lowCount === 0 || highCount === 0) return 'none';
	return (lowCount === 2 && highCount === 2) ? 'bad' : 'some';
}

// Create a report for one completed survey by one user. The report is 
// returned in the form of a string.
//
// 'scores' is the user's aggregated score for all domains and facets, in the form
//   {
//      domain1: {
//		  facet1: {score: <num>, count: <num>},
//		  facet2: {...},``
//        ...
//      domain2: {
//	      ....
//   }
// 'score' is the total score across all questions for the given domain+facet
// and 'count' is the number of questions associated with the given domain+facet
//

function createOneReport(emailaddress, scores) {
	let outputString = "";

	outputString += `\n${emailaddress}\n`;

	// Fetch the template which contains a list of all the domains and facets, including their human-readable names. 
	// The order of items in the template defines the order of the report.
	const template = getTemplate();

	// Iterate over the domains in the template
	for (let i = 0; i < template.length; i++) {
		const domain = template[i];

		// Iterate over the facets of this domain. Accumulate the score and count
		// of each facet into a total score and count for this domain.
		let totalScore = 0;
		let totalCount = 0;
		for (let j = 0; j < domain.facets.length; j++) {
			const facet = domain.facets[j];

			// Grab the scores data for this domain+facet; just use zero if no data.
			const facetScore = scores[domain.domain] && scores[domain.domain][facet.facet] || {score: 0, count: 0};

			// Collect our information
			totalScore += facetScore.score;
			totalCount += facetScore.count;
		}

		// Print the domain summary line
		outputString += `\n    ${domain.domain}. ${domain.title}: ${totalScore} / ${totalCount * 5}\n`;

		// Iterate over facets and print a line for each facet.
		for (let k = 0; k < domain.facets.length; k++) {
			const facet = domain.facets[k];
			const facetScore = scores[domain.domain] && scores[domain.domain][facet.facet] || {score: 0, count: 0, scores: []};
			const inconsistency = calcConsistency(facetScore.scores);
			// const variance = calcVariance(facetScore.scores);
			// const spread = calcSpread(facetScore.scores);
			// const scoreString = JSON.stringify({scores: facetScore.scores, variance: variance.variance});
			// const scoreString = inconsistency !== 'none' ? `scores: ${facetScore.scores} variance: ${variance.variance} spread: ${spread} inconsistency: ${inconsistency}` : '';
			const scoreString = inconsistency !== 'none' ? `scores: ${facetScore.scores} inconsistency: ${inconsistency}` : '';
			// const scoreString = facetScore.scores.join(", ");
			// console.log(scoreString);
			// console.log(JSON.stringify({scoreString: scoreString, scores: facetScore.scores}, undefined, 2))
			outputString += `        ${facet.facet}. ${facet.title}: ${facetScore.score} / ${facetScore.count * 5}     ${scoreString}\n`;
		}
	}

	return outputString;
}

// For a given question and answer to that question, 
// find the domain & facet that the question pertains to, and determine
// the score for the answer. The return value is a 3-item array [<domain>, <facet>, <score>].
function getScoreInfoForAnswer(question, answer) {
	// Search questionInfo for the question
	for (let i = 0; i < questionInfo.length; i++) {
		const info = questionInfo[i];
		if (info.text === question) {
			// Found the question! Now try to match the answer.
			for (let j = 0; j < info.choices.length; j++) {
				const choice = info.choices[j];
				if (choice.text === answer) {
					// We found the answer. Return our array of information.
					return [info.domain, info.facet, choice.score];
				}
			}
		}
	}
	// Question or answer not found.
	return [null, null, null];
}

// Analyzes the csv data and creates a report. The report is returned in the form of a string.
function createReport(csvData) {
	let outputString = "";

	// Split the input csv data into lines.
	const lines = csvData.split(/[\n\r]+/);

	// The first line of the csv data contains a list of all the questions.
	const firstLineTokens = lines[0].split(/,/);
	const questions = [];
	for (let k = 9; k < firstLineTokens.length; k++) {
		questions.push(firstLineTokens[k]);
	}

	// Each subsequent line of the csv represents one completed survey by one user. 
	// The first few tokens are misc metadata, including the user's email address.
	// The rest of the tokens are the responses to each question.
	for (let i = 1; i < lines.length; i++) {
		// It's a CSV file, so tokens are separated by commas.
		const tokens = lines[i].split(/,/);
		const emailAddress = tokens[5];

		if (emailAddress) {
			// If the line has an email address, compute that user's score.
			// We ignore lines that don't have an email address.

			// Here is where the "data analysis" happens.
			// 	input: array of {question, answer}
			//  result: {score, count} for each facet of each domain
			// 
			// Loop over the answers to all the questions. For each answer,
			// we determine which domain/facet it relates to, then we add that 
			// answer's score into the total score for that domain/facet for that user.
			// This data is accumulated in the 'scores' data structure which looks like this:
			// {
			//		domain1: {facet1: {score: xxx, count, xxx}, facet2: ...}, 
			//		domain2: ...
			//	}
			const scores = {};		

			for (let j = 9; j < tokens.length; j++) {
				const answer = tokens[j];
				const question = questions[j - 9];
				const [domain, facet, score] = getScoreInfoForAnswer(question, answer);

				if (domain && facet && score) {
					// Find the scores for this domain. If it doesn't yet exist, create it.
					let facetScores = scores[domain];
					if (!facetScores) {
						facetScores = {};
						scores[domain] = facetScores;
					}

					// Find the score for this facet. If it doesn't yet exist, create it.
					let facetScore = facetScores[facet];
					if (!facetScore) {
						facetScore = {score: 0, count: 0, scores: []};
						facetScores[facet] = facetScore;
					}

					// Aggregate this answer's score into the facet's score.
					facetScore.count += 1;
					facetScore.score += score;
					facetScore.scores.push(score);
				}
			}

			// The analysis is complete. The aggregated data for this user is in 'scores'. Generate a report.
			outputString += createOneReport(emailAddress, scores);
		}
	}

	return outputString;
}

module.exports = createReport;
