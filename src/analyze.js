#!/usr/bin/env node


const normalizeScore = require("./normalize");
const {getItems} = require("@alheimsins/b5-johnson-120-ipip-neo-pi-r");

// const choices = require(`@alheimsins/b5-johnson-120-ipip-neo-pi-r/data/en/choices`)
// Pkg doesn't handle the above require(), so we'll just do brute force
const choices = ["Very Inaccurate", "Moderately Inaccurate", "Neither Accurate Nor Inaccurate", "Moderately Accurate", "Very Accurate"];

// QuestionInfo contains information about each question:
// - what domain and facet the question is associated with
// - what score is assigned to each possible answer
const questionInfo = getItems("en");

// Returns true if consistent, false if inconsistent
// Someday, we should generalize this so it works for any survey, not just johnson 120.
function calcConsistency(arrayOfNumbers) {
	const mid = 3;
	let lowCount = 0;
	let highCount = 0;
	for (let number of arrayOfNumbers) {
		if (number < mid) lowCount++;
		if (number > mid) highCount++;
	}
	if (lowCount === 0 || highCount === 0) return "none";
	return (lowCount === 2 && highCount === 2) ? "bad" : "minor";
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
			image[i] += "   " + ((index < 0) ? "....." : (".".repeat(index) + "X" + ".".repeat(4 - index)));

			if (nextAnswerIndex >= answers.length) {
				return image.join("\n");
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

	// The first line of the csv data contains the name of each column.
	// The first few columns of each line are metadata, including the user's email address.
	// The rest of the tokens are the responses to each question.
	const columnNames = lines[0].split(/,/);
	const emailIndex = columnNames.indexOf("Email Address");
	const startTimeIndex = columnNames.indexOf("Start Date");
	const endTimeIndex = columnNames.indexOf("End Date");
	const ageIndex = columnNames.indexOf("Age");
	const sexIndex = columnNames.indexOf("Sex");
	const firstQuestionIndex = columnNames.indexOf("Worry about things");

	// Make a list of questions, and a list of what columns contain answers to questions.
	const questionColumns = [];
	for (let k = firstQuestionIndex; k < columnNames.length; k++) {
		if (columnNames[k] !== "") {
			// We're only interested in columns that have a non-null question.
			questions.push(columnNames[k]);
			questionColumns.push(k);
		}
	}

	// Each subsequent line of the csv represents one completed survey by one user. 
	for (let i = 1; i < lines.length; i++) {
		// It's a CSV file, so tokens are separated by commas.
		const tokens = lines[i].split(/,/);
		let emailAddress = tokens[emailIndex];
		if (emailAddress) {
			const startTime = Date.parse(tokens[startTimeIndex]);

			// Make a list of this user's answers.
			const answersForThisUser = [];
			for (let column of questionColumns) {
				answersForThisUser.push(tokens[column]);
			}

			// Record this user's data into 'answers'.
			if (answers[emailAddress]) {
				// We already have data for this email address.
				// Make up a new unique key for this data.
				emailAddress = emailAddress + "-" + startTime;
			}
			answers[emailAddress] = {
				age: tokens[ageIndex], 
				sex: tokens[sexIndex], 
				time: startTime, 
				elapsedSeconds: (Date.parse(tokens[endTimeIndex]) - startTime) / 1000, 
				answers: answersForThisUser
			};
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
// Where <score> is the total score across all questions for the given domain+facet
// And <count> is the number of answered questions associated with the given domain+facet
//
function aggregate(info) {
	const allScores = {};

	for (let emailAddress in info.answers) {
		if (info.answers.hasOwnProperty(emailAddress)) {
			const answersForThisUser = info.answers[emailAddress].answers;
			const dataForThisUser = {scores: {}};		

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
			const answerInfo = info.answers[emailAddress];
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
					normalizeScore(answerInfo.age, answerInfo.sex, scores[domain].score, domain, null);
					for (let facet = 1; facet <= 6; facet++) {
						const facetScore = scores[domain].facets[facet];
						if (facetScore) {
							normalizeScore(answerInfo.age, answerInfo.sex, facetScore, domain, facet);
						}
					}
				}
			}
			userData.missingAnswers = missingCount;
			userData.image = makeAnswerImage(answerInfo.answers);
			if (answerInfo.elapsedSeconds < 300) {
				userData.suspiciousDuration = answerInfo.elapsedSeconds;
			}
			userData.time = answerInfo.time;
			userData.age = answerInfo.age;
			userData.sex = answerInfo.sex;
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

