from initiate import *
import random

class Player:
    def __init__ (self, disc_name, disc_id, ign, rank, role):
        self.disc_name = disc_name
        self.disc_id = disc_id
        self.ign = ign
        self.rank = rank 
        self.role = role
    def build(user,role):
        cell = Players.find(user)
        disc_name = user
        disc_id = Players.row_values(cell.row)[cell.col+2]
        ign = Players.row_values(cell.row)[cell.col+1]
        rank = Players.row_values(cell.row)[cell.col+2]
        role = role
        return Player(disc_name, ign, disc_id, rank, role)

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

