from initiate import *
from sqlfunctions import sqlplayer,sqlservers

class Player:
    def __init__ (self, disc_id, ign, rank, opgg, role):
        self.disc_id = disc_id
        self.disc_name = f'<@{str(disc_id)}>' 
        self.ign = ign
        self.rank = rank 
        self.opgg = opgg
        self.role = role
    def build(user_id,role=None):
        player = sqlplayer(user_id)
        return Player(player[0], player[1], player[2], player[3], role)

#Queues: 
regions = ['NA', 'EUW']
class Queue:
    def __init__(self):
        self.top_queue = {}
        self.mid_queue = {}
        self.adc_queue = {}
        self.sup_queue = {}
    def build():
        servers = sqlservers()
        print(servers)
        Queues = {}
        for server in servers:
            server_id = server[0]
            Queues[server_id] = {}
            for region in regions:
                Queues[server_id][region] = Queue()
        return Queues
    def add_server(server_id):
        Queues[server_id] = {}
        for region in regions:
            Queues[server_id][region] = Queue()
            return Queues        
Queues = Queue.build()


