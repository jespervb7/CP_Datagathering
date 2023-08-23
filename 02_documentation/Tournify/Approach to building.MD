# Overview

- The script will take an URL. It's sadly impossible to automate the current website as it doesn't have a sitemap
    - There will be checks just incase it's not a valid tournament. As well as exception handling
- Grab the HTML
- Grab the data we want
- Check the data
    - This is to make sure our program grabs the correct sort of data, if it's slightly off we don't want it(?)
    - We should probably write util functions for this
- Roughly clean the data to fit the format described in the [Data_to_grab](../../../02_documentation/Data_to_grab.MD) file
- Output the data to a simple CSV file. Eventually automate this to a database.