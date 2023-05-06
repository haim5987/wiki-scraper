import argparse
from wiki_scraper import WikiScraper
from utils.dict_to_html_converter import DictToHtmlConverter
from utils.constants import *
import concurrent.futures


class AdaptiveShieldScraper:

    def __init__(self):
        self.args = self.init_args_parser()
        self.wiki_scraper = WikiScraper(f'{WIKI_URL}{WIKI_ANIMAL_LIST_PATH}')
        self.wiki_scraper.init_species_table()
        self.dict_to_html_converter = None

    def init_args_parser(self):
        self.args = argparse.ArgumentParser(description=SCRIPT_DESCRIPTIONS)
        self.args.add_argument(BUILD_DICT_FLAG, action='store_true', help=BUILD_DICT_DESCRIPTIONS)
        self.args.add_argument(SAVE_IMAGES_FLAG, action='store_true', help=SAVE_IMAGES_DESCRIPTIONS)
        return self.args.parse_args()

    def convert_adjective_animals_dict_to_html(self):
        global animal_adj_dict
        try:
            self.dict_to_html_converter = DictToHtmlConverter(animal_adj_dict, HTML_FILE_TITLE)
            self.dict_to_html_converter.export_dict_to_html(INDEX_HTML)
            print(HTML_SUCCESS_INFO)
        except Exception as e:
            print(f'{CONVERT_HTML_ERROR}: {e}')

    def build_adjective_animals_dict(self):
        global animal_adj_dict
        try:
            print(BUILDING_DICT_INFO)
            animal_adj_dict = self.wiki_scraper.get_adjective_animals_dict()
            print(DICT_SUCCESS_INFO)
            return animal_adj_dict
        except Exception as e:
            print(f'{BUILD_DICT_ERROR}: {e}')

    def download_animals_images(self):
        try:
            print(SAVE_IMAGES_INFO)
            self.wiki_scraper.download_animals_images()
            print(IMAGES_SUCCESS_INFO)
        except Exception as e:
            print(f'{CONVERT_HTML_ERROR}: {e}')

    def process_adjective_animals_data(self):
        global animal_adj_dict
        if self.args.build_dict:
            build_adjective_animals_dict()
            AdaptiveShieldScraper.display_adj_animal_dict(animal_adj_dict)

        elif self.args.save_images:
            self.download_animals_images()

        else:
            # Build collateral adjectives and animals dictionary, download and saves animals images and converts
            # dictionary to html in parallel
            with concurrent.futures.ThreadPoolExecutor() as executor:
                animal_adj_dict_thread = executor.submit(self.build_adjective_animals_dict)
                img_saver_thread = executor.submit(self.download_animals_images)
                animal_adj_dict = animal_adj_dict_thread.result()
                self.convert_adjective_animals_dict_to_html()
                img_saver_thread.result()
                AdaptiveShieldScraper.display_adj_animal_dict_and_lcl_links(animal_adj_dict)

    @staticmethod
    def display_adj_animal_dict_and_lcl_links(adj_animal_dict):
        for adjective in adj_animal_dict.keys():
            print(f"List of Animals of {adjective}:")
            for animal in adj_animal_dict[adjective]:
                print(f'    {animal}: {TMP_PATH}/{animal}.jpg')
            print('')

    @staticmethod
    def display_adj_animal_dict(adj_animal_dict):
        for adjective in adj_animal_dict.keys():
            print(f"List of Animals of {adjective}:")
            for animal in adj_animal_dict[adjective]:
                print(f'    {animal}')
            print('')


if __name__ == '__main__':
    adaptive_shield_scraper = AdaptiveShieldScraper()
    adaptive_shield_scraper.process_adjective_animals_data()
