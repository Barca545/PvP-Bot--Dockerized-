import psycopg2
from config import config
from Matchmaking import Match

def sqlmatch(winner,match_id):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        c = conn.cursor()
        c.execute(f'''
        UPDATE matches 
        SET winner='{winner}'
        WHERE match_number='{match_id}'
        ''')
        conn.commit()
        c.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def sqlservers():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        c = conn.cursor()
        c.execute(f'''SELECT server_id, channel_id FROM servers''')
        servers = c.fetchall()
        conn.commit()
        c.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return servers

def sqlupdateprof(user_id,ign,mmr,opgg_link):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        c = conn.cursor()
        c.execute(f'''
        UPDATE users 
        SET ign='{ign}', rank='{mmr}', opgg='{opgg_link}'
        WHERE disc_id='{user_id}'
        ''')
        conn.commit()
        c.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def sqlsetup(user_id,ign,mmr,opgg_link):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        c = conn.cursor()
        c.execute(f'''
        INSERT INTO users (disc_id, ign, rank, opgg)
        VALUES 
        ({user_id},'{ign}','{mmr}', '{opgg_link}')
        ''')
        conn.commit()
        c.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def sqlsetchannel(server_id,channel_id):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        c = conn.cursor()
        c.execute(f'''INSERT INTO servers (server_id, channel_id) VALUES ({server_id}, {channel_id})''')
        conn.commit()
        c.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def matchupdate(Bot_match:Match):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        c = conn.cursor()
        c.execute(f'''
        INSERT INTO matches (player_1, player_2, player_3, player_4)
        VALUES 
        ({Bot_match.blue_player_1}, {Bot_match.red_player_1},{Bot_match.blue_support},{Bot_match.red_support})
        ''')
        conn.commit()
        c.execute(f'''SELECT max(match_number) FROM matches''')
        matchid = c.fetchone()[0]
        c.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return matchid

def sqlplayer(user_id):    
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        c = conn.cursor()
        c.execute(f'''SELECT * FROM users WHERE disc_id = {user_id}''')
        conn.commit()
        c.execute(f'''SELECT max(match_number) FROM matches''')
        player = c.fetchone()
        c.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return player

def sqlqueue(user_id):
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        c = conn.cursor()
        c.execute(f'''SELECT * FROM users WHERE disc_id = {user_id}''')
        conn.commit()
        c.execute('SELECT server_id FROM servers')
        servers = c.fetchall()
        c.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return servers