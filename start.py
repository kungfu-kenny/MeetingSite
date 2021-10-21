import os
import sys
from db.db_main import DataBaseMain
from models.model_gender import ModelGender

try:
    DataBaseMain().produce_basic_values_insertion()
    ModelGender().produce_values_main()
except Exception as e:
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)
    print('____________________________________')
    print(e)
    print('.......................................')