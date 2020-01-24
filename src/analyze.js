#!/usr/bin/env node


const normalizeScore = require("./normalize");
const {getItems} = require("@alheimsins/b5-johnson-120-ipip-neo-pi-r");
const _ = require("lodash");

// const choices = require(`@alheimsins/b5-johnson-120-ipip-neo-pi-r/data/en/choices`)
// Pkg doesn't handle the above require(), so we'll just do brute force
const choices = ["Very Inaccurate", "Moderately Inaccurate", "Neither Accurate Nor Inaccurate", "Moderately Accurate", "Very Accurate"];

// QuestionInfo contains information about each question:
// - what domain and facet the question is associated with
// - what score is assigned to each possible answer
const questionInfo = getItems("en");

// Returns "none", "minor", or "bad" depending on inconsistent the set of scores is.
// Someday, we should generalize this so it works for any survey, not just johnson 120.
function calcConsistency (arrayOfNumbers) {
	const mid = 3;
	let lowCount = 0;
	let highCount = 0;
	for (const number of arrayOfNumbers) {
		if (number < mid) { lowCount++; }
		if (number > mid) { highCount++; }
	}
	if (lowCount === 0 || highCount === 0) { return "none"; }
	return lowCount === 2 && highCount === 2 ? "bad" : "minor";
}

// For a given question and answer to that question,
// find the domain & facet that the question pertains to, and determine
// the score for the answer. The return value is a 3-item array [<domain>, <facet>, <score>].
function getScoreInfoForAnswer (question, answer) {
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
			if (answer !== "") {
				// eslint-disable-next-line no-console
				console.log(`Unrecognized answer '${answer}' for question '${question}'`);
			}
			return [info.domain, info.facet, -1];
		}
	}
	// Question not found.
	// eslint-disable-next-line no-console
	console.log(`Unrecognized question '${question}'`);
	return [null, null, null];
}

// For a given answer, find out it's index, where "Very Inaccurate" is 1, "Moderately Inaccurate" is 2, and so on.
function getAnswerIndex (answer) {
	for (let i = 0; i < choices.length; i++) {
		if (choices[i] === answer) {
			return i;
		}
	}
	return -1;
}

