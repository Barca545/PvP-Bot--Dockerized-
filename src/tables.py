import psycopg2
from config import config

def create_tables():
    commands = ('''
    CREATE TABLE IF NOT EXISTS users
        (disc_id BIGINT PRIMARY KEY UNIQUE, 
        ign TEXT NOT NULL UNIQUE, 
        rank INTEGER NOT NULL, 
        opgg TEXT NOT NULL UNIQUE)''',

    '''CREATE TABLE IF NOT EXISTS servers
    (server_id BIGINT PRIMARY KEY, channel_id BIGINT)''',                                                                                                                                                                                                                                     

    '''CREATE TABLE IF NOT EXISTS matches
    (match_number SERIAL PRIMARY KEY, 
    player_1 BIGINT, 
    player_2 BIGINT, 
    player_3 BIGINT, 
    player_4 BIGINT, 
    winner BIGINT)                                                                                                                                                                                                                                  
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