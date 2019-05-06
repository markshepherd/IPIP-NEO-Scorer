#!/usr/bin/env node
'use strict';

const { getItems } = require('@alheimsins/b5-johnson-120-ipip-neo-pi-r');
const { getTemplate } = require('@alheimsins/b5-result-text');
// const choices = require(`@alheimsins/b5-johnson-120-ipip-neo-pi-r/data/en/choices`)

// questionInfo contains information about each question:
// - what domain and facet the question is associated with
// - what score is assigned to each possible answer
const questionInfo = getItems('en');

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
	return (lowCount === 2 && highCount === 2) ? 'bad' : 'minor';
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

function getAnswerIndex(answer) {
	const choices = ['Very Inaccurate', 'Moderately Inaccurate', 'Neither Accurate Nor Inaccurate', 'Moderately Accurate', 'Very Accurate'];
	for (let i = 0; i < choices.length; i++) {
		if (choices[i] === answer) {
			return i;
		}
	}
	return -1;
}

/*
function getAnswerIndex(answer) {
	for (let i = 0; i < choices.plus.length; i++) {
		let choice = choices.plus[i];
		if (choice.text === answer) {
			return i;
		}
	}
	return -1;
}
*/

function makeAnswerImage(answers) {
	const height = 15;
	let image = [];
	for (let i = 0; i < height; i++) {
		image.push('');
	}

	let nextAnswerIndex = 0;

	/* eslint-disable-next-line no-constant-condition */
	while (true) {
		for (let i = 0; i < height; i++) {	
			const index = getAnswerIndex(answers[nextAnswerIndex++]);
			image[i] += "   " + ((index < 0) ? '.....' : (".".repeat(index) + "X" + ".".repeat(4 - index)));

			if (nextAnswerIndex >= answers.length) {
				return image.join('\n');
			}
		}
	}
}


// Input: csvData
//
// Output: info extracted from csv data, in the form:
//  {
//		questions: [question1, question2, ...], 
//		answers: {
//			user1: {elapsedSeconds: nnn, answers: [answer1, answer2, ...]}, 
//			user2: etc...
//		}
//	}
//
// We only extract data for users for which there is an email address.
function extractQuestionsAndAnswers(csvData) {
	const questions = [];
	const answers = {};

	// Split the input csv data into lines.
	const lines = csvData.split(/[\n\r]+/);

	// The first line of the csv data contains a list of all the questions.
	const firstLineTokens = lines[0].split(/,/);
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
		const startTime = Date.parse(tokens[2]);
		const endTime = Date.parse(tokens[3]);
		const elapsedSeconds = (endTime - startTime) / 1000;
		
		if (emailAddress) {
			const answersForThisUser = [];
			for (let j = 9; j < tokens.length; j++) {
				answersForThisUser.push(tokens[j]);
			}
			answers[emailAddress] = {elapsedSeconds: elapsedSeconds, answers: answersForThisUser};
		}
	}

	return {questions, answers};
}

