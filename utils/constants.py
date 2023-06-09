# Wiki Consts
WIKI_URL = 'https://en.wikipedia.org'
WIKI_ANIMAL_LIST_PATH = '/wiki/List_of_animal_names'
WIKI_SORT_TABLE = 'wikitable sortable'
ANIMAL_CELL_INDEX = 0
ADJECTIVE_CELL_INDEX = 5

# HTML Tags
ROW_TAG = 'tr'
CELL_TAG = 'td'
END_LINE_TAG = 'br'
LINK_TAG = 'a'
SUP_TAG = 'sup'
HREF_TAG = 'href'
TITLE_TAG = 'title'
THUMB_TAG = 'thumb'
IMG_TAG = 'img'
SRC_TAG = 'src'
H1_TAG = 'h1'
DIV_TAG = 'div'

# Consts
QUES_MARK = '?'
CLASS = 'class'
TABLE = 'table'
INFOBOX = 'infobox'
HTML_PARSER = 'html.parser'
HTTPS = 'https:'
STYLE = 'style'
INDEX_HTML = 'index.html'
SECOND_PLACE = 1

# Paths
TMP_PATH = '/tmp'

# Exit Code
EXIT_SUCCESS = 0
EXIT_FAIL = 1

# Error Messages
SPECIES_TABLE_NOT_FOUND = 'Error: Failed to find species table. You might use wrong URL '
SPECIES_TABLE_UNINITIALIZED = 'Error: Species table is uninitialized'
PROCESSING_IMG_ERROR = 'Error processing animal:'
PROCESSING_ANIMAL_ADJ_ERROR = 'Error processing row for dictionary'
SOUP_INIT_ERROR = 'Error initialize BeautifulSoup object with the URL: '
DIRECTORY_ERROR = 'is not a directory.'
ACCESS_DIR_ERROR = 'Error accessing directory'
BUILD_DICT_ERROR = 'Error: Failed to build collateral adjective dictionary'
SAVE_IMAGES_ERROR = 'Error: Failed to save animals images'
CONVERT_HTML_ERROR = 'Error: Failed to convert collateral adjectives animals dictionary to html'

# Args Consts
SCRIPT_DESCRIPTIONS = 'Build Collateral adjectives and animals dictionary,' \
                      ' download and save animals images and export the data to html'
BUILD_DICT_FLAG = '--build-dict'
BUILD_DICT_DESCRIPTIONS = 'Build animal dictionary'
SAVE_IMAGES_FLAG = '--save-images'
SAVE_IMAGES_DESCRIPTIONS = 'Save animal images'

# General Info
BUILDING_DICT_INFO = "Building dictionary...\n"
DICT_SUCCESS_INFO = "Dictionary built successfully.\n"
SAVE_IMAGES_INFO = "Download and saving animals images...\n"
IMAGES_SUCCESS_INFO = "Images saved successfully.\n"
HTML_SUCCESS_INFO = "HTML file built successfully.\n"

# HTML CSS Style
CSS_FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"> <link rel="preconnect" ' \
            'href="https://fonts.gstatic.com" crossorigin> <link ' \
            'href="https://fonts.googleapis.com/css2?family=Raleway:wght@200&display=swap" ' \
            'rel="stylesheet"> '

HTML_FILE_HEADER = "<html><head> " + \
                   CSS_FONTS + \
                   "<title></title><style> body { background-color: #f0f0f0; " \
                   "font-family: 'Raleway', sans-serif; } h1 { justify-content: center; " \
                   "text-align: center; font-family: 'Raleway', sans-serif; font-size: " \
                   "36px; margin: 30px 0; } p { font-family: Arial, sans-serif; " \
                   "font-size: 16px; margin: 0; }</style></head><body></body></html> " \

HTML_FILE_TITLE = "Collateral Adjective and Animals Dictionary"

CSS_TABLE_STYLE = 'align-items: center; justify-content: center; display: flex; border-collapse: collapse;'

BORDER_STYLE = 'border: solid rgb(0,0,0,0.5) 1px;'

REQUEST_HEADER_IMG = {
        'User-Agent': 'MyApplication/1.0'
    }

