# Overview

Base URL = https://www.tourney.nz/data/tournaments <- it's an API call containing links to each of the tournaments
Once we have the JSON file we append the ID of each tournament to the following URL: https://www.tourney.nz/data/tournament/<id>

**Pay attention to the second link. It's slightly different than the base URL**

# Requirements
- This should be an automatted script, meaning we should be able to schedule it with cron
- The data should be returned in some folder for further cleaning down the line. Once we have all the data we will create a cleaning project on github showcasing data cleaning.
- CSV files should not be shown on git (add to gitignore)
- We should store the links scraped somewhere so our script can check that first. However putting it into a database is something we will do later.
- Get the match events if possible. 

## Match events API description
The url for this is https://www.tourney.nz/data/tournament/<tournament uuid>/date/<Date uuid>/pitch/<pitch uuid>/game/<game uuid>
So in order to check each match properly you need to also grab those items from the JSON file