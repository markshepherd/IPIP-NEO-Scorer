#!/usr/bin/env node
'use strict';

const { getTemplate } = require('@alheimsins/b5-result-text');
const moment = require('moment');

// Create a summary report of scores and warnings for all users. We return the report in the form of a character string.
function summaryReport(allScores) {
	let outputString = "";

	for (let emailAddress in allScores) {
		if (allScores.hasOwnProperty(emailAddress)) {
			const userData = allScores[emailAddress];
			const scoresForThisUser = userData.scores;
			let userComments = (userData.missingAnswers > 0) ? `       *** ${userData.missingAnswers} missing answers` : '';
			userComments += userData.suspiciousDuration ? `       *** Completed too quickly - ${userData.suspiciousDuration} seconds.` : '';
			let time = moment(new Date(userData.time)).format('M/D/YY H:mm');
			outputString += `\n\n\n${emailAddress}  ${time} ${userComments}\n\n${userData.image}\n`;

			// Fetch the template which contains a list of all the domains and facets, including their human-readable names. 
			// The order of items in the template defines the order of the report.
			const template = getTemplate();

			// Iterate over the domains in the template
			for (let i = 0; i < template.length; i++) {
				const domain = template[i];
				const scoresForThisDomain = scoresForThisUser[domain.domain] || {};
				const domainScore = scoresForThisDomain.score || {score: 0, count: 0};
				const facetScores = scoresForThisDomain.facets || {};

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

module.exports = {summaryReport};