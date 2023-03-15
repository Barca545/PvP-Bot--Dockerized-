from initiate import *

class Player:
    def __init__ (self, disc_id, ign, rank, opgg, role):
        self.disc_id = disc_id
        self.disc_name = f'<@{str(disc_id)}>'
        self.ign = ign
        self.rank = rank 
        self.opgg = opgg
        self.role = role
    def build(user_id,role=None):
        c.execute(f'''SELECT * FROM users WHERE disc_id = {user_id}''')
        player = c.fetchone()
        return Player(player[0], player[1], player[2], player[3], role)

#test = Player.build(221397446066962435)

#Queues: 
class Queue:
    def __init__(self):
        self.top_queue = {}
        self.mid_queue = {}
        self.adc_queue = {}
        self.sup_queue = {}
    def build():
        c.execute('SELECT server_id FROM servers')
        servers = c.fetchall()
        Queues = {}
        regions = ['NA', 'EUW']
        for server in servers:
            server_id = server[0]
            Queues[server_id] = {}
            for region in regions:
                Queues[server_id][region] = Queue()
        print(Queues)
        return Queues
    def add_server(server_id):
        regions = ['NA', 'EUW']
        Queues[server_id] = {}
        for region in regions:
            Queues[server_id][region] = Queue()
            print(Queues)
            return Queues
        
Queues = Queue.build()

