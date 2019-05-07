const analyzeCSV = require('./analyze');
const { makePDF} = require('./report');
const readline = require('readline-sync');
const fs = require('fs');

/* eslint-disable no-console */
function main() {
  let csvPath;
  const reset = "\x1b[0m";
  const highlight = "\x1b[36m";
  if (process.argv.length === 3) {
    csvPath = process.argv[2];
  } else {
    csvPath = readline.question(`${highlight}Please enter location of csv file:${reset}`);
    csvPath = csvPath.split("\\").join(""); 
  }

  fs.readFile(csvPath, 'utf8', function (err, csvData) {
    if (err) throw err;
    const allScores = analyzeCSV(csvData);
    makePDF(allScores);
  });
}
/* eslint-enable no-console */

main();
