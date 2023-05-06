import concurrent.futures
from utils.utils_functions import *

"""A class for scraping Wikipedia pages to build a dictionary of collateral adjectives and animals, along with 
animals images. """


class WikiScraper:
    def __init__(self, url):
        self.__url = url
        self.__soup = get_soup_of_url(self.__url)
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
        self.__check_species_table_init()

        adj_animal_dict = {}

        # Use concurrent.futures to map and reduce species table
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_row_for_dict, row) for row in self.__get_species_table_rows()]

            # Wait for all the futures to complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    merge_dict(adj_animal_dict, future.result())
                except Exception as e:
                    print(f'{PROCESSING_ANIMAL_ADJ_ERROR}: {e}')

        return adj_animal_dict

    def save_animals_images(self):
        self.__check_species_table_init()
        counter = 0
        # Use concurrent.futures to map and reduce species table
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(process_row_for_img, row, counter) for row in self.__get_species_table_rows()]

            # Wait for all threads to complete
            for future in concurrent.futures.as_completed(futures):
                try:
                    future.result()
                except Exception as e:
                    print(f'{PROCESSING_IMG_ERROR}: {e}')
        print(f'img None counter: {counter}')

    def __get_species_table_rows(self):
        return self.species_table.find_all(ROW_TAG)[1:]

    def __check_species_table_init(self):
        if self.species_table is None or len(self.species_table) == 0:
            print(SPECIES_TABLE_UNINITIALIZED)
            exit(EXIT_FAIL)

    def __is_soup_valid(self):
        return self.__soup is not None


# Helper Functions

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


def process_row_for_dict(row):
    """
    This function processes a row in the species table to generate dictionary of Collateral adjective and animals
    """
    cells = row.find_all(CELL_TAG)

    if is_valid_cells(cells):
        animal_cell = cells[ANIMAL_CELL_INDEX]
        animal_name = get_html_link_title(animal_cell)

        adjective_cell = cells[ADJECTIVE_CELL_INDEX]
        adjective_lst = get_adjective_lst(adjective_cell)

        adj_animal_dict = {}
        [add_pair_to_dict(adj_animal_dict, adjective, animal_name) for adjective in adjective_lst]
        # [adj_animal_dict.setdefault(adjective, []).append(animal_name) for adjective in adjective_lst]

        return adj_animal_dict

    return {}


def process_row_for_img(row, counter):
    """
    This function processes a row in the species table to generate and saves animals images from animals links.
    """
    cells = row.find_all(CELL_TAG)

    if is_valid_cells(cells):
        animal_cell = cells[ANIMAL_CELL_INDEX]
        animal_name = get_html_link_title(animal_cell)
        animal_href = get_html_link_href(animal_cell)

        animal_soup = get_soup_of_url(f'{WIKI_URL}{animal_href}')
        img_src = get_img_src_from_infobox(animal_soup)
        if img_src is None:
            counter += 1
        save_image_from_img_src(TMP_PATH, animal_name, img_src)
