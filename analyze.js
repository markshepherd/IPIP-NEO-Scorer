#!/usr/bin/env node
'use strict';

const { getItems } = require('@alheimsins/b5-johnson-120-ipip-neo-pi-r');

// const choices = require(`@alheimsins/b5-johnson-120-ipip-neo-pi-r/data/en/choices`)
// pkg doesn't handle the above require(), so we'll just do brute force
const choices = ['Very Inaccurate', 'Moderately Inaccurate', 'Neither Accurate Nor Inaccurate', 'Moderately Accurate', 'Very Accurate'];

// questionInfo contains information about each question:
// - what domain and facet the question is associated with
// - what score is assigned to each possible answer
const questionInfo = getItems('en');

// returns true if consistent, false if inconsistent
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
			// Answer not found
			return [info.domain, info.facet, -1];
		}
	}
	// Question not found.
	return [null, null, null];
}

// For a given answer, find out it's index, where "Very Inaccurate" is 1, "Moderately Inaccurate" is 2, and so on.
function getAnswerIndex(answer) {
	for (let i = 0; i < choices.length; i++) {
		if (choices[i] === answer) {
			return i;
		}
	}
	return -1;
}

// Create a schematic image of all the answers so a user can see illegal patterns in the answers. The image
// is in the form of an ASCII-art character string.
function makeAnswerImage(answers) {
	const height = 15;
	const image = Array(height).fill("");
	let nextAnswerIndex = 0;

	for (;;) {
		for (let i = 0; i < height; i++) {	
			const index = getAnswerIndex(answers[nextAnswerIndex++]);
			image[i] += "   " + ((index < 0) ? '.....' : (".".repeat(index) + "X" + ".".repeat(4 - index)));

			if (nextAnswerIndex >= answers.length) {
				return image.join('\n');
			}
		}
	}
}

// Parse the input data and put it into a usable format.
//
// Input: csvData
//
// Output: info extracted from csv data, in the form:
//  {
//		questions: [question1, question2, ...], 
//		answers: {
//			user1: {time: xxx, elapsedSeconds: nnn, answers: [answer1, answer2, ...]}, 
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
	const questionColumns = [];
	for (let k = 9; k < firstLineTokens.length; k++) {
		if (firstLineTokens[k] !== '') {
			// We're only interested in columns that have a non-null question.
			questions.push(firstLineTokens[k]);
			questionColumns.push(k);
		}
	}

	// Each subsequent line of the csv represents one completed survey by one user. 
	// The first few tokens are misc metadata, including the user's email address.
	// The rest of the tokens are the responses to each question.
	for (let i = 1; i < lines.length; i++) {
		// It's a CSV file, so tokens are separated by commas.
		const tokens = lines[i].split(/,/);
		let emailAddress = tokens[5];
		const startTime = Date.parse(tokens[2]);
		const endTime = Date.parse(tokens[3]);
		const elapsedSeconds = (endTime - startTime) / 1000;
		
		if (emailAddress) {
			const answersForThisUser = [];
			for (let column of questionColumns) {
				answersForThisUser.push(tokens[column]);
			}
			if (answers[emailAddress]) {
				// we already have data for this email address
				// make up a new unique key for this data
				emailAddress = emailAddress + '-' + startTime;
			}
			answers[emailAddress] = {time: startTime, elapsedSeconds: elapsedSeconds, answers: answersForThisUser};
		}
	}

	return {questions, answers};
}

// Compute the domain and facet scores based on the input data.
//
// Input: question/answer info from extractQuestionsAndAnswers()
//
// Output: for each user, the aggregated score for each domain and facet, in the form
// {
//     email1: {
//         time: time,
//         missingAnswers: number,
//         image: string,
//         suspiciousDuration: number,
//         scores: {
//             domain1: {
//                score: {score, count},
//                facets: {
//                  facet1: {score: <score>, count: <count>, scores: [], inconsistency: xxxx},
//                  facet2: {...},
//                  ...
//                }
//             },
//             domain2: { 
//                score: ....,
//                facets: ....
//             }
//          },
//      },
//      email2: { ... }
//      ...
// }
// where <score> is the total score across all questions for the given domain+facet
// and <count> is the number of answered questions associated with the given domain+facet
//
function aggregate(info) {
	const allScores = {};

	for (let emailAddress in info.answers) {
		if (info.answers.hasOwnProperty(emailAddress)) {
			const answersForThisUser = info.answers[emailAddress].answers;
			const dataForThisUser = {sex: 'Male', age: 63, scores: {}};		

			// Loop over the answers to all the questions. For each answer,
			// we determine which domain/facet it relates to, then we add that 
			// answer's score into the total score for that domain/facet for that user.
			for (let i = 0; i < answersForThisUser.length; i++) {
				const answer = answersForThisUser[i];
				const question = info.questions[i];
				let [domain, facet, score] = getScoreInfoForAnswer(question, answer);

				if (domain && facet && score) {
					// Find the scores for this domain. If it doesn't yet exist, create it.
					let facetScores = dataForThisUser.scores[domain];
					if (!facetScores) {
						facetScores = {score: {score: 0, count: 0}, facets: {}};
						dataForThisUser.scores[domain] = facetScores;
					}

					// Find the score for this facet. If it doesn't yet exist, create it.
					let facetScore = facetScores.facets[facet];
					if (!facetScore) {
						facetScore = {score: 0, count: 0, scores: []};
						facetScores.facets[facet] = facetScore;
					}

					// Aggregate this answer's score into the facet's score.
					facetScore.count += 1;
					if (score <= 0) {
						score = 3;
						facetScore.missing = (facetScore.missing || 0) + 1;
					}
					facetScore.score += score;
					facetScore.scores.push(score);
				}
			}

			allScores[emailAddress] = dataForThisUser;
		}
	}

	return allScores;
}

