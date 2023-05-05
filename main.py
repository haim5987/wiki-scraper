from utils.wiki_animals_scraper import WikiScraper
from utils.html_builder import DictHtmlBuilder
from utils.utils_functions import *
import concurrent.futures

if __name__ == '__main__':
    wiki_scraper = WikiScraper(f'{WIKI_URL}{WIKI_ANIMAL_LIST_PATH}')
    wiki_scraper.init_species_table()

    # Use concurrent.futures to run the tasks of dictionary builder and images saver in parallel
    with concurrent.futures.ThreadPoolExecutor() as executor:
        animal_adj_dict_task = executor.submit(wiki_scraper.get_adjective_animals_dict)
        img_saver_task = executor.submit(wiki_scraper.save_animals_images)

        animal_adj_dict = animal_adj_dict_task.result()
        print(animal_adj_dict)

        converter = DictHtmlBuilder(animal_adj_dict)
        converter.export_dict_to_html(INDEX_HTML)

        img_result = img_saver_task.result()

