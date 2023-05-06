from bs4 import BeautifulSoup
from utils.constants import *


class DictHtmlBuilder:
    def __init__(self, dictionary, title):
        self.my_dict = dictionary
        self.soup = BeautifulSoup(HTML_FILE_HEADER, HTML_PARSER)
        self.soup.title.string = title
        h1 = self.soup.new_tag(H1_TAG)
        h1.string = title
        self.soup.body.append(h1)

    def adj_animals_html_builder(self):
        """
        This method build html page from given dictionary of Collateral adjective and Animals list
        """
        table = self.soup.new_tag(TABLE)
        table.attrs[STYLE] = CSS_TABLE_STYLE
        self.soup.body.append(table)
        for adj, animals in self.my_dict.items():
            animal_title, row = self.__parse_adjectives(adj, table)
            self.__parse_animals(animal_title, row, animals)
        return str(self.soup)

    def __parse_adjectives(self, key, table):
        animal_title = self.soup.new_tag(CELL_TAG)
        animal_title.string = ''
        adj_title = self.soup.new_tag(CELL_TAG)
        adj_title.string = f'{key.capitalize()}'
        row = self.soup.new_tag(ROW_TAG)
        row.attrs[STYLE] = BORDER_STYLE
        table.append(row)
        row.append(adj_title)
        return animal_title, row

    def __parse_animals(self, animal_title, row, animals):
        for animal in animals:
            animal_link = self.soup.new_tag(LINK_TAG)
            animal_link.string = f'{animal}'
            animal_link.attrs[HREF_TAG] = f'file:///tmp/{animal}.jpg'
            animal_title.append(animal_link)
            br = self.soup.new_tag(END_LINE_TAG)
            animal_title.append(br)
            row.append(animal_title)

    def export_dict_to_html(self, filename):
        with open(filename, "w") as f:
            f.write(self.adj_animals_html_builder())
