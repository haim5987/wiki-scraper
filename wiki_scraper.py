import concurrent.futures
import requests
import urllib.request
import os
from bs4 import BeautifulSoup
from utils.constants import *

"""A class for scraping Wikipedia pages to build a dictionary of collateral adjectives and animals, along with 
animals images. """


class WikiScraper:
    def __init__(self, url):
        self.__url = url
        self.__soup = WikiScraper.get_soup_of_url(self.__url)
        if not self.__is_soup_valid():
            print(f'{SOUP_INIT_ERROR} {url}')

        self.species_table = None

    def init_species_table(self):
        try:
            self.species_table = self.__soup.find_all(TABLE, {CLASS: WIKI_SORT_TABLE})[SECOND_PLACE]
        except Exception as e:
            print(f"{SPECIES_TABLE_NOT_FOUND} {e}")

    def set_url(self, url):
        self.__url = url

    def get_adjective_animals_dict(self):
        adj_animal_dict = {}
        self.__check_species_table_init()

        # Use concurrent.futures to map and reduce species table
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(WikiScraper.extract_animal_details, animal_row) for animal_row in self.__get_species_table_rows()]
            # Wait for all the futures to complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    WikiScraper.merge_adjective_animals_dict(adj_animal_dict, future.result())
                except Exception as e:
                    print(f'{PROCESSING_ANIMAL_ADJ_ERROR}: {e}')

        return adj_animal_dict

    def download_animals_images(self):
        self.__check_species_table_init()
        WikiScraper.check_and_create_dir(TMP_PATH)

        # Use concurrent.futures to map and reduce species table
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(WikiScraper.download_animal_image, animal_row) for animal_row in self.__get_species_table_rows()]
            # Wait for all threads to complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f'{PROCESSING_IMG_ERROR}: {e}')

    def __get_species_table_rows(self):
        return self.species_table.find_all(ROW_TAG)[1:]

    def __check_species_table_init(self):
        if self.species_table is None or len(self.species_table) == 0:
            print(SPECIES_TABLE_UNINITIALIZED)

    def __is_soup_valid(self):
        return self.__soup is not None

    @staticmethod
    def get_adjective_lst(adjective_cell):
        """
        Returns a list of collateral adjectives extracted from a BeautifulSoup Tag.

        Description:
            This function iterates over the children of the given Tag (assumed
            to represent collateral adjectives). It filters out any children that are not <br>,
            <sup>, or '?' tags and extracts the title attribute value for any <a> tags.
        """
        return [
            adjective[TITLE_TAG] if adjective.name == LINK_TAG else adjective
            for adjective in adjective_cell.children
            if adjective.name not in [END_LINE_TAG, SUP_TAG] and adjective != QUES_MARK
        ]

    @staticmethod
    def extract_animal_details(row):
        # This function processes a row in the species table to generate dictionary of Collateral adjective and animals
        cells = row.find_all(CELL_TAG)

        if len(cells) >= 2:
            animal_cell = cells[ANIMAL_CELL_INDEX]
            animal_name = animal_cell.a[TITLE_TAG]

            adjective_cell = cells[ADJECTIVE_CELL_INDEX]
            adjective_lst = WikiScraper.get_adjective_lst(adjective_cell)

            adj_animal_dict = {}
            [adj_animal_dict.setdefault(adjective, []).append(animal_name) for adjective in adjective_lst]

            return adj_animal_dict

        return {}

    @staticmethod
    def download_animal_image(row):
        # This function processes a row in the species table to generate and saves animals images from animals links.
        cells = row.find_all(CELL_TAG)

        if len(cells) >= 2:
            animal_cell = cells[ANIMAL_CELL_INDEX]
            animal_name = animal_cell.a[TITLE_TAG]
            animal_href = animal_cell.a[HREF_TAG]

            animal_soup = WikiScraper.get_soup_of_url(f'{WIKI_URL}{animal_href}')
            img_src = WikiScraper.get_img_src_from_soup(animal_soup)
            if img_src:
                WikiScraper.save_image_from_img_src(TMP_PATH, animal_name, img_src)

    @staticmethod
    def get_img_src_from_soup(soup):
        # Get the image source from a Beautiful Soup object, attempting to find it in the 'infobox' or 'thumb' classes.
        img_src = WikiScraper.get_img_src_from_infobox(soup)
        if not img_src:
            img_src = WikiScraper.get_img_src_from_thumb(soup)
        return img_src

    @staticmethod
    def get_soup_of_url(url):
        # Returns a BeautifulSoup object representing the HTML content of the given URL.
        response = requests.get(url)
        if WikiScraper.check_response_status(response):
            soup = BeautifulSoup(response.content, HTML_PARSER)
            return soup

    @staticmethod
    def get_img_src_from_infobox(wiki_page):
        # Extracts the image source URL from a Wikipedia page infobox.
        infobox = wiki_page.find(TABLE, {CLASS: INFOBOX})
        if infobox:
            img_tag = infobox.find(IMG_TAG)
            img_src = img_tag.get(SRC_TAG)
            return img_src

    @staticmethod
    def get_img_src_from_thumb(wiki_page):
        # Extracts the image source URL from a Wikipedia page thumb.
        thumb_div = wiki_page.find(DIV_TAG, {CLASS: THUMB_TAG})
        if thumb_div:
            img_tag = thumb_div.find(IMG_TAG)
            img_src = img_tag.get(SRC_TAG)
            return img_src

    @staticmethod
    def save_image_from_img_src(path, image_name, img_src):
        # Downloads an image from a given URL and saves it to a specified path and filename.
        response = requests.get(f'{HTTPS}{img_src}', headers=REQUEST_HEADER_IMG)
        if WikiScraper.check_response_status(response):
            with open(f'{path}/{image_name}.jpg', 'wb') as f:
                f.write(response.content)

    @staticmethod
    def check_response_status(response):
        return response.status_code == requests.codes.ok

    @staticmethod
    def merge_adjective_animals_dict(dict1, dict2):
        for adjective, animals in dict2.items():
            if adjective in dict1:
                dict1[adjective].extend(animals)
            else:
                dict1[adjective] = animals

    @staticmethod
    def check_and_create_dir(path):
        # Checks if a directory exists at the given path, and creates it if it doesn't exist.
        if not os.path.isdir(path):
            os.makedirs(path)