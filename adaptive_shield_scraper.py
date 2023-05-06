import argparse
from wiki_scraper import WikiScraper
from utils.dict_to_html_converter import DictToHtmlConverter
from utils.utils_functions import *
import concurrent.futures


def init_args_parser():
    args_parser = argparse.ArgumentParser(description=SCRIPT_DESCRIPTIONS)
    args_parser.add_argument(BUILD_DICT_FLAG, action='store_true', help=BUILD_DICT_DESCRIPTIONS)
    args_parser.add_argument(SAVE_IMAGES_FLAG, action='store_true', help=SAVE_IMAGES_DESCRIPTIONS)
    parser.add_argument('--default', nargs='?', const=1, type=int)
    return args_parser.parse_args()


def display_adj_animal_dict_and_lcl_links(adj_animal_dict):
    for adjective in adj_animal_dict.keys():
        print(f"List of Animals of {adjective}:")
        for animal in adj_animal_dict[adjective]:
            print(f'    {animal}: {TMP_PATH}/{animal}.jpg')
        print('')


def display_adj_animal_dict(adj_animal_dict):
    for adjective in adj_animal_dict.keys():
        print(f"List of Animals of {adjective}:")
        for animal in adj_animal_dict[adjective]:
            print(f'    {animal}')
        print('')


def convert_adjective_animals_dict_to_html():
    global animal_adj_dict
    try:
        converter = DictToHtmlConverter(animal_adj_dict, HTML_FILE_TITLE)
        converter.export_dict_to_html(INDEX_HTML)
        print(HTML_SUCCESS_INFO)
    except Exception as e:
        print(f'{CONVERT_HTML_ERROR}: {e}')


def build_adjective_animals_dict():
    global animal_adj_dict
    try:
        print(BUILDING_DICT_INFO)
        animal_adj_dict = wiki_scraper.get_adjective_animals_dict()
        print(DICT_SUCCESS_INFO)
        return animal_adj_dict
    except Exception as e:
        print(f'{BUILD_DICT_ERROR}: {e}')


def save_animals_images():
    try:
        print(SAVE_IMAGES_INFO)
        wiki_scraper.save_animals_images()
        print(IMAGES_SUCCESS_INFO)
    except Exception as e:
        print(f'{CONVERT_HTML_ERROR}: {e}')


if __name__ == '__main__':
    args = init_args_parser()
    wiki_scraper = WikiScraper(f'{WIKI_URL}{WIKI_ANIMAL_LIST_PATH}')
    wiki_scraper.init_species_table()

    if args.build_dict:
        build_adjective_animals_dict()
        display_adj_animal_dict(animal_adj_dict)

    if args.save_images:
        save_animals_images()

    else:
        # Build collateral adjectives and animals dictionary, download and saves animals images and converts dictionary
        # to html in parallel
        with concurrent.futures.ThreadPoolExecutor() as executor:
            animal_adj_dict_thread = executor.submit(build_adjective_animals_dict)
            img_saver_thread = executor.submit(wiki_scraper.save_animals_images)

            animal_adj_dict = animal_adj_dict_thread.result()

            convert_adjective_animals_dict_to_html()

            img_saver_thread.result()

            display_adj_animal_dict_and_lcl_links(animal_adj_dict)
