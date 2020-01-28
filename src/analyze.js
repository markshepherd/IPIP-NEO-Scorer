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

// January 2020 - at present, the text of some of the survey questions includes commas and line-ends,
// which interferes with the parsing of the csv file. This function replaces six garbled lines with
// one correct line.
//
// *** Make sure to update this function if/when you edit the survey questions. ***
//
function fixColumnNames(lineArray) {
	lineArray[0] = `Respondent ID,Collector ID,Start Date,End Date,IP Address,Email Address,First Name,Last Name,Custom Data 1,In what country do you live?,,Select the racial/ethnic identity (or identities) that best describes you (please select all that apply).,,,,,,,"Please enter four digits that represent the month and year (last two digits) you were born:Example: If I was born in January 1988 I would enter ""0188""",What is your gender?,,"Are you currently pregnant?***Drinking alcohol at any time during pregnancy can cause serious harm to your developing baby. Alcohol consumption during pregnancy increases the chances of miscarriage and stillbirth and of premature birth low birthweight birth defects and fetal alcohol spectrum disorder in your baby.***Find more information about drinking during pregnancy here: https://www.marchofdimes.org/pregnancy/alcohol-during-pregnancy.aspxIf you need help to stop drinking you can: Talk to your healthcare provider about treatment programs. Join an Alcoholics Anonymous (AA) support group. In the United States: Use the SAMHSA Substance Abuse Treatment Facility Locator: https://findtreatment.samhsa.gov/ or call 1-800 662-4357.",Did you complete high school (or secondary school)?,How many years of college have you completed?,"On a scale of 1 to 10 (1 being 'I have no social support' and 10 being 'I feel very supported by the people in my life') what is your perceived level of social support?",Worry about things,,Make friends easily,Have a vivid imagination,Trust others,Complete tasks successfully,Get angry easily,Love large parties,Believe in the importance of art,Use others for my own ends,Like to tidy up,Often feel blue,Take charge,Experience my emotions intensely,Love to help others,Keep my promises,Find it difficult to approach others,Am always busy,Prefer variety to routine,Love a good fight,Work hard,Go on binges,Love excitement,Believe that I am better than others,Am always prepared,Love to read challenging material,Panic easily,Radiate joy,Tend to vote for liberal political candidates,Sympathize with the homeless,Jump into things without thinking,Fear for the worst,Feel comfortable around people,Enjoy wild flights of fantasy,Believe that others have good intentions,Excel in what I do,Get irritated easily,Talk to a lot of different people at parties,See beauty in things that others might not notice,Cheat to get ahead,Often forget to put things back in their proper place,Dislike myself,Try to lead others,Feel others' emotions,Am concerned about others,Tell the truth,Am afraid to draw attention to myself,Am always on the go,Prefer to stick with things that I know,Yell at people,Do more than what's expected of me,Rarely overindulge,Seek adventure,Avoid philosophical discussions,Think highly of myself,Carry out my plans,Become overwhelmed by events,Have a lot of fun,Believe that there is no absolute right and wrong,Feel sympathy for those who are worse off than myself,Make rash decisions,Am afraid of many things,Avoid contacts with others,Love to daydream,Trust what people say,Handle tasks smoothly,Lose my temper,Prefer to be alone,Do not like poetry,Take advantage of others,Leave a mess in my room,Am often down in the dumps,Take control of things,Rarely notice my emotional reactions,Am indifferent to the feelings of others,Break rules,Only feel comfortable with friends,Do a lot in my spare time,Dislike changes,Insult people,Do just enough work to get by,Easily resist temptations,Enjoy being reckless,Have difficulty understanding abstract ideas,Have a high opinion of myself,Waste my time,Feel that I'm unable to deal with things,Love life,Tend to vote for conservative political candidates,Am not interested in other people's problems,Rush into things,Get stressed out easily,Keep others at a distance,Like to get lost in thought,Distrust people,Know how to get things done,Am not easily annoyed,Avoid crowds,Do not enjoy going to art museums,Obstruct others' plans,Leave my belongings around,Act without thinking,Feel comfortable with myself,Wait for others to lead the way,Don't understand people who get emotional,Take no time for others,Break my promises,Am not bothered by difficult social situations,Like to take it easy,Am attached to conventional ways,Get back at others,Put little time and effort into my work,Am able to control my cravings,Act wild and crazy,Am not interested in theoretical discussions,Boast about my virtues,Have difficulty starting tasks,Remain calm under pressure,Look at the bright side of life,Believe that we should be tough on crime,Try not to think about the needy,I really want to make changes in my drinking.,Sometimes I wonder if I'm an alcoholic.,"If I don't change my drinking soon my problems are going to get worse.",I have already started making some changes in my drinking.,"I was drinking too much at one time but I've managed to change my drinking.",Sometimes I wonder if my drinking is hurting other people.,I am a problem drinker.,"I'm not just thinking about changing my drinking I'm already doing something about it.","I have already changed my drinking and I am looking for ways to keep from slipping back to my old pattern.",I have serious problems with drinking. ,Sometimes I wonder if I am in control of my drinking. ,My drinking is causing a lot of harm.,I am actively doing things now to cut down or stop my drinking.,I want help to keep from going back to the drinking problems that I had before.,I know that I have a drinking problem.,There are times when I wonder if I drink too much.,I am an alcoholic.,I am working hard to change my drinking.,"I have made some changes in my drinking and I want some help to keep from going back to the way I used to drink.","Within the past 90 days on about how many days have you consumed alcohol?","Within the past two weeks on days that you drink alcohol about how many drinks on average do you consume?--> If unsure convert your drinks into standard drink sizes here: http://aodtool.cfar.uvic.ca/index-stddt.html",,What is your approximate body weight (please specify pounds or kilograms)?,Have you ever been in treatment for alcohol abuse?,Are you currently in treatment for alcohol abuse?,"Are you currently attending/participating in a mutual-aid support group (e.g. Alcoholics Anonymous or other 12-step group Celebrate Recovery Smart Recovery Refuge Recovery etc.)?","If you are currently sober/abstinent from alcohol what is your sobriety date (skip this question if not applicable)?",,"This question will allow us to create a unique respondent code for you so we can connect your first and second surveys and keep your responses anonymous. If you are not providing your email address you may leave this question blank.Please enter the first two letters of the city/town in which you had your first job:Example: If my first job was in Toronto I would enter ""to"""`;
	lineArray.splice(1,5);
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
	fixColumnNames(lines);

	// The first line of the csv data contains the name of each column.
	const columnNames = lines[0].split(/,/u);

	// The first few columns of each line are metadata. Grab the data that we're interested in.
	const mmyyIndex = _.findIndex(columnNames, (n) => n.match(/Please enter four digits/u));
	const firstTwoLettersIndex = _.findIndex(columnNames, (n) => n.match(/This question will allow us/u));
	const startTimeIndex = columnNames.indexOf("Start Date");
	const endTimeIndex = columnNames.indexOf("End Date");
	const sexIndex = columnNames.indexOf("What is your gender?");
	const firstQuestionIndex = columnNames.indexOf("Worry about things");

	// Starting at firstQuestionIndex, the next 120 columns are the responses to each Johnson question.
	// We'll make a list of questions, and a list of what columns contains the answer to each question.
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
		gotUser: if (userId) {
			let gender = {male: "Male", female: "Female"}[tokens[sexIndex].toLowerCase()];
			if (!gender) {
				// eslint-disable-next-line no-console
				console.log(`*** User ID ${userId} has unrecognized gender "${tokens[sexIndex]}".`);
				gender = 'Female';
			}	
			const age = findAge(tokens[mmyyIndex]);
			if (!(Number.isInteger(age) && age > 16 && age < 999)) {
				// eslint-disable-next-line no-console
				console.log(`*** User ID ${userId} has out-of-range age "${age}".`);
				break gotUser;
			}
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
					age: age,
					sex: gender,
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

