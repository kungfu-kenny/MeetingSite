import os
import pandas as pd
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from parser.parser_main import ParserMain
from db.db_creator import Base
from utillities.check_all import (check_storage, 
                                 produce_storage, 
                                 check_file_presence)
from config import (Db, 
                    Folders, 
                    dictionary_astrology)


class DataBaseMain:
    """
    class which is dedicated to make the basic tests insertion and operations for it
    """
    def __init__(self) -> None:
        self.parser_main = ParserMain()
        self.folder_path = os.path.join(Folders.folder_main, Folders.folder_storage)
        self.file_path = os.path.join(self.folder_path, Db.sqlite_name)
        self.engine = self.produce_engine_file()

    def check_route(self) -> bool:
        """
        Method which is dedicated to develop check of the route of sqlite
        Input:  None; all what we have created
        Output: we developed path to the database and produced everything
        """
        if not check_storage(self.folder_path):
            produce_storage(self.folder_path)
            return False
        if not check_file_presence(self.file_path):
            return False
        return True

    def produce_engine_file(self) -> object:
        """
        Method which is dedicated to create engine from the file
        Input:  None
        Output: we created engine files
        """
        self.check_route()
        return create_engine(self.file_path, echo=True)


    def check_database(self) -> bool:
        """
        Method which is dedicated to develop checking the database
        Input:  
        Output: boolean value which signify that database is developed
        """
        if not self.check_route():
            print('Base is completely new')
        #TODO try here to write the script of the development of it
        return False

    def develop_database(self):
        """
        Method which is dedicated to produce the database it that cases
        Input:  None
        Output: we created values from the db_creator file and produced the database
        """
        try:
            Base.metadata.create_all(self.engine)
        except Exception as e:
            print(f"We faced problems with Base: {e}")
            print('------------------------------------------')

    def return_session(self) -> object:
        """
        Method which is dedicated to develop session
        Input:  None
        Output: We created session of the values
        """
        try:
            Session = sessionmaker(bind=self.engine)
            return Session()
        except Exception as e:
            print(e)
            print('-----------------------------')

    def produce_insertion(self, *args:set) -> None:
        """
        Method which is dedicated to insert all values to the database
        Input:  args = set with used values of the created database:
                    list_astrology = list with the astrology table
                    list_profession = list with the profession table
                    list_users = list with the users table
                    list_id_astrology = list of the connecting user/astrology
                    list_id_professions = list of the connecting id/professions
        Output: we inserted values to the database if it is necessary
        """
        list_astrology, list_profession, list_users, \
            list_id_astrology, list_id_professions = args
        if not self.check_database():
            #TODO add here values of the developing the connection of it
            print(1)
        else:
            print(2)

    def produce_basic_values_insertion(self, value_refind:bool=False) -> None:
        """
        Method which is dedicated to transform basic values of the insertion
        Input:  value_refind = boolean value which signify that 
                                we need to refill the csv file from the Imdb
        Output: we prepared all possible values and removed them from the 
        """
        if value_refind:
            self.parser_main.produce_dataframe()
        if not os.path.exists(self.parser_main.dataframe_storage):
            self.parser_main.produce_dataframe()
        df_value = pd.read_csv(self.parser_main.dataframe_storage)
        df_value = self.parser_main.produce_dataframe_filtration(df_value)
        df_value = pd.read_csv(self.parser_main.dataframe_storage)
        list_astrology = [[index + 1, f.get('name'), 
                        f.get('begin'), f.get('end')]
                        for index, f in enumerate(dictionary_astrology)]    
        list_profession = pd.read_csv(self.parser_main.dataframe_professions).values.tolist()
        list_users = df_value[['id', 'url', 'name', 'image', 
                            'description', 'birthdate', 'deathdate']].values.tolist()
        list_id_astrology = [[value_id, value_astrology] for value_id, value_astrology 
                                            in zip(df_value['id'].values, 
                                                    df_value['astrology_index'].values)]
        list_id_astrology = [[value_id, value_astrology] for value_id, value_astrology 
                                        in list_id_astrology if value_astrology != 0]
        list_id_professions = [[value_id, [int(i) for i in value_id_profession.split('|')]] 
                            for value_id, value_id_profession in zip(df_value['id'].values, 
                                                        df_value['jobs_indexes'].values)]
        self.produce_insertion(list_astrology, list_profession, 
                            list_users, list_id_astrology, list_id_professions)