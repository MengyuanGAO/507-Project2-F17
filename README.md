# Python_REST_API_iTunes

## Overview

This project used iTunes Search API to get media data from iTunes and stored them into csv files.

## Implementation 

1. Define functions to get data from iTunes Search API:
* params_unique_combination: get the unique url to request data
* sample_get_cache_itunes_data: request data from iTunes Search API or load existing data.

2. Define a class Media, representing any piece of media we can find on iTunes search.

3. Define two more different classes, each of which *inherit from* class Media: class Song & class Movie.

4. Call the functions to request data from iTunes Search API and get a list of media objects, a list of song objects as well as a list of movie objects.

5. Store the data into three different csv files.



