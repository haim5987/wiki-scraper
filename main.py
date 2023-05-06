import argparse
from utils.wiki_animals_scraper import WikiScraper
from utils.html_builder import DictHtmlBuilder
from utils.utils_functions import *
import concurrent.futures


def init_args_parser():
    args_parser = argparse.ArgumentParser(description=SCRIPT_DESCRIPTIONS)
    args_parser.add_argument(BUILD_DICT_FLAG, action='store_true', help=BUILD_DICT_DESCRIPTIONS)
    args_parser.add_argument(SAVE_IMAGES_FLAG, action='store_true', help=SAVE_IMAGES_DESCRIPTIONS)
    return args_parser.parse_args()


def display_adj_animal_dict_and_lcl_links(adj_animal_dict):
    for adjective in adj_animal_dict.keys():
        print(f"List of Animals of {adjective}:")
        for animal in adj_animal_dict[adjective]:
            print(f'    {animal}: {TMP_PATH}/{animal}.jpg')
        print('')


def run_all_tasks():
    global animal_adj_dict
    print("Running all tasks...\n")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        animal_adj_dict_task = executor.submit(wiki_scraper.get_adjective_animals_dict)
        img_saver_task = executor.submit(wiki_scraper.save_animals_images)

        print(BUILDING_DICT_INFO)
        animal_adj_dict = animal_adj_dict_task.result()
        print(DICT_SUCCESS_INFO)

        converter = DictHtmlBuilder(animal_adj_dict, HTML_FILE_TITLE)
        converter.export_dict_to_html(INDEX_HTML)
        print(HTML_SUCCESS_INFO)

        print(SAVE_IMAGES_INFO)
        img_saver_task.result()
        print(IMAGES_SUCCESS_INFO)
        display_adj_animal_dict_and_lcl_links(animal_adj_dict)


def run_build_dict_task():
    global animal_adj_dict
    print(BUILDING_DICT_INFO)
    animal_adj_dict = wiki_scraper.get_adjective_animals_dict()
    print(DICT_SUCCESS_INFO)
    display_adj_animal_dict_and_lcl_links(animal_adj_dict)


def run_save_images_task():
    print(SAVE_IMAGES_INFO)
    wiki_scraper.save_animals_images()


if __name__ == '__main__':
    args = init_args_parser()
    wiki_scraper = WikiScraper(f'{WIKI_URL}{WIKI_ANIMAL_LIST_PATH}')
    wiki_scraper.init_species_table()

    if not args.build_dict and not args.save_images:
        run_all_tasks()
    if args.build_dict:
        run_build_dict_task()
    if args.save_images:
        run_save_images_task()
