import os
import time
import asyncio
import pandas as pd
from parser.parser_kinopoisk import ParseKinopoisk
from utillities.check_all import (check_storage,
                                 produce_chunks,
                                 produce_storage,
                                 check_file_presence)
from config import (Folders, 
                    Kinopoisk,
                    user_numbers)


class ParserMain:
    """
    class which is dedicated to develop values of the parser and store it as a dataframe
    """
    def __init__(self) -> None:
        self.folder_storage = os.path.join(Folders.folder_main, Folders.folder_storage)
        self.dataframe_storage = os.path.join(self.folder_storage, Kinopoisk.df_name)

    def produce_absent(self) -> list:
        """
        Method which is dedicated to produce values of the id values which were not used
        Input:  None
        Output: list with values which were previously non-created
        """
        return [[]]

    def produce_dataframe(self) -> pd.DataFrame:
        """
        Method which is dedicated to produce values of it
        Input:  None
        Output: we returned values of it
        """
        begin = time.time()
        if not check_storage(self.folder_storage):
            produce_storage(self.folder_storage)
        if check_storage(self.folder_storage) and not check_file_presence(self.dataframe_storage):
            #TODO we are here now
            values_id = [i+1 for i in range(user_numbers)]
            values_id = produce_chunks(values_id)
        else:
            values_id = self.produce_absent()
        parse_kinopoisk = ParseKinopoisk()
        for value_id in values_id[:1]:
            loop = asyncio.get_event_loop()
            value_list = loop.run_until_complete(parse_kinopoisk.produce_main(value_id))
        print(f"{time.time() - begin} seconds")
        print('cccccccccccccccccccccccccccccccccccccccccccccccccccccccc')