#!/usr/bin/env node


const {getTemplate, getDomain} = require("@alheimsins/b5-result-text");
const moment = require("moment");
const puppeteer = require("puppeteer");
const ejs = require("ejs");
const path = require("path");
const fs = require("fs");

/*
  "userId": "ab1234",
  "time": "5/3/19 14:19",
  "domains": [
	{
	  "name": "Ddddddd",
	  "shortDescription": "Xxx. Xxx. Xxx. Xxx. ",
	  "longDescription": "Yyy yyy. Yyy yyy. Yyy yyy. Yyy yyy. ",
	  "score": {score: nnn, max: nnn, rating: 'high'},
	  "yourScoreDescription": "Your medium score means xxx.",
	  "facets": [
		{
		  "name": "Ffffff",
		  "score": {score: nnn, max: nnn, rating: 'high'}
		  "description": "Zzzzz. Zzzzz. Zzzzz. Zzzzz. ",
		},
*/

const oneUserPDFTemplate = `
<html>
<head>
<title>IPIP Scores for <%= userId %> - <%= time %></title>
<style>
body {
  font-family: Arial, Helvetica, sans-serif;
}
</style>
</head>
<body>
<h1>IPIP Scores for <%= userId %> <%= sex %> <%= age %> </h1>
<p><%= time %></p>
<% domains.forEach(function (domain) { -%>
	<h2><%= domain.name %></h2>
	<p><%= domain.shortDescription %></p>
	<p>Score: <%= domain.score.score %> - <%= domain.score.rating %><p>
	<p><%= domain.yourScoreDescription %></p>
	<% domain.facets.forEach(function (facet) { -%>
		<h4><%= facet.name %></h4>
		<p>Score: <%= facet.score.score %> - <%= facet.score.rating %><p>
		<p><%= facet.description %></p>
	<% }) -%>
<% }) -%>
</body>
</html>
`;

/* eslint-disable no-console */
async function makePDF (allScores, outputFolder) {
	// When we use 'pkg' to create a stand-alone executable of this app, 'pkg' fails to include
	// the chromium binary that's in the puppeteer node module. (It gives you a message telling you this).
	// As a workaround, our 'package' script explicitly copies the chromium folder into the folder
	// that contains the executable, and the following code tells puppeteer where to find chromium.
	// This workaround was inspired by https://github.com/rocklau/pkg-puppeteer/blob/master/index.js
	const chromiumExecutablePath = (typeof process.pkg !== "undefined")
		? puppeteer.executablePath().replace(
			/^.*?\/node_modules\/puppeteer\/\.local-chromium/u,
			path.join(path.dirname(process.execPath), "chromium"))
		: puppeteer.executablePath();

	const browser = await puppeteer.launch({executablePath: chromiumExecutablePath, headless: true});
	const page = await browser.newPage();

	for (const userId in allScores) {
		if (allScores.hasOwnProperty(userId)) {
			// Write a dot to the console without a newline
			process.stdout.write(". ");
			const userData = allScores[userId];
			const time = moment(new Date(userData.time)).format("MMM D, Y h:mma");
			const params = {userId, sex: userData.sex, age: userData.age, time, domains: []};

			for (const domain in userData.scores) {
				if (userData.scores.hasOwnProperty(domain)) {
					const domainData = userData.scores[domain];
					const domainStrings = getDomain({language: "en", domain});
					const yourScoreDescription = domainStrings.results.find((info) => {
						if (domainData.score.rating === "average") {
							return info.score === "neutral";
						} else {
							return info.score === domainData.score.rating;
						}
					}).text;

					const domainParams = {
						name: domainStrings.title,
						score: {score: domainData.score.percentileScore, rating: domainData.score.rating},
						shortDescription: domainStrings.shortDescription,
						longDescription: domainStrings.description,
						yourScoreDescription: yourScoreDescription,
						facets: []
					};

					for (const facet in domainData.facets) {
						if (domainData.facets.hasOwnProperty(facet)) {
							const facetData = domainData.facets[facet];
							const facetStrings = domainStrings.facets[facet - 1];
							const facetParams = {
								name: facetStrings.title,
								description: facetStrings.text,
								score: {score: facetData.percentileScore, rating: facetData.rating}
							};
							domainParams.facets.push(facetParams);
						}
					}

					params.domains.push(domainParams);
				}
			}

			const html = ejs.render(oneUserPDFTemplate, params, {});
			const outputFileName = path.join(outputFolder, userId.replace("@", "_"));
			const err = fs.writeFileSync(`${outputFileName}.html`, html);
			if (err) {
				console.log(err);
			} else {
				const gotoFile = `file://${outputFileName}.html`;
				await page.goto(gotoFile, {waitUntil: "networkidle2"});
				await page.pdf({path: `${outputFileName}.pdf`, format: "Letter"});
				fs.unlinkSync(`${outputFileName}.html`);
			}
		}
	}
	await browser.close();
}
/* eslint-enable no-console */

