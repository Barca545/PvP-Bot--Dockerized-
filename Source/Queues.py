from Matchmaking import *
from Bot_initiate import *
import random

class Player:
    def __init__ (self, disc_name, disc_id, ign, rank, role, champ):
        self.disc_name = disc_name
        self.disc_id = disc_id
        self.ign = ign
        self.rank = rank 
        self.role = role
        self.champ = champ
    def build(user,role,db):
        cell = db.find(user)
        disc_name = user
        disc_id = db.row_values(cell.row)[cell.col+2]
        ign = db.row_values(cell.row)[cell.col+1]
        rank = db.row_values(cell.row)[cell.col+2]
        role = role
        champ = str(random.choice(db.row_values(cell.row)[cell.col+5:]))
        return Player(disc_name, ign, disc_id, rank, role, champ)

#Queues: Remove dummy players
dummy_supp_1 = Player('Test1#303030', 221397446066962435, 'Test 1', 1000, 'ADC', 'Lulu',  )
dummy_supp_2 = Player('Test2#303030',221397446066962435,'Test 3', 3000, 'Mid', 'Soraka')
dummy_adc_1 = Player('Test3#303030',221397446066962435, 'Test 3', 4500, 'Support','MF')

#Top_queue = {'Test1#303030': dummy_supp_1,'Test2#303030': dummy_supp_2, 'Test3#303030':dummy_adc_1}
#Mid_queue = {'Test1#303030': dummy_supp_1,'Test2#303030': dummy_supp_2}
#ADC_queue = {'Test3#303030': dummy_adc_1, 'Test1#303030':dummy_supp_1 } 
#Sup_queue = {'Test1#303030': dummy_supp_1,'Test2#303030': dummy_supp_2}

class Queue:
    def __init__(self):
        self.top_queue = {}
        self.mid_queue = {}
        self.adc_queue = {}
        self.sup_queue = {}

def build_queues():
    server_ids = Guilds.col_values(col=1)[1:] 
    Queues = {}
    regions = ['NA', 'EUW']
    for server in server_ids:
        Queues[server] = {}
        for region in regions:
            Queues[server][region] = Queue()
    print(Queues)
    return Queues
Queues = build_queues()

