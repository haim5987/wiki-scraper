import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.constants import HTML_FILE_TITLE
from utils.dict_to_html_converter import DictToHtmlConverter
from wiki_scraper import WikiScraper

VALID_URL = "https://en.wikipedia.org/wiki/List_of_animal_names"
INVALID_URL = "https://en.wikipedia.org/wiki/List_of_animal_namesaaa"


def test_init_species_table_valid_url():
    scraper = WikiScraper(VALID_URL)

    scraper.init_species_table()

    assert scraper.species_table is not None


def test_init_species_table_invalid_url():
    scraper = WikiScraper(INVALID_URL)

    scraper.init_species_table()

    assert scraper.species_table is None


def test_get_adjective_animals_dict():
    scraper = WikiScraper(VALID_URL)
    scraper.init_species_table()

    adj_animal_dict = scraper.get_adjective_animals_dict()

    assert isinstance(adj_animal_dict, dict)
    assert len(adj_animal_dict) > 0


def test_adjective_animals_dict_valid_items():
    scraper = WikiScraper(VALID_URL)
    scraper.init_species_table()
    test_dict = {'castoridine': ['Beaver'], 'apian': ['Bee'], 'apiarian': ['Bee'],
                 'coleopterous': ['Beetle', 'Ladybug'], 'procyonine': ['Raccoon'],
                 'musteline': ['Badger', 'Ferret', 'Mink', 'Otter', 'Weasel', 'Wolverine']}

    adj_animal_dict = scraper.get_adjective_animals_dict()

    assert '?' not in adj_animal_dict.keys()
    for adj in test_dict:
        assert adj in adj_animal_dict.keys()
        for animal in test_dict[adj]:
            assert animal in adj_animal_dict[adj]


def test_tmp_dir_contain_valid_img():
    scraper = WikiScraper(VALID_URL)
    scraper.init_species_table()

    origin_tmp_len = len(os.listdir('/tmp'))
    scraper.download_animals_images()
    new_tmp_len = len(os.listdir('/tmp'))

    assert new_tmp_len > origin_tmp_len
    assert os.path.isfile('/tmp/Lemur.jpg')
    assert os.path.isfile('/tmp/Partridge.jpg')
    assert os.path.isfile('/tmp/Porpoise.jpg')
    assert os.path.isfile('/tmp/Falcon.jpg')


def test_export_dict_to_html():
    scraper = WikiScraper(VALID_URL)
    scraper.init_species_table()

    adj_animal_dict = scraper.get_adjective_animals_dict()
    html_builder = DictToHtmlConverter(adj_animal_dict, HTML_FILE_TITLE)
    html_builder.export_dict_to_html("index.html")

    assert os.path.exists("index.html")

    os.remove("index.html")
