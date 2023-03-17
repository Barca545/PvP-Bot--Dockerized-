import discord 
from discord import Embed
from Matchmaking import Match
from Queues import *
from initiate import *

Embed()
#set up profile
def setupmsg(ign):
    msg = discord.Embed(color=0xc27c0e)
    msg.add_field(name='__**Set up Complete**__',value=f'You are set up {ign}. See you on the Fields of Justice!')
    return msg

#Update profile
def updateupmsg(ign):
    msg = discord.Embed(color=0xc27c0e)
    msg.add_field(name='__**Update Complete**__',value=f'Your profile has been updated {ign}. See you on the Fields of Justice!')
    return msg

#show profile
def profilemsg(disc_name, ign, rank, opgg):
    msg = discord.Embed(title='__**Profile**__',color=0xc27c0e)
    msg.add_field(name='__User__',value=disc_name,inline=False)
    msg.add_field(name='IGN',value=ign,inline=False)
    msg.add_field(name='__Rank__',value=rank,inline=False)
    msg.add_field(name='__OP.GG__',value=opgg,inline=False)
    return msg
# Join queue
def updatequeuemsg(user_id,role,action):
    msg = discord.Embed(color=0xc27c0e)
    msg.add_field(name=f'**{role} queue update**',value=f'<@{user_id}> has {action} the queue',inline=True)
    return msg

#show queue
def showqmsg(server,region,lane): 
    tops = Queues[server][region].top_queue.keys()
    topnames = [f'<@{player}>' for player in tops]
    mids = Queues[server][region].mid_queue.keys()
    midnames=[f'<@{player}>' for player in mids]
    adcs = Queues[server][region].adc_queue.keys()
    adcnames = [f'<@{player}>' for player in adcs]
    supports = Queues[server][region].sup_queue.keys()
    supportnames =[f'<@{player}>' for player in supports]
    if lane == 'Bottom Lane':       
        msg = discord.Embed(title='__**Bottom Lane Queue**__',color=0xc27c0e)
        msg.add_field(name='**Adcs**', value=f'{str(len(adcs))} players in the ADC queue: ' + ', '.join(adcnames),inline=False)
        msg.add_field(name='**Supports**', value=f'{str(len(supports))} players in the support queue: '+', '.join(supportnames),inline=False)
        return msg
    elif lane == 'Middle Lane':
        msg = discord.Embed(title='__**Middle Lane Queue**__',color=0xc27c0e)
        msg.add_field(name='**Middle Laners**', value=f'{str(len(mids))} players in the middle lane queue: ' + ', '.join(midnames))
        return msg
    elif lane == 'Top Lane':
        msg = discord.Embed(title='__**Top Lane Queue**__',color=0xc27c0e)
        msg.add_field(name='**Top laners**', value=f'{str(len(tops))} players in the Top lane queue: ' + ', '.join(topnames))
        return msg
    else:
        msg = discord.Embed(title='__**All Queues**__',color=0xc27c0e)
        msg.add_field(name='**Top laners**', value=str(len(tops))+' players in the top lane queue: ' + ', '.join(topnames),inline=False)
        msg.add_field(name='**Middle Laners**', value=str(len(mids))+' players in the middle lane queue: ' + ', '.join(midnames),inline=False)
        msg.add_field(name='**Adcs**', value=str(len(adcs))+' players in the ADC queue: ' + ', '.join(adcnames))
        msg.add_field(name='**Supports**', value=str(len(supports))+' players in the support queue: ' + ', '.join(supportnames),inline=False)
        return msg

#pop queue     
async def popmsg(match:Match,channel_id:int,lane:str):     
    users = list(filter(None,[match.blue_player,match.red_player,match.blue_support,match.red_support]))
    for j in users: 
        user_id = bot.get_user(int(j.disc_id))
    def msg(lane:str):
        message = discord.Embed(title = '__**NEW MATCH**__',color=0xc27c0e)
        message.add_field(name='__Match ID__', value=f'{match.matchid}',inline=False)
        message.add_field(name='__Lobby Creator__', value= match.creator,inline=False)
        message.add_field(name='__Lobby Type__', value=lane,inline=False)
        message.add_field(name='__Lobby Name__', value=f'PVP{match.matchid}',inline=False)
        message.add_field(name='__Password__', value=match.pwd,inline=False)
        if match.secondary_players_dict is None:
            message.add_field(name=f'__Blue side {match.blue_player.role}__', value=f'[{match.blue_player.ign}]({match.blue_player.opgg})',inline=True)
            message.add_field(name=f'__Red side {match.red_player.role}__', value=f'[{match.red_player.ign}]({match.red_player.opgg})',inline=True)
            message.add_field(name='__Elo Difference__', value=str(match.diff),inline=False)
        elif match.secondary_players_dict is not None:
            message.add_field(name='__Blue side__',
            value=
            f'Blue {match.blue_player.role}: [{match.blue_player.ign}]({match.blue_player.opgg})'
            +'\n'+
            f'Blue {match.blue_support.role}: [{match.blue_support.ign}]({match.blue_support.opgg})',inline=True)
            message.add_field(name='__Red side__',
            value=
            f'Blue {match.blue_player.role}: [{match.red_player.ign}]({match.red_player.opgg})'
            +'\n'+
            f'Blue {match.red_support.role}: [{match.red_support.ign}]({match.red_support.opgg})',inline=True)
            message.add_field(name='__Elo Difference__', value=str(match.diff),inline=False)      
        return message
    message = msg(lane=lane)
    channel=bot.get_channel(channel_id)
    recipients = [channel,user_id]
    for recipient in recipients:   
        await recipient.send(embed=message)

#record match
def matchmessage(match_id,winner):
    msg = discord.Embed(title=f'Match {match_id} recorded',color=0xc27c0e)
    msg.add_field(name=f'Winner {winner} side,',value='Congratulations!')
            