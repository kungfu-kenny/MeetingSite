import os
from attr import dataclass
from dotenv import load_dotenv


load_dotenv()

link_webdriver = os.getenv("LINK_WEBDRIVER")
link_model_gender = os.getenv("LINK_MODEL_GENDER")

default_chunk = 10
user_numbers = 1000000

@dataclass
class Db:
    sqlite_name = 'sqlite.db'
    echo = False

@dataclass
class ProductionConfig(object):
    host = '0.0.0.0'
    port = 5001
    debug = True
    # SECRET_KEY = ''

@dataclass
class Models:
    folder_models = 'models'
    face_proto = 'opencv_face_detector.pbtxt'
    face_model = 'opencv_face_detector_uint8.pb'
    gender_proto = 'gender_deploy.prototxt'
    gender_model = 'gender_net.caffemodel'
    gender_name_archive = 'gad.zip'
    
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
    
@dataclass
class DataFrames:
    df_name = 'names_imdb.csv'
    df_name_proffesions = 'professions.csv'
    df_name_astrology = 'astrology.csv'

dictionary_gender = {
    'Male': 1,
    'Female': 2,
    'Unknown': 3,
}

dictionary_astrology = [
    {
        'name': 'The Ram',
        'begin': '03.21',
        'end': '04.19',
    },
    {
        'name': 'The Bull',
        'begin': '04.20',
        'end': '05.20',
    },
    {
        'name': 'The Twins',
        'begin': '05.21',
        'end': '06.21',
    },
    {
        'name': 'The Crab',
        'begin': '06.22',
        'end': '07.22',
    },
    {
        'name': 'The Lion',
        'begin': '07.23',
        'end': '08.22',
    },
    {
        'name': 'The Maiden',
        'begin': '08.23',
        'end': '09.22',
    },
    {
        'name': 'The Scales',
        'begin': '09.23',
        'end': '10.22',
    },
    {
        'name': 'The Scorpion',
        'begin': '10.23',
        'end': '11.22',
    },
    {
        'name': 'The Archer',
        'begin': '11.23',
        'end': '12.21',
    },
    {
        'name': 'The Goat',
        'begin': '12.22',
        'end': '01.19',
    },
    {
        'name': 'The Water-bearer',
        'begin': '01.20',
        'end': '02.18',
    },
    {
        'name': 'The Fish',
        'begin': '02.19',
        'end': '03.20',
    },
]

# config = {
#     'dev': Website,
# }