// "men over 60 years of age");
const norm = [
0,58.42,79.73,79.78,90.20,95.31,15.48,13.63,12.21,11.73,11.99,
9.81,11.46,8.18,11.08,9.91,8.24,3.54,4.31,3.59,3.82,3.36,3.28,
14.55,11.19,15.29,12.81,11.03,15.02,3.47,3.58,3.10,3.25,2.88,3.16,
14.06,14.22,14.34,12.42,14.61,10.11,3.13,3.64,2.90,3.20,3.89,4.02,
13.96,17.74,15.76,16.18,11.87,14.00,3.13,2.39,2.74,3.41,3.50,3.11,
16.32,14.41,17.54,16.65,14.98,15.18,2.31,4.49,2.30,2.68,2.76,3.61
];

const map1 = {
	'N': 1,
	'E': 2,
	'O': 3,
	'A': 4,
	'C': 5
};
const map2 = {
	'N': 10,
	'E': 22,
	'O': 34,
	'A': 46,
	'C': 58
};

function normalizeScore(score, index1, index2) {
	score.normalizedScore = (10 * (score.score - norm[index1])/norm[index2]) + 50;

    if (score.normalizedScore < 45) {
      score.rating = "low"; 
	} else if (score.normalizedScore > 55) {
      score.rating = "high"; 
	} else {
      score.rating = "average"; 
	}

	if (score.normalizedScore < 27) {
		score.percentileScore = 1;
	} else if (score.normalizedScore > 73) {
		score.percentileScore = 99;
	} else {
		const s = score.normalizedScore;
		score.percentileScore = Math.trunc(210.335958661391 - (16.7379362643389 * s)
			+ (0.405936512733332 * (s * s)) - (0.00270624341822222 * (s * s * s)));
	}
}

// Derive various interesting information from the domain & facet scores and input data. Add the info into the allScores data structure.
//
// Input: aggregated scores, from aggregate()
// 
// Output: various items added to allScores
// - results of checks for missing answers, suspicious duration, and answer consistency
// - a schematic image of all the answers so a user can see illegal patterns in the answers.
// - score totals for each domain
function analyze(allScores, info) {
	for (let emailAddress in allScores) {
		if (allScores.hasOwnProperty(emailAddress)) {
			let missingCount = 0;
			const userData = allScores[emailAddress];
			const scores = userData.scores;

			for (let domain in scores) {
				if (scores.hasOwnProperty(domain)) {
					const facets = scores[domain].facets;

					let totalScore = 0;
					let totalCount = 0;

					for (let facet in facets) {
						if (facets.hasOwnProperty(facet)) {
							const facetScore = facets[facet];
							totalScore += facetScore.score;
							totalCount += facetScore.count;
							missingCount += facetScore.missing || 0;
							facetScore.inconsistency = calcConsistency(facetScore.scores);
						}
					}
					scores[domain].score = {score: totalScore, count: totalCount};
					normalizeScore(scores[domain].score, map1[domain], map1[domain] + 5);
					for (let facet = 1; facet <= 6; facet++) {
						const facetScore = scores[domain].facets[facet];
						if (facetScore) {
							normalizeScore(facetScore, facet + map2[domain], facet + map2[domain] + 6);
						}
					}
				}
			}
			userData.missingAnswers = missingCount; // info.questions.length - answerCount;
			userData.image = makeAnswerImage(info.answers[emailAddress].answers);
			// console.log(`elapsedSeconds = ${info.answers[emailAddress].elapsedSeconds}`);
			if (info.answers[emailAddress].elapsedSeconds < 300) {
				userData.suspiciousDuration = info.answers[emailAddress].elapsedSeconds;
			}
			userData.time = info.answers[emailAddress].time;
		}
	}
}

// Analyze the answers and return a summary report.
function analyzeCSV(csvData) {
	const info = extractQuestionsAndAnswers(csvData);

	const allScores = aggregate(info);

	analyze(allScores, info);

	return allScores;
}

module.exports = analyzeCSV;