// Create a schematic image of all the answers so a user can see illegal patterns in the answers. The image
// is in the form of an ASCII-art character string.
function makeAnswerImage (answers) {
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

// Given a character string in the form 'mmyy' which represents somebody's birth date, return the
// person's age as of 2020. Validate the input date and complain to the console if it's not valid.
function findAge (mmyy) {
	// find the 2 numbers 'mm' and 'yy'
	const matchResult = (mmyy || "").toString().match(/^(?<mm>\d{1,2})(?<yy>\d{2})$/u);
	if (!matchResult) {
		// eslint-disable-next-line no-console
		console.log(`findAge failed, mmyy '${mmyy}' is not 3 or 4 digits.`);
		return null;
	}
	
	// convert the string to an integer and calculate the birth year.
	let year = parseInt(matchResult.groups.yy, 10);
	if (year < 20) {
		year += 2000;
	} else {
		year += 1900;
	}
	
	// calculate the age as of 2020
	return 2020 - year;
}

// Determine a user's UserID. Validate the input date and complain to the console if it's not valid.
// @param firstTwoLetters the user's response to the "first two letters" question
// @param mmyy the user's response to the "4-digit birthdate" question
// @return <string> the user's unique(ish) UserID 
function makeUserId (firstTwoLetters, mmyy) {
	const firstTwoLettersString = (firstTwoLetters || "").toString().toLowerCase().trim();
	let mmyyString = (mmyy || "").toString().trim();
	if (firstTwoLettersString.length === 0) {
		return null;
	}

	if (!firstTwoLettersString.match(/^[a-z][a-z]$/u)) {
		// eslint-disable-next-line no-console
		console.log(`makeUserId failed, firstTwoLetters '${firstTwoLetters}' is not 2 letters.`);
		return null;
	}

	if (mmyyString.match(/^\d\d\d$/u)) {
		mmyyString = `0${mmyyString}`;
	}
	if (!mmyyString.match(/^\d\d\d\d$/u)) {
		// eslint-disable-next-line no-console
		console.log(`makeUserId failed, mmyy '${mmyy}' is not 3 or 4 digits.`);
		return null;
	}

	const result = `${firstTwoLettersString}${mmyyString}`;
	// eslint-disable-next-line no-console
	// console.log(`makeUserId firstTwoLetters: '${firstTwoLetters}', mmyy: '${mmyy}', result: '${result}'`);
	return result;
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
// We only extract data for users who have a user ID
function extractQuestionsAndAnswers (csvData) {
	const questions = [];
	const answers = {};

	// Split the input csv data into lines.
	const lines = csvData.split(/[\n\r]+/u);

	// The first line of the csv data contains the name of each column.
	// The first few columns of each line are metadata.
	// The rest of the tokens are the responses to each question.
	const columnNames = lines[0].split(/,/u);
	const mmyyIndex = _.findIndex(columnNames, (n) => n.match(/Please enter four digits/u));
	const firstTwoLettersIndex = _.findIndex(columnNames, (n) => n.match(/This question will allow us/u));
	const startTimeIndex = columnNames.indexOf("Start Date");
	const endTimeIndex = columnNames.indexOf("End Date");
	const sexIndex = columnNames.indexOf("What is your gender?");
	const firstQuestionIndex = columnNames.indexOf("Worry about things");

	// Make a list of questions, and a list of what columns contain answers to questions.
	const questionColumns = [];
	for (let k = firstQuestionIndex; (k < columnNames.length) && (questions.length < questionInfo.length); k++) {
		if (columnNames[k] !== "") {
			// We're only interested in columns that have a non-null question.
			questions.push(columnNames[k]);
			questionColumns.push(k);
		}
	}

	if (questions.length !== questionInfo.length) {
		// eslint-disable-next-line no-console
		console.log(`Expected ${questionInfo.length} personality questions but found ${questions.length}.`);
	}

	// Each line of the csv, starting from the 3rd line, represents one completed survey by one user.
	let numberWithUserId = 0;
	let numberWithoutUserId = 0;

	for (let i = 2; i < lines.length; i++) {
		// It's a CSV file, so tokens are separated by commas.
		const tokens = lines[i].split(/,/u);
		const userId = makeUserId(tokens[firstTwoLettersIndex], tokens[mmyyIndex]);
		if (userId) {
			const startTime = Date.parse(tokens[startTimeIndex]);

			// Make a list of this user's answers.
			const answersForThisUser = [];
			for (const column of questionColumns) {
				answersForThisUser.push(tokens[column]);
			}

			// Record this user's data into 'answers'.
			if (answers[userId]) {
				// We already have data for this userId
				// eslint-disable-next-line no-console
				console.log(`*** More than one record for User ID ${userId}. Ignoring all but first.`);
			} else {
				answers[userId] = {
					age: findAge(tokens[mmyyIndex]),
					sex: tokens[sexIndex],
					time: startTime,
					elapsedSeconds: (Date.parse(tokens[endTimeIndex]) - startTime) / 1000,
					answers: answersForThisUser
				};
				numberWithUserId += 1;
			}
		} else {
			numberWithoutUserId += 1;
		}
	}

	// eslint-disable-next-line no-console
	console.log(`${numberWithUserId} responses had a valid user id. ${numberWithoutUserId} did not.`);

	return {questions, answers};
}

// Compute the domain and facet scores based on the input data.
//
// Input: question/answer info from extractQuestionsAndAnswers()
//
// Output: for each user, the aggregated score for each domain and facet, in the form
// {
//     userId1: {
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
//      userId2: { ... }
//      ...
// }
// Where <score> is the total score across all questions for the given domain+facet
// And <count> is the number of answered questions associated with the given domain+facet
//
function aggregate (info) {
	const allScores = {};

	for (const userId in info.answers) {
		if (info.answers.hasOwnProperty(userId)) {
			const answersForThisUser = info.answers[userId].answers;
			const dataForThisUser = {scores: {}};

			// Loop over the answers to all the questions. For each answer,
			// we determine which domain/facet it relates to, then we add that
			// answer's score into the total score for that domain/facet for that user.
			for (let i = 0; i < answersForThisUser.length; i++) {
				const answer = answersForThisUser[i];
				const question = info.questions[i];
				const [domain, facet, score] = getScoreInfoForAnswer(question, answer);

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
					let s = score;
					if (score <= 0) {
						s = 3;
						facetScore.missing = (facetScore.missing || 0) + 1;
					}
					facetScore.score += s;
					facetScore.scores.push(s);
				}
			}

			allScores[userId] = dataForThisUser;
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
function analyze (allScores, info) {
	for (const userId in allScores) {
		if (allScores.hasOwnProperty(userId)) {
			let missingCount = 0;
			const userData = allScores[userId];
			const answerInfo = info.answers[userId];
			const scores = userData.scores;
			userData.inconsistencies = {none: 0, minor: 0, bad: 0};

			for (const domain in scores) {
				if (scores.hasOwnProperty(domain)) {
					const facets = scores[domain].facets;

					let totalScore = 0;
					let totalCount = 0;

					for (const facet in facets) {
						if (facets.hasOwnProperty(facet)) {
							const facetScore = facets[facet];
							totalScore += facetScore.score;
							totalCount += facetScore.count;
							missingCount += facetScore.missing || 0;
							facetScore.inconsistency = calcConsistency(facetScore.scores);
							userData.inconsistencies[facetScore.inconsistency] += 1;
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
function analyzeCSV (csvData) {
	const info = extractQuestionsAndAnswers(csvData);

	const allScores = aggregate(info);

	analyze(allScores, info);

	return allScores;
}

module.exports = analyzeCSV;

