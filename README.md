# IPIP-NEO-Scorer
This is a command-line app that analyzes user responses to the SurveyMonkey survey "Johnson 120 IPIP-NEO-PI-R". The result is a report that gives each user's score for the [Big 5](https://en.wikipedia.org/wiki/Big_Five_personality_traits) personality traits and their 30 facets.

This app is written in NodeJS. It was developed and tested on Macintosh but I think it should work with little or no change on Windows and *nix.

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

This will create a file called `IPIP Scores.txt` in your Desktop folder. This file contains all the domain and facet scores for each email address that submitted a survey. Surveys that are not associated with a user email address wiil not be included in the report. You can double click this file to view it in TextEdit, or do whatever you need to do with it. Here's what the report looks like:

````
jane_smith_123@gmail.com

    A. Agreeableness: 92 / 120
        1. Trust: 8 / 20
        2. Morality: 20 / 20
        3. ....

    E. Extraversion: 48 / 120
        1. Friendliness: 12 / 20
        2. Gregariousness: 12 / 20
        3. ...
        
    ...
    
sanjiv_wong@yahoo.com

    A. Agreeableness ...
````

# To package the app

1. `npm install -g pkg`
1. `cd ~/Documents/IPIP-NEO-Scorer`
1. `pkg -t node10-macos-x64 --output ./IPIP-Scorer cli.js`

This will create a mac executable `IPIP-Scorer` in the same folder. If you want executables for windows or linux, `pkg --help` will tell you how.



