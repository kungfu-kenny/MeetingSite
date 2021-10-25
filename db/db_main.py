import os
import pandas as pd
from pprint import pprint
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from parser.parser_main import ParserMain
from db.db_creator import  (Base,
                            User,
                            Gender,
                            Astrology,
                            Profession,
                            association_table_user_gender,
                            association_table_user_astrology,
                            association_table_user_profession)
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
        self.session = None
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
        return create_engine(f"sqlite:///{self.file_path}", echo=True)
        
    def check_database(self) -> bool:
        """
        Method which is dedicated to develop checking the database
        Input:  
        Output: boolean value which signify that database is developed
        """
        check_route = self.check_route()
        if not check_route:
            print('Base is completely new')
            self.develop_database()
        return bool(self.session)

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

    def close_session(self) -> None:
        """
        Method which is dedicated to close session of the sql alchemy
        Input:  None values
        Output: we close this session
        """
        if self.session:
            self.session.close()

    def make_mass_insertion(self, value_list:list) -> None:
        """
        Method for inserting objects at one iterations
        Input:  value_list = list of the selected objects
        Output: we commited to the database
        """
        if value_list:
            self.session.add_all(value_list)
            self.session.commit()

    def make_basic_insertion(self, value_list:list) -> None:
        """
        Method which is dedicated to insert basic without add_all command
        Input:  value_list = list of the commands
        Output: we inserted values of it
        """
        if value_list:
            for f in value_list:
                self.session.execute(f)
                self.session.commit()

    def produce_insertion_model_gender(self, list_gender:list, list_gender_id:list) -> None:
        """
        Method which is dedicated to make insertion of the selected values
        Input:  list_gender = set of the values to insert genders
                list_gender_id = list of lists of the values which is innerconnected to it
        Output: we developed insertion values which developed 
        """
        if not self.check_database():
            self.session = self.return_session()
        gender_used = [f[0] for f in self.session.query(Gender.id).all()]
        list_gender = [[id, name] for id, name in list_gender if id not in gender_used]
        gender_specified = [f[0] for f in self.session.query(User.id).filter(
                            association_table_user_gender.c.id_user== User.id).all()]
        list_gender_id = [[id_user, id_gender] for id_user, id_gender 
                            in list_gender_id if id_user not in gender_specified]
        objects = [Gender(id=id, name=name) for id, name in list_gender]
        self.make_mass_insertion(objects)
        objects = [association_table_user_gender.insert().values(id_user=id_user, id_gender=id_gender)
                    for id_user, id_gender in list_gender_id]
        self.make_basic_insertion(objects)
        self.close_session()
        print('finished')

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
            self.session = self.return_session()
        
        list_id_astrologies = [[list_users[i-1][1], list_ids] for i, list_ids in list_id_astrology]
        list_id_profession = [[list_users[i-1][1], list_ids] for i, list_ids in list_id_professions]
        list_users = [[i, link, name, link_image, description, date_begin, date_end]
                for i, link, name, link_image, description, date_begin, date_end 
                in list_users  if link not in [f[0] for f in self.session.query(User.link).all()]]
        list_id_astrologies = [[list_user, list_ids] for list_user, list_ids in list_id_astrologies
                if list_user in [f[1] for f in list_users]]
        list_id_profession = [[list_user, list_ids] for list_user, list_ids in list_id_professions
                if list_user in [f[1] for f in list_users]]
        
        objects = [User(name=name, link=link, description=description, 
                        date_birth=date_birth, date_death=date_death, link_image=link_image)
                    for _, link, name, link_image, description, date_birth, date_death in list_users]
        self.make_mass_insertion(objects)
        
        list_astrology = [[i, name, date_begin, date_end] for i, name, date_begin, date_end 
                            in list_astrology if name 
                        not in [f[0] for f in self.session.query(Astrology.name).all()]]        
        objects = [Astrology(id=i, name=name, date_begin=date_begin, date_end=date_end)
                    for i, name, date_begin, date_end in list_astrology]
        self.make_mass_insertion(objects)

        list_profession = [[i, name] for i, name in list_profession if name not in 
                            [f[0] for f in self.session.query(Profession.name).all()]]
        objects = [Profession(name=name) for _, name in list_profession]
        self.make_mass_insertion(objects)

        ids_users = [f[0] for f in self.session.query(User.id).filter(
                        User.link.in_([f[0] for f in list_id_astrologies])).all()]
        list_id_astrologies = [[id_user, id_astrology] for 
                                id_user, (_, id_astrology) in zip(ids_users, list_id_astrologies)]
        objects = [association_table_user_astrology.insert().values(id_user=id_user, id_astrology=int(id_astrology))
                    for id_user, id_astrology in list_id_astrologies]
        self.make_basic_insertion(objects)
        
        ids_users = [f[0] for f in self.session.query(User.id).filter(
                        User.link.in_(f[0] for f in list_id_profession)).all()]
        list_id_professions = []
        for (_, id_professions), ids_user in zip(list_id_profession, ids_users):
            for id_profession in id_professions:
                list_id_professions.append([ids_user, id_profession])
        objects = [association_table_user_profession.insert().values(id_user=ids_user, id_profession=id_profession)
                    for ids_user, id_profession in list_id_professions]
        self.make_basic_insertion(objects)
        self.close_session()
        
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
        #TODO remove if statement
        # if len(df_value) < user_numbers:
        #     self.parser_main.produce_dataframe()
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
                                                    df_value['jobs_indexes'].values) 
                                                    if isinstance(value_id_profession, str)]
        self.produce_insertion(list_astrology, list_profession, 
                            list_users, list_id_astrology, list_id_professions)
        self.close_session()