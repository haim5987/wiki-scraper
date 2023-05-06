from utils.wiki_animals_scraper import WikiScraper
from utils.html_builder import DictHtmlBuilder
from utils.utils_functions import *
import concurrent.futures


def display_adj_animal_dict_and_lcl_links(adj_animal_dict):
    for adjective in adj_animal_dict.keys():
        print(f"List of Animals of {adjective}:")
        for animal in adj_animal_dict[adjective]:
            print(f'    {animal}: {TMP_PATH}/{animal}.jpg')
        print('')


if __name__ == '__main__':
    wiki_scraper = WikiScraper(f'{WIKI_URL}{WIKI_ANIMAL_LIST_PATH}')
    wiki_scraper.init_species_table()

    # Use concurrent.futures to run the tasks of dictionary builder and images saver in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        animal_adj_dict_task = executor.submit(wiki_scraper.get_adjective_animals_dict)
        img_saver_task = executor.submit(wiki_scraper.save_animals_images)

        animal_adj_dict = animal_adj_dict_task.result()

        converter = DictHtmlBuilder(animal_adj_dict, HTML_FILE_TITLE)
        converter.export_dict_to_html(INDEX_HTML)

        img_result = img_saver_task.result()
        display_adj_animal_dict_and_lcl_links(animal_adj_dict)
