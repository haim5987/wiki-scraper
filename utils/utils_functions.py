from utils.constants import *
import requests
import urllib.request
import os
from bs4 import BeautifulSoup


def add_pair_to_dict(dictionary, key, value):
    # Adds a key-value pair to a dictionary, creating a new list if the key doesn't exist.
    dictionary.setdefault(key, []).append(value)


def save_image_from_img_src(path, image_name, img_src):
    # Downloads an image from a given URL and saves it to a specified path and filename.
    response = requests.get(f'{HTTPS}{img_src}', headers=REQUEST_HEADER_IMG)
    if check_response_status(response):
        with open(f'{path}/{image_name}.jpg', 'wb') as f:
            f.write(response.content)


def get_soup_of_url(url):
    # Returns a BeautifulSoup object representing the HTML content of the given URL.
    response = requests.get(url)
    if check_response_status(response):
        soup = BeautifulSoup(response.content, HTML_PARSER)
        return soup


def get_img_src_from_infobox(wiki_page):
    # Extracts the image source URL from a Wikipedia page infobox.
    infobox = wiki_page.find(TABLE, {CLASS: INFOBOX})
    if infobox:
        img_tag = infobox.find(IMG_TAG)
        img_src = img_tag.get(SRC_TAG)
        return img_src


def get_img_src_from_thumb(wiki_page):
    # Extracts the image source URL from a Wikipedia page thumb.
    thumb_div = wiki_page.find('div', {CLASS: 'thumb'})
    if thumb_div:
        img_tag = thumb_div.find(IMG_TAG)
        img_src = img_tag.get(SRC_TAG)
        return img_src


def get_html_link_title(cell_tag):
    # Returns the `title` attribute of the first <a> tag found within the given Beautiful Soup `cell_tag`.
    return cell_tag.a[TITLE_TAG]


def get_html_link_href(cell_tag):
    # Returns the `href` attribute of the first <a> tag found within the given Beautiful Soup `cell_tag`.
    return cell_tag.a[HREF_TAG]


def is_valid_cells(cells):
    # Checks if a list of BeautifulSoup cells contains valid information about an animal.
    return len(cells) >= 2


def check_response_status(response):
    return response.status_code == requests.codes.ok


def print_dir_content(dir_path):
    if not os.path.isdir(dir_path):
        print(f"{dir_path} {DIRECTORY_ERROR}")
        return

    try:
        files = os.listdir(dir_path)
    except OSError as err:
        print(f"{ACCESS_DIR_ERROR} {dir_path}: {err}")
        return

    print(f"Contents of {dir_path}:")
    for file in files:
        print(file)


def merge_dict(dict1, dict2):
    for key, value in dict2.items():
        if key in dict1:
            dict1[key].extend(value)
        else:
            dict1[key] = value
