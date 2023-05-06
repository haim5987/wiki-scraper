from utils.constants import *
import requests
import urllib.request
import os
from bs4 import BeautifulSoup


def check_and_create_dir(path):
    # Checks if a directory exists at the given path, and creates it if it doesn't exist.
    if not os.path.isdir(path):
        os.makedirs(path)
