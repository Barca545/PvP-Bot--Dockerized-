from initiate import *
from Matchmaking import *
from Messages import *
from Queues import *
from sqlfunctions import *

rank_as_mmr = {
    'Iron 2' : 300,
    'Iron 1' : 400,
    'Bronze 4' : 500,
    'Bronze 3' : 600,
    'Bronze 2' : 700,
    'Bronze 1' : 800,
    'Silver 4' : 900,
    'Silver 3' : 1000,
    'Silver 2' : 1100,
    'Silver 1' : 1200,
    'Gold 4' : 1300,
    'Gold 3' : 1400,
    'Gold 2' : 1500,
    'Gold 1' : 1600,
    'Platinum 4' : 1700,
    'Platinum 3' : 1800,
    'Platinum 2' : 1900,
    'Platinum 1' : 2000,
    'Diamond 4' : 2100,
    'Diamond 3' : 2200,
    'Diamond 2' : 2300,
    'Diamond 1' : 2400,
    'Master' : 2600,
    'Grandmaster' : 3000,
    'Challenger' : 3500,
    }
roles = ['ADC','Support','Top', 'Mid']

#Discord connect
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    pop_queue.start()

#set channel
@bot.slash_command()
async def set_channel(ctx):
    server_id = int(ctx.guild_id)
    channel_id= int(ctx.channel_id)
    sqlsetchannel(str(server_id),str(channel_id))
    Queue.add_server(server_id  )
    await ctx.respond('Bot channel is now ' + f'<#{channel_id}>')

#/setup
@bot.slash_command()
async def setup(ctx, ign:str, rank: Option(choices=rank_as_mmr), opgg_link):             
    user_id = int(ctx.author.id)
    mmr = rank_as_mmr[rank]
    sqlsetup(user_id,ign,mmr,opgg_link)
    msg=setupmsg(ign=ign)
    await ctx.respond(embed=msg)

@bot.slash_command()
async def updateprofile(ctx, ign:str, rank: Option(choices=rank_as_mmr), opgg_link):
    user_id = int(ctx.author.id)
    mmr = rank_as_mmr[rank]
    sqlupdateprof(user_id,ign,mmr,opgg_link)
    msg=updateupmsg(ign=ign)
    await ctx.respond(embed=msg)

@bot.slash_command()
async def joinqueue(ctx, region: Option(choices=regions), role: Option(choices=roles)):
    server_id = int(ctx.guild_id)
    user_id = int(ctx.author.id)
    player = Player.build(user_id,role)
    msg=updatequeuemsg(user_id,role,'joined')
    if role == 'ADC':    
        Queues[server_id][region].adc_queue[player.disc_id] = player
    elif role == 'Support':
        Queues[server_id][region].sup_queue[player.disc_id] = player
    elif role == 'Mid':
        Queues[server_id][region].mid_queue[player.disc_id] = player
    elif role == 'Top':
        Queues[server_id][region].top_queue[player.disc_id] = player
    await ctx.respond(embed=msg)

@bot.slash_command()
async def leavequeue(ctx, region: Option(choices=regions),role: Option(choices=roles)):
    user_id = int(ctx.author.id)
    server_id = int(ctx.guild_id)
    if role == 'ADC':  
        del Queues[server_id][region].adc_queue[user_id]
    elif role == 'Support':
        del Queues[server_id][region].sup_queue[user_id]
    elif role == 'Mid':
        del Queues[server_id][region].mid_queue[user_id] 
    elif role == 'Top':
        del Queues[server_id][region].top_queue[user_id]
    msg=updatequeuemsg(user_id,role,'left')
    await ctx.respond(embed=msg)

#/showqueues
@bot.slash_command()
async def showqueue(ctx,region:Option(choices=regions),lane:Option(choices=['Top Lane', 'Middle Lane', 'Bottom Lane', 'All'])): 
    server_id = int(ctx.guild_id)
    message = showqmsg(server_id,region,lane)         
    await ctx.respond(embed=message)

#/match
@bot.slash_command()
async def match(ctx,match_id,winner:Option(choices=['Blue', 'Red'])):
    sqlmatch(winner,match_id)
    await ctx.respond('match updated')

#/show profile
@bot.slash_command() 
async def showprofile(ctx,user_id=None):
    if user_id==None:
        user = int(ctx.author.id)
    else:
        user=(user_id)
    player = Player.build(user)
    msg=profilemsg(player.disc_name, player.ign, player.rank, player.opgg)
    await ctx.respond(embed=msg)

#Pop queue    
#need to make the loop more periodic
@tasks.loop(seconds=0) 
async def pop_queue(): 
    servers = sqlservers()
    for server in servers:
        server_id = server[0]
        channel_id=server[1]
        for region in regions:
            top_queue = Queues[server_id][region].top_queue
            mid_queue=Queues[server_id][region].mid_queue
            adc_queue=Queues[server_id][region].adc_queue
            sup_queue=Queues[server_id][region].sup_queue
            if len(top_queue)>=2: 
                top_match = Match.build_solo(top_queue)
                await popmsg(top_match,channel_id=channel_id,lane='Top Lane')
            if len(mid_queue)>=2:
                mid_match = Match.build_solo(mid_queue)
                await popmsg(mid_match,channel_id=channel_id,lane='Middle Lane')
            if len(adc_queue) >= 2 and len(sup_queue) >= 2:
                bot_match = Match.build_duo(adc_queue=adc_queue,sup_queue=sup_queue)
                await popmsg(bot_match,channel_id=channel_id,lane='Bottom Lane')
bot.run(token)                                                                                                                                           