# IPIP-NEO-Scorer
This is a command-line app that analyzes user responses to the SurveyMonkey survey "Johnson 120 IPIP-NEO-PI-R". The result is a report that gives each user's score for the [Big 5](https://en.wikipedia.org/wiki/Big_Five_personality_traits) personality traits and their 30 facets.

This app is written in NodeJS. It was developed and tested on Macintosh but I think it should work with little or no change on Windows and *nix.

The IPIP-NEO personality survey was created by Dr. J. Johnson of Penn State University. This app uses scoring algorithms based in part on the cgi code of Johnson's web site, at http://www.personal.psu.edu/~j5j/IPIP/.

Thanks to the [bigfive](https://github.com/Alheimsins/bigfive-web "title") project, which provided a couple of node modules - `@alheimsins/b5-johnson-120-ipip-neo-pi-r` and `@alheimsins/b5-result-text` - that we use. These modules define the 120 questions and how they map to domains and facets. They also provide the full text of questions, answers, domain/descriptions, and facet names/descriptions.

# To install the app:

1. Install `node.js`
    1. in Terminal, do `node -v`
    1. if it says "command not found" then go to https://nodejs.org/en/download/ and install `node.js`.
1. Install git
    1. in Terminal, do `git --version`
    1. if it says "command not found" then go to https://git-scm.com/downloads and install `git`.
1. In Terminal, do
    1. `cd ~/Documents`
    1. `git clone https://github.com/markshepherd/IPIP-NEO-Scorer.git`
    1. `cd IPIP-NEO-Scorer`
    1. `npm install`
    
# To run the app

1. Extract the data from survey monkey
    1. go to https://www.surveymonkey.com
    1. go to the `Johnson 120 IPIP-NEO-PI-R` project
    1. go to `Analyze Results`
    1. do `Save As > Export File > All individual responses`
    1. select File Format `XLS`
    1. do `Export`
    1. when it says `Your export is complete`, click `Download`
1. Find the data file
    1. in Finder, go to the `Downloads` folder
    1. locate the file you just downloaded, it will be called something like `Data_All_190503.zip`
    1. double click the downloaded file to unzip it
    1. open the resulting folder, it will be called something like `Data_All_190503`
    1. open the `CSV` folder
1. Generate the report.
    1. in Terminal do `cd ~/Documents/IPIP-NEO-Scorer`
    1. do `./cli.js`
    
    When it prompts for a filename, drag in the file `Johnson 120 IPIP-NEO-PI-R.csv` from the `csv` folder, and hit Return.

This will create a folder called `IPIP Scores` in your Documents folder. Each time you run the app it creates a new sub-folder with a unique timestamp name, and adds various documents derived from the survey answers:
* Scores.csv - a concise data file giving each user's 5 domain scores and 30 facet scores
* Report.txt - a summary report giving each user's domain and facet scores, along with annotations that help you evaluate how reliable the answers are.
* *email-address*.pdf - for each user there is a PDF file with the email address as the file name. This is a detailed report, custom-generated for each user, that explains each of the user's domain and facet scores.
* Survey Answers.csv - a copy of the input data file

# Development notes

`npm start` runs the analyzer and prompts for an input csv file

`npm run lint` runs the linter on all js files. DO THIS BEFORE EVERY COMMIT!

`npm test` runs the test suite, and gives a pass/fail result on the console. DO THIS BEFORE EVERY COMMIT!

`npm run dev` runs the analyzer on the input file `test/Johnson xxxx.csv`

`npm run debug` runs the analyzer on the input file `test/Johnson xxxx.csv`, connects to debugger

`npm run package` creates a stand-alone mac app packaged in a zip file in the `build` folder. When you unzip, you get a folder containing (1) the mac executable `IPIP-Scorer`, and (2) a sub-folder called chromium. These 2 items must be kept together in the same folder; the executable expects to find chromium there. If you want executables for windows or linux, take a look at `pkg --help`. It is always safe to delete the entire `build` folder, it is re-created whenever you `npm run package`.

