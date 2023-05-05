
# WikiScraper
This is a Python program that scrapes data from the Wikipedia page https://en.wikipedia.org/wiki/List_of_animal_names, and outputs all of the “collateral adjectives” and all of the “animals” which belong to it. It also downloads the picture of each animal into /tmp/ and adds a local link when displaying the animals. Finally, it outputs the results to an HTML file.

## Requirements
* Python 3.6 or higher <br>
* Requests <br>
* BeautifulSoup 4

## Usage
1. Clone the repository: git clone https://github.com/haim5987/wiki-scraper.git
2. Install the required packages: ```pip install -r requirements.txt```
3. Run the main program: ```python3 main.py``` <br><br>
The program will output the results to both the console and an HTML file named index.html in the project root directory. Additionally, it downloads images of the animals to the /tmp/ directory.

# Testing
To run the tests, navigate to the tests/ directory and run the following command:
``` pytest ```
