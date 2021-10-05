from parser.parser_main import ParserMain
from db.db_main import DataBaseMain

try:
    # ParserMain().produce_dataframe()
    DataBaseMain().produce_basic_values_insertion()
except Exception as e:
    print(e)
    print('.......................................')