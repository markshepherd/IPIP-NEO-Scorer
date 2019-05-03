# IPIP-NEO-Scorer
Node JS command-line app to process response data exported from the survey "Johnson 120 IPIP-NEO-PI-R" on SurveyMonkey.

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

1. Extract the data
    1. go to https://www.surveymonkey.com
    1. go to the `Johnson 120 IPIP-NEO-PI-R` project
    1. go to `Analyze Results`
    1. do `Save As > Export File > All individual responses`
    1. select File Format `XLS`
    1. do `Export`
    1. when it says `Your export is complete`, click `Download`
1. Grab the data file
    1. in Finder, go to the `Downloads` folder
    1. locate the file you just downloaded, it will be called something like `Data_All_190503.zip`
    1. double click the downloaded file to unzip it
    1. open the resulting folder, it will be called something like `Data_All_190503`
    1. open the `CSV` folder
    1. copy the file `Johnson 120 IPIP-NEO-PI-R.csv`
    1. go to the folder `Documents > IPIP-NEO-Scorer`
    1. paste the file
1. Generate the report. In Terminal, do
    1. `cd ~/Documents/IPIP-NEO-Scorer`
    1. `./cli.js "Johnson 120 IPIP-NEO-PI-R.csv" > scores.txt`

You should now have a file called `scores.txt` in your `Documents > IPIP-NEO-Scorer` folder. This file contains all the domain and facet scores for each email address that submitted a survey. Surveys that are not associated with a user email address wiil not be included in the report. You can double click this file to view it in TextEdit, or do whatever you need to do with it. Here's what the report looks like:

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
