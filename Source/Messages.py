import discord 
from Queues import *

#show queue
def showqmsg(server,region,lane=None): 
    if lane == 'Bottom Lane':
        adcs = Queues[server][region].adc_queue.keys()
        supports = Queues[server][region].sup_queue.keys()
        msg = discord.embed(title='__**Bottom Lane Queue**__')
        msg.add_field(name='**Adcs**', value=str(len(adcs))+' players in the ADC queue: ' + ', '.join(adcs))
        msg.add_field(name='**Supports**', value=str(len(supports))+' players in the support queue: ' + ', '.join(supports))
        return msg
    elif lane == 'Middle Lane':
        mids = Queues[server][region].mid_queue.keys()
        msg = discord.embed(title='__**Middle Queue**__')
        msg.add_field(name='**Middle Laners**', value=str(len(mids))+' players in the middle lane queue: ' + ', '.join(mids))
        return msg
    elif lane == 'Top Lane':
        tops = Queues[server][region].top_queue.keys()
        msg = discord.embed(title='__**Middle Queue**__')
        msg.add_field(name='**Top laners**', value=str(len(tops))+' players in the middle lane queue: ' + ', '.join(tops))
        return msg
    else:
        tops = Queues[server][region].top_queue.keys()
        mids = Queues[server][region].mid_queue.keys()
        adcs = Queues[server][region].adc_queue.keys()
        supports = Queues[server][region].sup_queue.keys()
        msg = discord.embed(title='__**All Queues**__')
        msg.add_field(name='**Middle Laners**', value=str(len(mids))+' players in the middle lane queue: ' + ', '.join(mids))
        msg.add_field(name='**Top laners**', value=str(len(tops))+' players in the middle lane queue: ' + ', '.join(tops))
        msg.add_field(name='**Adcs**', value=str(len(adcs))+' players in the ADC queue: ' + ', '.join(adcs))
        msg.add_field(name='**Supports**', value=str(len(supports))+' players in the support queue: ' + ', '.join(supports))
        return msg

#pop queue     
async def popmsg(users,match:Match,DM:bool,channel:int):     
    for j in users: 
        user_id = bot.get_user(j.disc_id)
    def msg():
        message = discord.embed(title = 'Lobby Name: ' + match.creator + "'s Lobby")
        message.add_field(name='Lobby Creator:', value = match.creator)
        message.add_field(name='Lobby Type:', value = match.lane)
        message.add_field(name='Password: ' + match.pwd)
        if match.secondary_players_dict is None:
            message.add_field(name='Blue side '+match.blue_player_1.role + ':', value=match.blue_player_1.disc_name,inline=True)
            message.add_field(name='Red side '+match.red_player_1.role + ':', value=match.red_player_1.disc_name,inline=True)
            message.add_field(name='Elo Difference:', value=str(match.diff))
        elif match.secondary_players_dict is not None:
            message.add_field(name='Blue side '+match.blue_player_1.role + ':', value=match.blue_player_1.disc_name,inline=True)
            message.add_field(name='Blue side '+match.blue_support.role + ':', value=match.blue_support.disc_name,inline=True)
            message.add_field(name='Red side '+match.red_player_1.role + ':', value=match.red_player_1.disc_name,inline=True)
            message.add_field(name='Red side '+match.red_support.role + ':', value=match.red_support.disc_name,inline=True)
            message.add_field(name='Elo Difference:', value=str(match.diff))      
        return message
    message = msg()
    if DM == True:    
        await user_id.send(message)
    if channel is not None:       
        channel = bot.get_channel(channel) 
        await channel.send(message)  