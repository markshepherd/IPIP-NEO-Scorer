'use strict';

var fs = require('fs');
const { getItems, getInfo } = require('@alheimsins/b5-johnson-120-ipip-neo-pi-r');
const { getTemplate } = require('@alheimsins/b5-result-text');
const questionInfo = getItems('en');

function printResult(result) {
	const data = getTemplate();

	for (var i = 0; i < data.length; i++) {
		var domain = data[i];
		var totalScore = 0;
		var totalCount = 0;

		for (var j = 0; j < domain.facets.length; j++) {
			var facet = domain.facets[j];
			const score = result[domain.domain][facet.facet] || {score: 0, count: 0};
			totalScore += score.score;
			totalCount += score.count;
		}
		console.log(`\n    ${domain.domain}. ${domain.title}: ${totalScore} / ${totalCount * 5}`);

		for (var j = 0; j < domain.facets.length; j++) {
			var facet = domain.facets[j];
			const score = result[domain.domain][facet.facet] || {score: 0, count: 0};
			console.log(`        ${facet.facet}. ${facet.title}: ${score.score} / ${score.count * 5}`);
		}
	}
}

// returns [domain, facet, score]
function decode(question, answer) {
	for (var i = 0; i < questionInfo.length; i++) {
		const info = questionInfo[i];
		if (info.text === question) {
			for (var j = 0; j < info.choices.length; j++) {
				const choice = info.choices[j];
				if (choice.text === answer) {
					return [info.domain, info.facet, choice.score];
				}
			}
		}
	}
	return ['XXX', 1, 4];
}

module.exports = function(file) {
	fs.readFile(file, 'utf8', function (err, data) {
  		if (err) throw err;

  		const lines = data.split(/[\n\r]+/);

  		// the first line of the data files contains a list of all the questions 
		const firstLineTokens = lines[0].split(/,/);
		const questions = [];
		for (var k = 9; k < firstLineTokens.length; k++) {
			questions.push(firstLineTokens[k]);
		}

		// Process each line of the file
		for (var i = 1; i < lines.length; i++) {
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

		  		console.log('');
		  		console.log(emailAddress);
				printResult(result);
			}
  		}
	});
}
