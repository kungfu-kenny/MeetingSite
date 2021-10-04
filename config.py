import os
from attr import dataclass
from dotenv import load_dotenv


load_dotenv()
link_webdriver = os.getenv("LINK_WEBDRIVER")

default_chunk = 10
user_numbers = 1000000

@dataclass
class Folders:
    folder_main = os.getcwd()
    folder_storage = 'storage'

@dataclass
class Imdb:
    link = 'https://www.imdb.com'
    link_name = 'name'
    semaphore = 10
    link_name_add = 'nm'
    df_name = 'names_imdb.csv'