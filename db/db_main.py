import os
import pandas as pd
from parser.parser_main import ParserMain


class DataBaseMain:
    """
    class which is dedicated to make the basic tests insertion and operations
    """
    def __init__(self) -> None:
        self.parser_main = ParserMain()

    def check_database(self) -> bool:
        """
        Method which is dedicated to develop checking the database
        Input:  
        Output: boolean value which signify that database is developed
        """
        pass

    def produce_insertion(self) -> None:
        """
        Method which is dedicated to insert all values to the database
        Input:  all inserted values
        Output: we created values
        """
        pass

    def produce_basic_values_insertion(self, value_refind:bool=False) -> None:
        """
        Method which is dedicated to transform basic values of the insertion
        Input:  value_refind = boolean value which signify that we need to refill the csv file from the Imdb
        Output: we prepared all possible values and removed them from the 
        """
        if value_refind:
            self.parser_main.produce_dataframe()
        if not os.path.exists(self.parser_main.dataframe_storage):
            self.parser_main.produce_dataframe()
        df_value = pd.read_csv(self.parser_main.dataframe_storage)
        df_value = self.parser_main.produce_dataframe_filtration(df_value)
        return 0