from bs4 import BeautifulSoup
from utils.constants import *


class DictToHtmlConverter:
    def __init__(self, dictionary, title):
        self.dict = dictionary
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
        for adj, animals in self.dict.items():
            adj_title, row = self.__parse_adjectives(adj, table)
            self.__parse_animals(adj_title, row, animals)
        return str(self.soup)

    def __parse_adjectives(self, adjective, table):
        adj_title = self.soup.new_tag(CELL_TAG)
        adj_title.string = ''
        adj_title = self.soup.new_tag(CELL_TAG)
        adj_title.string = f'{adjective.capitalize()}'
        row = self.soup.new_tag(ROW_TAG)
        row.attrs[STYLE] = BORDER_STYLE
        table.append(row)
        row.append(adj_title)
        return adj_title, row

    def __parse_animals(self, adj_title, row, animals):
        for animal in animals:
            animal_link = self.soup.new_tag(LINK_TAG)
            animal_link.string = f'{animal}'
            animal_link.attrs[HREF_TAG] = f'file:///tmp/{animal}.jpg'
            adj_title.append(animal_link)
            br = self.soup.new_tag(END_LINE_TAG)
            adj_title.append(br)
            row.append(adj_title)

    def export_dict_to_html(self, filename):
        with open(filename, "w") as f:
            f.write(self.adj_animals_html_builder())
