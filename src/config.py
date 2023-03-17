from configparser import ConfigParser
from dotenv import load_dotenv,find_dotenv 
import os

load_dotenv(find_dotenv())
db_connect_path = os.environ.get("DB")

def config(filename=f'{db_connect_path}', section='postgresql'):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    # get section, default to postgresql
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception('Section {0} not found in the {1} file'.format(section, filename))
    return db

