import pytest
from utils.wiki_animals_scraper import WikiScraper

# A valid Wikipedia URL to use for testing
VALID_URL = "https://en.wikipedia.org/wiki/List_of_animal_names"
INVALID_URL = "https://en.wikipedia.org/wiki/List_of_animal_namesaaa"


def test_init_species_table_valid_url():
    # Create a scraper object
    scraper = WikiScraper(VALID_URL)

    # Call the init_species_table method
    scraper.init_species_table()

    # Assert that the species_table attribute is not None
    assert scraper.species_table is not None


def test_init_species_table_invalid_url():
    # Create a scraper object
    scraper = WikiScraper(INVALID_URL)

    # Call the init_species_table method
    scraper.init_species_table()

    # Assert that the species_table attribute is not None
    assert scraper.species_table is None
