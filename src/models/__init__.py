from .player import Player
from .course import Course, Club, Hole
from .tournament import Tournament
from .scorecard import Scorecard
from pony.orm import *
import os
from datetime import datetime
from .model import db
from time import sleep

# !!! Hard refreshing the database will cause you to reset your database !!!
# Data is saved but is placed in the backups folder. All analysis will be done off the new db
def connect_to_sqlite(hard_refresh: bool = False, database_file: str = 'pga.sqlite', sql_debug: bool = False):
    create_db = False
    # path calculated from run.py
    db_file_path = f'../data/{database_file}'

    if os.path.exists(db_file_path):
        print("Found Database...")
        if (hard_refresh): 
            print("Hard Refreshing Database...")
            now = datetime.now().timestamp()
            os.rename(db_file_path, f'../data/backups/backup_{now}.sqlite')
            create_db = True
    else:
        create_db = True
    
    sleep(3)
    print(f'Connecting to database ../{db_file_path}')

    db.bind('sqlite', f'../{db_file_path}', create_db)
    set_sql_debug(sql_debug)
    db.generate_mapping(create_tables=True)

