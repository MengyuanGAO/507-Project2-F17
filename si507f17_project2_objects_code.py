import requests
import json
import unittest
import csv


######### Part One
## You can search for a variety of different types of media with the iTunes Search API: songs, movies, ebooks and audiobooks... (and more) You'll definitely need to check out the documentation to understand/recall how the parameters of this API work: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/

def params_unique_combination(baseurl, params_d, private_keys=['api_key']):
    alphabetized_keys = sorted(params_d.keys())
    res = []
    for k in alphabetized_keys:
        if k not in private_keys:
            res.append("{}-{}".format(k, params_d[k]))
    return baseurl + "_".join(res)


def sample_get_cache_itunes_data(search_term, media_term="all"):
    CACHE_FNAME = 'cache_file_name.json'
    try:
        cache_file = open(CACHE_FNAME, 'r')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents)
        cache_file.close()
    except:
        CACHE_DICTION = {}
    baseurl = "https://itunes.apple.com/search"
    params = {}
    params["media"] = media_term
    params["term"] = search_term
    unique_ident = params_unique_combination(baseurl, params)
    if unique_ident in CACHE_DICTION:
        return CACHE_DICTION[unique_ident]
    else:
        CACHE_DICTION[unique_ident] = json.loads(requests.get(baseurl, params=params).text)
        full_text = json.dumps(CACHE_DICTION)
        cache_file_ref = open(CACHE_FNAME, "w")
        cache_file_ref.write(full_text)
        cache_file_ref.close()
        return CACHE_DICTION[unique_ident]

    
    
###### Part Two
## define a class Media, representing ANY piece of media you can find on iTunes search.

## The Media class should accept one dictionary data structure representing a piece of media from iTunes as input to the constructor.
## Its constructor should invoke a method to get and cache data, and instatiate at least the following instance variables:
## - title
## - author
## - itunes_URL
## - itunes_id (e.g. the value of the track ID, whatever the track is in the data... a movie, a song, etc)

## The Media class should also have the following methods:
## - a special string method, that returns a string of the form 'TITLE by AUTHOR'
## - a special representation method, which returns "ITUNES MEDIA: <itunes id>" with the iTunes id number for the piece of media (e.g. the track) only in place of "<itunes id>"
## - a special len method, which, for the Media class, returns 0 no matter what. (The length of an audiobook might mean something different from the length of a song, depending on how you want to define them!)
## - a special contains method (for the in operator) which takes one additional input, as all contains methods must, which should always be a string, and checks to see if the string input to this contains method is INSIDE the string representing the title of this piece of media (the title instance variable)


class Media(object):
    def __init__(self, media_info_dict):
        self.type = 'media'
        self.title = media_info_dict['trackName']
        self.author = media_info_dict['artistName']
        self.itunes_URL = media_info_dict['trackViewUrl']
        self.itunes_id = media_info_dict['trackId']

    def __str__(self):
        return "{} by {}".format(self.title, self.author)

    def __repr__(self):
        return "ITUNES MEDIA: {}".format(self.itunes_id)

    def __len__(self):
        return 0

    def __contains__(self, term):
        return term in self.title

    
    
##### Part Three
#define 2 more different classes, each of which *inherit from* class Media:
## class Song
## class Movie

## In the class definitions, you can assume a programmer would pass to each class's constructor only a dictionary that represented the correct media type (song, movie, audiobook/ebook).

## Below follows a description of how each of these should be different from the Media parent class.

### class Song:

## Should have the following additional instance variables:
## - album (the album title)
## - track_number (the number representing its track number on the album)
## - genre (the primary genre name from the data iTunes gives you)

## Should have the len method overridden to return the number of seconds in the song. (HINT: The data supplies number of milliseconds in the song... How can you access that data and convert it to seconds?)


class Song(Media):
    def __init__(self, media_info_dict):
        super().__init__(media_info_dict) #
        self.type = 'songs'
        self.album = media_info_dict['collectionName']
        self.track_number = media_info_dict['trackNumber']
        self.genre = media_info_dict['primaryGenreName']
        self.time = media_info_dict['trackTimeMillis']

    def __len__(self):
        return int(self.time / 1000)


### class Movie:

## Should have the following additional instance variables:
## - rating (the content advisory rating, from the data)
## - genre
## - description (if none, the value of this instance variable should be None) -- NOTE that this might cause some string encoding problems for you to debug!
## HINT: Check out the Unicode sub-section of the textbook! This is a common type of Python debugging you'll encounter with real data... but using the right small amount of code to fix it will solve all your problems.

## Should have the len method overridden to return the number of minutes in the movie (HINT: The data returns the number of milliseconds in the movie... how can you convert that to minutes?)

## Should have an additional method called title_words_num that returns an integer representing the number of words in the movie description. If there is no movie description, this method should return 0.


class Movie(Media):
    def __init__(self, media_info_dict):
        super().__init__(media_info_dict)
        self.type = 'movies'
        self.rating = media_info_dict['contentAdvisoryRating']
        self.genre = media_info_dict['primaryGenreName']
        try:
            self.description = media_info_dict['longDescription']
        except KeyError:
            self.description = None
        try:
            self.time = media_info_dict['trackTimeMillis']
        except KeyError:
            self.time = 0

    def __len__(self):
        return int(self.time / (1000 * 60))

    def title_words_num(self):
        if description is None:
            return 0
        else:
            return len(self.description.split())


        
#### Part Five
## write some code to use the definitions you've just written.

## First, here we have provided some variables which hold data about media overall, songs, movies, and books.

## NOTE: (The first time you run this file, data will be cached, so the data saved in each variable will be the same each time you run the file, as long as you do not delete your cached data.)

media_samples = sample_get_cache_itunes_data("love")["results"]
song_samples = sample_get_cache_itunes_data("love", "music")["results"]
movie_samples = sample_get_cache_itunes_data("love", "movie")["results"]

## You may want to do some investigation on these variables to make sure you understand correctly what type of value they hold, what's in each one!

## Use the values in these variables above, and the class definitions you've written, in order to create a list of each media type, including "media" generally.

## You should end up with: a list of Media objects saved in a variable media_list,
## a list of Song objects saved in a variable song_list,
## a list of Movie objects saved in a variable movie_list,
## and a list of Book objects saved in a variable book_list.

## You may use any method of accumulation to make that happen.

media_list = [Media(media_info_dict) for media_info_dict in media_samples]
song_list = [Song(media_info_dict) for media_info_dict in song_samples]
movie_list = [Movie(media_info_dict) for media_info_dict in movie_samples]


###### Part Five
## Finally, write 3 CSV files:
# - movies.csv
# - songs.csv
# - media.csv

## Each of those CSV files should have 5 columns each:
# - title
# - artist
# - id 
# - url (for the itunes url of that thing -- the url to view that track of media on iTunes) 
# - length 



FIELD_NAMES = ['title', 'artist', 'id', 'url', 'length']


def write_to_csv(media_list):
    file_name = media_list[0].type + '.csv'
    with open(file_name, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, FIELD_NAMES)
        writer.writeheader()
        for media in media_list:
            writer.writerow({
                'title': media.title,
                'artist': media.author,
                'id': media.itunes_id,
                'url': media.itunes_URL,
                'length': len(media)
            })


write_to_csv(media_list)
write_to_csv(song_list)
write_to_csv(movie_list)
