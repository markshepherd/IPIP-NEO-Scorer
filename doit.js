'use strict';

var fs = require('fs');
const { getItems, getInfo } = require('@alheimsins/b5-johnson-120-ipip-neo-pi-r');
const questionInfo = getItems('en');

// returns [domain, facet, score]
function decode(question, answer) {
	// console.log(JSON.stringify([question, answer], undefined, 2));

	// search items
	for (var i = 0; i < questionInfo.length; i++) {
		const info = questionInfo[i];
		if (info.text === question) {
			for (var j = 0; j < info.choices.length; j++) {
				const choice = info.choices[j];
				if (choice.text === answer) {
					console.log(`${question} . ${answer} ==> ${info.domain}, ${info.facet}, ${choice.score}`);
					return [info.domain, info.facet, choice.score];
				}
			}
		}
	}
	return ['XXX', 1, 4];
}

module.exports = function(file) {
	// console.log(JSON.stringify(items, undefined, 2));

	fs.readFile(file, 'utf8', function (err, data) {
  		if (err) throw err;

  		const lines = data.split(/[\n\r]+/);
		// console.log(JSON.stringify(lines, undefined, 2));

  		// the first line of the data files contains a list of all the questions 
		const firstLineTokens = lines[0].split(/,/);
		const questions = [];
		for (var k = 9; k < firstLineTokens.length; k++) {
			questions.push(firstLineTokens[k]);
		}
		// console.log('questions ----');
		// console.log(JSON.stringify(questions, undefined, 2));

		// Process each line of the file
		for (var i = 1; i < lines.length; i++) {
  			const tokens = lines[i].split(/,/);
  			const emailAddress = tokens[5];

  			if (emailAddress) {
				// If the line has an email address, compute that user's score. results' looks like this:
				//
				//     {domain1: {facet1: score, facet2: score, ...}, domain2: ...}
				//
				const results = {};		

  				for (var j = 9; j < tokens.length; j++) {
  					const answer = tokens[j];
  					const question = questions[j - 9];
  					const [domain, facet, score] = decode(question, answer);

  					var facetScores = results[domain];
  					if (!facetScores) {
  						facetScores = {};
						results[domain] = facetScores;
  					}

  					facetScores[facet] = (facetScores[facet] || 0) + score;
				}	

		  		console.log(' -------------- RESULT ------------------');
		  		console.log(emailAddress);
				console.log(JSON.stringify(results, undefined, 2));  		

			}
  		}
	});
}
