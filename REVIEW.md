## Review Readme

### Introduction
This readme file is intended for the reviewers of my home assignment project. In this file, I will describe how I approached the assignment and the thought process behind my implementation.

### Design
The project comprises `WikiScraper`, `DictToHtmlConverter`, and `AdaptiveShieldScraper` classes, which I decided to implement using the OOP approach to achieve a modular and organized design.

The `WikiScraper` class handles the Wikipedia implementation of building the dictionary and saving the images methods. To make the code modular, the class receives the URL from the user in a way that allows it to extend more methods related to different URLs in the future.

The `DictToHtmlConverter` class is designed to receive the dictionary and file title and export it to an HTML file displaying the keys and values in a table format.

To further organize the code, I created a utils package containing the `DictToHtmlConverter` class, and a constants file containing common constant variables used in the project.

The `AdaptiveShieldScraper` is responsible for initializing the program arguments, the `WikiScraper` object, and displaying the results.

### Implementation
To read and write HTML files, I used the `BeautifulSoup` module, which offers a restful API for this task. To send requests to HTML pages, I used the `requests` module.

To read the species table on both `get_adjective_animals_dict` and `download_animals_images`, I used the `concurrent.futures` module, which offers multi-threading using the map and reduce to process the data of the table, making it a more efficient solution for large amounts of data.

For the implementation of the images saver for every animal wiki page, I built the `get_img_src_from_infobox` function, which gets the image from the infobox of the wiki page. If this approach didn't retrieve the main image, I tried to get the image from the thumb.

The main class (`AdaptiveShieldScraper`) is responsible for running the main and bonus tasks. Running the main script, building the dictionary, and saving the images will run parallelly as independent tasks using `concurrent.futures`. After they have successfully finished, the function of `display_adj_animal_dict_and_lcl_links` will display them and their local links, and the `DictToHtmlConverter` will build the HTML page and call it `index.html`.

To export the dictionary to an HTML file, I utilized the `DictToHtmlConverter` class using `BeautifulSoup`, which allowed for modularity and potential support for additional dictionaries in the future. I also added custom CSS styles to the HTML file for font styling.

### Testing
To ensure the functionality and reliability of the program, I implemented several tests using pytest. The tests were written to ensure that the `WikiScraper` and `DictToHtmlConverter` classes work properly with valid and invalid URLs.

Tests for building the dictionary, saving the images, and building the HTML file were also implemented to ensure they contained valid values. These tests were run successfully, indicating that the program functions as intended.

### CI/CD Pipeline
The project includes a simple CI/CD pipeline that ensures changes to the codebase are thoroughly tested and validated. The pipeline is implemented with a GitHub Actions workflow file named `wiki-scraper.yml` in the `.github/workflows/` directory.
The pipeline is triggered automatically on every push to the main branch. It runs on an Ubuntu environment and performs the following steps:
1. Checks out the project codebase from GitHub.
2. Installs the required dependencies using pip.
3. Runs the test suite using pytest to ensure the project works correctly.
4. Runs the project's main script.
