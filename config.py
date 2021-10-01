import os

default_chunk = 10
user_numbers = 1000000

class Folders:
    folder_main = os.getcwd()
    folder_storage = 'storage'

class Kinopoisk:
    link = 'https://www.kinopoisk.ru'
    link_name = 'name'
    semaphore = 10
    df_name = 'names_kinopoisk.csv'