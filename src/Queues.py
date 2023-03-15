from initiate import *

class Player:
    def __init__ (self, disc_id, ign, rank, opgg, role):
        self.disc_id = disc_id
        self.disc_name = "<@"+str(disc_id)+">"
        self.ign = ign
        self.rank = rank 
        self.opgg = opgg
        self.role = role
    def build(user_id,role=None):
        c.execute(f'''SELECT * FROM users WHERE disc_id = {user_id}''')
        player = c.fetchone()
        conn.close
        return Player(player[0], player[1], player[2], player[3], role)

#Queues: 
class Queue:
    def __init__(self):
        self.top_queue = {}
        self.mid_queue = {}
        self.adc_queue = {}
        self.sup_queue = {}

def build_queues():
    c.execute('SELECT server_id FROM servers')
    server_ids = c.fetchall()
    conn.close
    Queues = {}
    regions = ['NA', 'EUW']
    for server in server_ids:
        Queues[server] = {}
        for region in regions:
            Queues[server][region] = Queue()
    return Queues

Queues = build_queues()