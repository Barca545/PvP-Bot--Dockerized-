import discord 
from Queues import *
from Matchmaking import Match

#show queue
def showqmsg(server,region,lane): 
    if lane == 'Bottom Lane':
        adcs = Queues[server][region].adc_queue.keys()
        supports = Queues[server][region].sup_queue.keys()
        msg = discord.Embed(title='__**Bottom Lane Queue**__')
        msg.add_field(name='**Adcs**', value=str(len(adcs))+' players in the ADC queue: ' + ', '.join(adcs),inline=False)
        msg.add_field(name='**Supports**', value=str(len(supports))+' players in the support queue: ' + ', '.join(supports),inline=False)
        return msg
    elif lane == 'Middle Lane':
        mids = Queues[server][region].mid_queue.keys()
        msg = discord.Embed(title='__**Middle Queue**__')
        msg.add_field(name='**Middle Laners**', value=str(len(mids))+' players in the middle lane queue: ' + ', '.join(mids))
        return msg
    elif lane == 'Top Lane':
        tops = Queues[server][region].top_queue.keys()
        msg = discord.Embed(title='__**Middle Queue**__')
        msg.add_field(name='**Top laners**', value=str(len(tops))+' players in the middle lane queue: ' + ', '.join(tops))
        return msg
    else:
        tops = Queues[server][region].top_queue.keys()
        mids = Queues[server][region].mid_queue.keys()
        adcs = Queues[server][region].adc_queue.keys()
        supports = Queues[server][region].sup_queue.keys()
        msg = discord.Embed(title='__**All Queues**__')
        msg.add_field(name='**Middle Laners**', value=str(len(mids))+' players in the middle lane queue: ' + ', '.join(mids),inline=False)
        msg.add_field(name='**Top laners**', value=str(len(tops))+' players in the middle lane queue: ' + ', '.join(tops),inline=False)
        msg.add_field(name='**Adcs**', value=str(len(adcs))+' players in the ADC queue: ' + ', '.join(adcs))
        msg.add_field(name='**Supports**', value=str(len(supports))+' players in the support queue: ' + ', '.join(supports),inline=False)
        return msg

#pop queue     
async def popmsg(users,match:Match,DM:bool,channel:int):     
    for j in users: 
        user_id = bot.get_user(j.disc_id)
    def msg():
        message = discord.Embed(title = 'Lobby Name: ' + match.creator + "'s Lobby")
        message.add_field(name='Lobby Creator:', value = match.creator,inline=False)
        message.add_field(name='Lobby Type:', value = match.lane,inline=False)
        message.add_field(name='Password: ' + match.pwd,inline=False)
        if match.secondary_players_dict is None:
            message.add_field(name='Blue side '+match.blue_player_1.role + ':', value=match.blue_player_1.disc_name,inline=True)
            message.add_field(name='Red side '+match.red_player_1.role + ':', value=match.red_player_1.disc_name,inline=True)
            message.add_field(name='Elo Difference:', value=str(match.diff),inline=False)
        elif match.secondary_players_dict is not None:
            message.add_field(name='Blue side',
            value=
            'Blue '+match.blue_player_1.role + ': '+match.blue_player_1.disc_name
            + '\n'
            'Blue '+match.blue_support.role + ': '+match.blue_support.disc_name,inline=False)
            message.add_field(name='Red side',
            value=
            'Red '+match.red_player_1.role + ': '+match.red_player_1.disc_name
            + '\n'
            'Red '+match.red_support.role + ': '+match.red_support.disc_name,inline=False)
            message.add_field(name='Elo Difference:', value=str(match.diff),inline=False)      
        return message
    message = msg()
    if DM == True:    
        await user_id.send(embed=message)
    if channel is not None:       
        channel = bot.get_channel(channel) 
        await channel.send(embed=message)  