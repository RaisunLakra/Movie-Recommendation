# Name: Raisun Lakra
# Description: Program to extract lists of indian movies till today's date.
# Details: I am learning web scraping for which I am extracting movies list from imdb. I am unaware of the user terms and conditions or any rule if applied by imdb. Also I don't know it is legal or not. It's only for learning purposes.

import logging
logging.basicConfig(level=logging.INFO)

import requests
from bs4 import BeautifulSoup

target_url = "https://www.imdb.com/search/title/?country_of_origin=IN"

response = requests.get(target_url)