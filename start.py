from parser.parser_main import ParserMain

try:
    ParserMain().produce_dataframe()
except Exception as e:
    print(e)
    print('.......................................')