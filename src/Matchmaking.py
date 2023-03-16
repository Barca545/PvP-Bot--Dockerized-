import random
from initiate import *
import secrets
import string
import time
from Queues import *

#Could these be inside another class as a method maybe include pwd too?
def delta_mmr(laner_1:int, laner_2:int): 
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
    def __init__ (self,primary_players_dict, secondary_players_dict=None,matchid=None): #I don't think these args work
        self = self
        self.primary_players_dict = primary_players_dict
        self.secondary_players_dict = secondary_players_dict
        self.blue_player_1 = primary_players_dict['Blue']
        self.red_player_1 = primary_players_dict['Red']
        self.creator = random.choice([self.blue_player_1,self.red_player_1]).disc_name
        self.pwd = password()
        self.blue_support = Match.check_support(self,'Blue')
        self.red_support = Match.check_support(self,'Red')
        self.diff = Match.find_diff(self)
        self.matchid = matchid
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
    def lane_role(role,server,region,Queues=Queues): # Delete
        if role == 'Top':
            return Queues[server][region].top_queue 
        elif role == 'Mid':
            return Queues[server][region].mid_queue 
        elif role == 'ADC':
            return Queues[server][region].adc_queue 
        elif role == 'Support':
            return Queues[server][region].sup_queue 
    def choose_2nd(first_player,queue):       
        best_laner =  None
        for i in list(queue.keys()):
            test_laner = queue[i]
            if test_laner != first_player:
                if best_laner is None or delta_mmr(first_player.rank,best_laner.rank) > delta_mmr(first_player.rank,test_laner.rank):
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
    def choose_players(queue):             
        first_player = queue[list(queue.keys())[0]]
        for i in range(0,2100,100):
            second_player = Match.choose_2nd(first_player,queue)
            mmr_band = i
            if delta_mmr(first_player.rank,second_player.rank) <= mmr_band or mmr_band == 2000:
                del queue[first_player.disc_id]
                del queue[second_player.disc_id]
                return Match.side_selection(first_player,second_player)
            elif delta_mmr(first_player.rank,second_player.rank) > mmr_band:
                time.sleep(0)                                
    def build_solo(queue): 
        players = Match.choose_players(queue=queue)
        solo_match = Match(players)
        print(solo_match.blue_player_1.disc_id)
        print(solo_match.red_player_1.disc_id)
        c.execute(f'''
        INSERT INTO matches (player_1, player_2)
        VALUES 
        ({solo_match.blue_player_1.disc_id}, {solo_match.red_player_1.disc_id})
        ''')
        conn.commit()
        c.execute(f'''SELECT max(match_number) FROM matches''')
        matchid = c.fetchone()[0]
        solo_match.matchid = matchid
        return solo_match
    def build_duo(adc_queue,sup_queue): 
        ADC_players = Match.choose_players(queue=adc_queue)
        Sup_players = Match.choose_players(queue=sup_queue)
        Bot_match = Match(ADC_players,Sup_players)
        c.execute(f'''
        INSERT INTO matches (player_1, player_2, player_3, player_4)
        VALUES 
        ({Bot_match.blue_player_1}, {Bot_match.red_player_1},{Bot_match.blue_support},{Bot_match.red_support})
        ''')
        conn.commit()
        c.execute(f'''SELECT max(match_number) FROM matches''')
        matchid = c.fetchone()[0]
        Bot_match.matchid = matchid
        return Bot_match