// Input: question/answer info from extractQuestionsAndAnswers()
//
// Output: for each user, the aggregated score for each domain and facet, in the form
// {
//     email1: {
//         domain1: {
//            facet1: {score: <score>, count: <count>, scores: [], inconsistency: xxxx},
//            facet2: {...},
//            ...},
//         domain2: { 
//            facet1: { ... },
//            ...
//		},
//		email2: { ... }
//		...
//   }
// where <score> is the total score across all questions for the given domain+facet
// and <count> is the number of answered questions associated with the given domain+facet
//
function aggregate(info) {
	const allScores = [];

	for (let emailAddress in info.answers) {
		if (info.answers.hasOwnProperty(emailAddress)) {
			const answersForThisUser = info.answers[emailAddress].answers;
			const scoresForThisUser = {};		

			// Loop over the answers to all the questions. For each answer,
			// we determine which domain/facet it relates to, then we add that 
			// answer's score into the total score for that domain/facet for that user.
			for (let i = 0; i < answersForThisUser.length; i++) {
				const answer = answersForThisUser[i];
				const question = info.questions[i];
				const [domain, facet, score] = getScoreInfoForAnswer(question, answer);

				if (domain && facet && score) {
					// Find the scores for this domain. If it doesn't yet exist, create it.
					let facetScores = scoresForThisUser[domain];
					if (!facetScores) {
						facetScores = {};
						scoresForThisUser[domain] = facetScores;
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

			allScores[emailAddress] = scoresForThisUser;
		}
	}

	return allScores;
}

// Input: aggregated scores, from aggregate()
// 
// Output:
// - inconsistency field for every facet is added to allScores 
// - per-domain annotation containing score and count
//
function analyze(allScores, info) {
	const annotations = {};
	for (let emailAddress in allScores) {
		if (allScores.hasOwnProperty(emailAddress)) {
			let answerCount = 0;
			const annotationsForThisUser = {};
			const scores = allScores[emailAddress];

			for (let domain in scores) {
				if (scores.hasOwnProperty(domain)) {
					const facets = scores[domain];

					let totalScore = 0;
					let totalCount = 0;

					for (let facet in facets) {
						if (facets.hasOwnProperty(facet)) {
							const facetScore = facets[facet];
							totalScore += facetScore.score;
							totalCount += facetScore.count;
							answerCount += facetScore.count;
							facetScore.inconsistency = calcConsistency(facetScore.scores);
						}
					}
					annotationsForThisUser[domain] = {score: totalScore, count: totalCount};
				}
			}
			annotationsForThisUser.missingAnswers = info.questions.length - answerCount;
			annotationsForThisUser.image = makeAnswerImage(info.answers[emailAddress].answers);
			// console.log(`elapsedSeconds = ${info.answers[emailAddress].elapsedSeconds}`);
			if (info.answers[emailAddress].elapsedSeconds < 300) {
				annotationsForThisUser.suspiciousDuration = info.answers[emailAddress].elapsedSeconds;
			}
			annotations[emailAddress] = annotationsForThisUser;
		}
	}

	return annotations;
}

// Create a summary report of scores and warning for all users. The report is in the form of a character string.
function summaryReport(allScores, annotations) {
	let outputString = "";

	for (let emailAddress in allScores) {
		if (allScores.hasOwnProperty(emailAddress)) {
			const annotationsForThisUser = annotations[emailAddress];
			const scoresForThisUser = allScores[emailAddress];
			let userComments = (annotationsForThisUser.missingAnswers > 0) ? `       *** ${annotationsForThisUser.missingAnswers} missing answers` : '';
			userComments += annotationsForThisUser.suspiciousDuration ? `       *** Completed too quickly - ${annotationsForThisUser.suspiciousDuration} seconds.` : '';
			outputString += `\n\n\n${emailAddress} ${userComments}\n\n${annotationsForThisUser.image}\n`;

			// Fetch the template which contains a list of all the domains and facets, including their human-readable names. 
			// The order of items in the template defines the order of the report.
			const template = getTemplate();

			// Iterate over the domains in the template
			for (let i = 0; i < template.length; i++) {
				const domain = template[i];
				const domainScore = annotationsForThisUser[domain.domain] || {score: 0, count: 0};
				const facetScores = scoresForThisUser[domain.domain] || {};

				// Print the domain summary line
				outputString += `\n    ${domain.domain}. ${domain.title}: ${domainScore.score} / ${domainScore.count * 5}\n`;

				// Iterate over facets and print a line for each facet.
				for (let k = 0; k < domain.facets.length; k++) {
					const facet = domain.facets[k];
					const facetScore = facetScores[facet.facet] || {score: 0, count: 0, scores: [], inconsistency: 'none'};
					const scoreString = facetScore.inconsistency !== 'none' 
						? `*** ${facetScore.inconsistency} inconsistency; scores are ${facetScore.scores}` : '';
					outputString += 
						`        ${facet.facet}. ${facet.title}: ${facetScore.score} / ${facetScore.count * 5}        ${scoreString}\n`;
				}
			}
		}
	}
	return outputString;
}

function analyzeAndReport(csvData) {
	const info = extractQuestionsAndAnswers(csvData);

	const allScores = aggregate(info);

	const annotations = analyze(allScores, info);

	const report = summaryReport(allScores, annotations);

	return report;
}

module.exports = analyzeAndReport;

