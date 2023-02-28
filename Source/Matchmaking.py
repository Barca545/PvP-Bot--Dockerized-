import random
from Bot_initiate import *
import secrets
import string
import time
from Queues import *

#Could these be inside another class as a method maybe include pwd too?
def delta_mmr(laner_1, laner_2): 
    return abs(laner_1 - laner_2)
    
def password():
        pwd = ''
        for i in range(13):
            pwd += secrets.choice(string.ascii_letters + string.digits)
        return pwd

def heads_or_tails():
    coin = ['H','T']
    return random.choice(coin)

class Match:           
    def __init__ (self,lane:str,primary_players_dict, secondary_players_dict=None): #I don't think these args work
        self = self
        self.lane = lane
        self.primary_players_dict = primary_players_dict
        self.secondary_players_dict = secondary_players_dict
        self.blue_player_1 = primary_players_dict['Blue']
        self.red_player_1 = primary_players_dict['Red']
        self.creator = random.choice([self.blue_player_1,self.red_player_1]).disc_name
        self.pwd = password()
        self.blue_support = Match.check_support(self,'Blue')
        self.red_support = Match.check_support(self,'Red')
        self.diff = Match.find_diff(self)
    def check_support(self,side:str):
        if self.secondary_players_dict != None:
            return self.secondary_players_dict[side]
        else:
            return None  
    def find_diff(self):
        if self.secondary_players_dict != None:
            duodiff = delta_mmr(self.primary_players_dict['Blue'].rank+self.secondary_players_dict['Blue'].rank,self.primary_players_dict['Red'].rank+self.secondary_players_dict['Red'].rank)
            return duodiff
        else:
            solodiff = delta_mmr(self.primary_players_dict['Blue'].rank,self.primary_players_dict['Red'].rank)
            return solodiff
    def lane_role(role,server,region):
        if role == 'Top':
            return Queues[server][region].top_queue 
        elif role == 'Mid':
            return Queues[server][region].mid_queue 
        elif role == 'ADC':
            return Queues[server][region].adc_queue 
        elif role == 'Support':
            return Queues[server][region].sup_queue 
    def choose_2nd(blue_laner,lane_queue):       
        best_laner =  None
        for i in list(lane_queue.keys()):
            test_laner = lane_queue[i]
            if test_laner != blue_laner:
                if best_laner is None or delta_mmr(blue_laner.rank,best_laner.rank) > delta_mmr(blue_laner.rank,test_laner.rank):
                    best_laner = test_laner
        return best_laner 
    def side_selection(first_player, second_player):
        players_dict = {'Blue':None, 'Red':None}
        if first_player.rank > second_player.rank:
            players_dict['Blue'] = second_player
            players_dict['Red'] = first_player
        elif second_player.rank > first_player.rank:
            players_dict['Blue'] = first_player
            players_dict['Red'] = second_player
        else:
            if heads_or_tails() == 'H':
                players_dict['Blue'] = second_player
                players_dict['Red'] = first_player
            elif heads_or_tails() == 'F':
                players_dict['Blue'] = first_player
                players_dict['Red'] = second_player
        return players_dict   
    def choose_players(role,queue,server,region):        
        queue = Match.lane_role(role,server,region)        
        first_player = queue[list(queue.keys())[0]]
        for i in range(0,2100,100):
            second_player = Match.choose_2nd(first_player,queue)
            mmr_band = i
            if delta_mmr(first_player.rank,second_player.rank) <= mmr_band or mmr_band == 2000:
                del queue[first_player.disc_name]
                del queue[second_player.disc_name]
                return Match.side_selection(first_player,second_player)
            elif delta_mmr(first_player.rank,second_player.rank) > mmr_band:
                time.sleep(0) #make 30 in final deploy                                    

def choose_solo(role:str,server,region): #This probably needs to be an async function.
    players = Match.choose_players(role,server,region)
    solo_match = Match(role,players)
    return solo_match
def choose_duo(server,region): #This probably needs to be an async function.
    ADC_players = Match.choose_players('ADC',server,region)
    Sup_players = Match.choose_players('Support',server,region)
    Bot_match = Match('Bot',ADC_players,Sup_players)
    return Bot_match
