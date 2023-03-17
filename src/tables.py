import psycopg2
from config import config

def create_tables():
    commands = ('''
    CREATE TABLE IF NOT EXISTS users
        (disc_id TEXT PRIMARY KEY UNIQUE, 
        ign TEXT NOT NULL UNIQUE, 
        rank INTEGER NOT NULL, 
        opgg TEXT NOT NULL UNIQUE)''',

    '''CREATE TABLE IF NOT EXISTS servers
    (server_id TEXT PRIMARY KEY, channel_id TEXT)''',                                                                                                                                                                                                                                     

    '''CREATE TABLE IF NOT EXISTS matches
    (match_number SERIAL PRIMARY KEY, 
    player_1 TEXT, 
    player_2 TEXT, 
    player_3 TEXT, 
    player_4 TEXT, 
    winner TEXT)                                                                                                                                                                                                                                  
    ''') 
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
if __name__ == '__main__':
    create_tables()