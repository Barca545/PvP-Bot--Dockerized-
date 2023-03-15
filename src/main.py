from initiate import *
from Matchmaking import *
from Messages import *
from Queues import *

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
    guild = int(ctx.guild_id)
    channel= int(ctx.channel_id)
    Guilds.append_row([guild,channel])
    await ctx.respond('Bot channel is now ' + '#'+str(channel))

#/setup
@bot.slash_command()
async def setup(ctx, ign, rank: Option(choices=rank_as_mmr), opgg_link):             
    user = ctx.author
    id = user.id
    Players.append_row([str(user), ign, id,  rank_as_mmr[rank], opgg_link])
    msg=setupmsg(ign=ign)
    await ctx.respond(embed=msg)

@bot.slash_command()
async def joinqueue(ctx, region: Option(choices=['NA', 'EUW']), role: Option(choices=roles)):
    server = str(ctx.guild_id)
    user = Players.find('{}'.format(ctx.author)).value
    player = Player.build(user,role)
    if role == 'ADC':    
        Queues[server][region].adc_queue[player.disc_name] = player
        await ctx.respond(player.disc_name + ' has joined the ADC queue')
    elif role == 'Support':
        Queues[server][region].sup_queue[player.disc_name] = player
        await ctx.respond(player.disc_name + ' has joined the Support queue')
    elif role == 'Mid':
        Queues[server][region].mid_queue[player.disc_name] = player
        await ctx.respond(player.disc_name + ' has joined the Mid queue')
    elif role == 'Top':
        Queues[server][region].top_queue[player.disc_name] = player
        await ctx.respond(player.disc_name + ' has joined the Top queue')

@bot.slash_command()
async def leavequeue(ctx, region: Option(choices=['NA', 'EUW']),role: Option(choices=roles)):
    user = '{}'.format(ctx.author)
    server = str(ctx.guild_id)
    if role == 'ADC':  
        del Queues[server][region].adc_queue[user]
        await ctx.respond(user + ' has left the ADC queue')
    elif role == 'Support':
        del Queues[server][region].sup_queue[user]
        await ctx.respond(user + ' has left the Support queue')    
    elif role == 'Mid':
        del Queues[server][region].mid_queue[user] 
        await ctx.respond(user + ' has left the Mid queue')
    elif role == 'Top':
        del Queues[server][region].top_queue[user]
        await ctx.respond(user + ' has left the Top queue')      

#/showqueues
@bot.slash_command()
async def showqueue(ctx,region:Option(choices=['NA', 'EUW']),lane:Option(choices=['Top Lane', 'Middle Lane', 'Bottom Lane', 'All'])): 
    server = str(ctx.guild_id)
    message = showqmsg(server,region,lane)         
    await ctx.respond(embed=message)

@bot.slash_command() 
async def showprofile(ctx,username=None):
    if username==None:
        user = '{}'.format(ctx.author)
    else:
        user=username
    player = Player.build(user)
    msg=profilemsg(player.disc_name, player.ign, player.rank, player.opgg)
    await ctx.respond(embed=msg)
#Pop queue    
@tasks.loop(seconds=60) #make 2min in final deploy
async def pop_queue(): 
    regions =['NA', 'EUW']
    servers = Guilds.col_values(col=1)[1:]
    for server_id in servers:
        server = str(server_id)  
        for region in regions:
            channel_id = int(Guilds.row_values(Guilds.find(server).row)[Guilds.find(server).col+0]) #still not convinced this shouldn't be +1        
            if len(Queues[server][region].top_queue)>=2:
                top_match = choose_solo(queue)
                await popmsg(top_match,channel_id=channel_id,lane='Top Lane')
            if len(Queues[server][region].mid_queue)>=2:
                queue=Queues[server][region].mid_queue
                mid_match = choose_solo(queue)
                await popmsg(mid_match,channel_id=channel_id,lane='Middle Lane')
            if len(Queues[server][region].adc_queue) >= 2 and len(Queues[server][region].sup_queue) >= 2:
                adc_queue=Queues[server][region].adc_queue
                sup_queue=Queues[server][region].sup_queue
                bot_match = choose_duo(adc_queue=adc_queue,sup_queue=sup_queue)
                await popmsg(bot_match,channel_id=channel_id,lane='Bottom Lane')
bot.run(token)                                                                                                                                           