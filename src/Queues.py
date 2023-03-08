from initiate import *
import random

class Player:
    def __init__ (self, disc_name, disc_id, ign, rank, role,champ):
        self.disc_name = disc_name
        self.disc_id = disc_id
        self.ign = ign
        self.rank = rank 
        self.role = role
        self.champ = champ
    def build(user,role,db,champ):
        cell = db.find(user)
        disc_name = user
        disc_id = db.row_values(cell.row)[cell.col+2]
        ign = db.row_values(cell.row)[cell.col+1]
        rank = db.row_values(cell.row)[cell.col+2]
        role = role
        if champ == None:
            champ = str(random.choice(db.row_values(cell.row)[cell.col+5:]))
        else:
            champ==champ 
        return Player(disc_name, ign, disc_id, rank, role, champ)

#Queues: 
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
    return Queues

Queues = build_queues()