// Create a summary report of scores and warnings for all users. We return the report in the form of a character string.
function summaryReport (allScores) {
	let outputString = "";
	const inconsistencyCounts = {};

	for (const userId in allScores) {
		if (allScores.hasOwnProperty(userId)) {
			const userData = allScores[userId];
			const scoresForThisUser = userData.scores;
			let userComments = (userData.missingAnswers > 0) ? `       *** ${userData.missingAnswers} missing answers` : "";
			userComments += userData.suspiciousDuration ? `       *** Completed too quickly - ${userData.suspiciousDuration} seconds.` : "";
			userComments += (!userData.age || !userData.sex) ? "       *** age or sex not specified" : "";
			const inconsistencyCount = userData.inconsistencies.bad + userData.inconsistencies.minor;
			if (inconsistencyCount > 0) {
				userComments += `       *** inconsistencies: bad ${userData.inconsistencies.bad}, minor ${userData.inconsistencies.minor}, total ${inconsistencyCount}`;
			}
			inconsistencyCounts[inconsistencyCount] = (inconsistencyCounts[inconsistencyCount] || 0) + 1;
			const time = moment(new Date(userData.time)).format("M/D/YY H:mm");
			outputString += `\n\n\n${userId}   ${time}   ${userData.sex} ${userData.age}   ${userComments}\n\n${userData.image}\n`;

			// Fetch the template which contains a list of all the domains and facets, including their human-readable names.
			// The order of items in the template defines the order of the report.
			const template = getTemplate();

			// Iterate over the domains in the template
			for (let i = 0; i < template.length; i++) {
				const domain = template[i];
				const scoresForThisDomain = scoresForThisUser[domain.domain] || {};
				const domainScore = scoresForThisDomain.score || {score: 0, count: 0, rating: "average"};
				const facetScores = scoresForThisDomain.facets || {};

				// Print the domain summary line
				outputString += `\n    ${domain.domain}. ${domain.title}: ${domainScore.percentileScore} ${domainScore.rating}  (${domainScore.score} / ${domainScore.count * 5})\n`;

				// Iterate over facets and print a line for each facet.
				for (let k = 0; k < domain.facets.length; k++) {
					const facet = domain.facets[k];
					const facetScore = facetScores[facet.facet] || {score: 0, count: 0, scores: [], inconsistency: "none", rating: "average"};
					const scoreString = facetScore.inconsistency !== "none"
						? `*** ${facetScore.inconsistency} inconsistency; scores are ${facetScore.scores}` : "";
					outputString +=
						`        ${facet.facet}. ${facet.title}: ${facetScore.percentileScore} ${facetScore.rating}  (${facetScore.score} / ${facetScore.count * 5})      ${scoreString}\n`;
				}
			}
		}
	}

	outputString += `\n<Inconsistency count>:<number of users> - `;
	for (const count in inconsistencyCounts) {
		if (inconsistencyCounts.hasOwnProperty(count)) {
			outputString += `\n${count}: ${inconsistencyCounts[count]}`;
		}
	}
	outputString += `\n`;
	return outputString;
}

// Create a summary report of scores and warnings for all users. We return the report in the form of a character string.
function exportScores (allScores) {
	const lines = [];

	// Create the title line
	let values = [];
	values.push("");
	values.push("");
	const template = getTemplate();
	for (let i = 0; i < template.length; i++) {
		const domain = template[i];

		values.push(domain.title);

		for (let k = 0; k < domain.facets.length; k++) {
			const facet = domain.facets[k];
			values.push(facet.title);
		}
	}
	lines.push(values.join(","));

	for (const userId in allScores) {
		if (allScores.hasOwnProperty(userId)) {
			values = [];
			const userData = allScores[userId];
			const scoresForThisUser = userData.scores;

			values.push(userId);
			values.push(moment(new Date(userData.time)).format("M/D/Y HH:mm"));

			for (let i = 0; i < template.length; i++) {
				const domain = template[i];
				const scoresForThisDomain = scoresForThisUser[domain.domain] || {};
				const domainScore = scoresForThisDomain.score || {percentileScore: 0};
				const facetScores = scoresForThisDomain.facets || {};

				values.push(domainScore.percentileScore);

				for (let k = 0; k < domain.facets.length; k++) {
					const facet = domain.facets[k];
					const facetScore = facetScores[facet.facet] || {percentileScore: 0};
					values.push(facetScore.percentileScore);
				}
			}

			lines.push(values.join(","));
		}
	}
	return lines.join("\n");
}

module.exports = {summaryReport, makePDF, exportScores};
