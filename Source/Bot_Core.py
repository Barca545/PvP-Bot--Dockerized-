from Bot_initiate import *
from Matchmaking import *
#Supp_Champs = ['Alistar', 'Amumu','Ashe', 'Blitzcrank','Braum','Heimerdinger','Janna','Leona','Lulu','Lux','Morgana','Nami','Nautilus','Pyke','Rakan','Renata Glasc','Seraphine','Sona','Soraka','Swain','Tham Kench','Taric','Thresh','Zilean','Zyra',]
#ADC_Champs = ['Aphelios','Ashe','Caitlyn','Draven','Ezreal','Graves','Jhin','Jinx',"Kai'sa",'Kalista','Kindred',"Kog'ma",'Lucian','Miss Fortune','Samira','Senna','Quinn','Sivir','Tristana','Twitch','Varus','Vayne','Xayah','Zeri','Yasuo']
#full list of support champs #Supp_Champs = ['Alistar', 'Amumu', 'Ashe', 'Bard', 'Blitzcrank', 'Brand','Braum','Heimerdinger','Ivern','Janna','Karma', 'Leona','Lulu','Lux','Malphite','Maokai','Morgana','Nami','Nautilus','Pantheon','Pyke','Rakan','Renata Glasc','Senna','Seraphine','Sona','Soraka','Swain','Tham Kench','Taric','Thresh',"Vel'Koz",'Xerath','Yuumi','Zac','Zilean','Zyra',]

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
Queues = build_queues()

#discord set up
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    pop_queue.start()

@bot.slash_command()
async def set_channel(ctx):
    guild = int(ctx.guild_id)
    channel= int(ctx.channel_id)
    Guilds.append_row([guild,channel])
    await ctx.respond('Bot channel is now ' + '#'+str(channel))

#/setup
@bot.slash_command()
async def setup(ctx, ign, rank: Option(choices=rank_as_mmr),role: Option(choices=roles), opgg_link, champ_1, champ_2, champ_3):             
    user = ctx.author
    id = user.id
    if role == 'ADC':
        Botlaners.append_row([str(user), ign, id, rank_as_mmr[rank], opgg_link, champ_1, champ_2, champ_3])
    elif role == 'Support':                               
        Supports.append_row([str(user), ign, id, rank_as_mmr[rank], opgg_link, champ_1, champ_2, champ_3])
    elif role == 'Top':
        Tops.append_row([str(user), ign, id, rank_as_mmr[rank], opgg_link, champ_1, champ_2, champ_3])
    elif role == 'Mid':
        Mids.append_row([str(user), ign, id,  rank_as_mmr[rank], opgg_link, champ_1, champ_2, champ_3])
    await ctx.respond(f'Setup complete GLHF {ign}!!!')

@bot.slash_command()
async def joinqueue(ctx, region: Option(choices=['NA', 'EUW']), role: Option(choices=roles)):
    if role == 'ADC':
        user = Botlaners.find('{}'.format(ctx.author)).value
        player = Player.build(user,role,Botlaners)
        server = ctx.guild_id
        Queues[server][region].adc_queue[player.disc_name] = player
        await ctx.respond(player.disc_name + ' has joined the ADC queue')
    elif role == 'Support':
        user = str(Supports.find('{}'.format(ctx.author)).value)
        player = Player.build(user,role,Supports)
        Queues[server][region].sup_queue[player.disc_name] = player
        await ctx.respond(player.disc_name + ' has joined the Support queue')
    elif role == 'Mid':
        user = str(Mids.find('{}'.format(ctx.author)).value)
        player = Player.build(user,role,Mids)
        Queues[server][region].mid_queue[player.disc_name] = player
        await ctx.respond(player.disc_name + ' has joined the Mid queue')
    elif role == 'Top':
        user = str(Tops.find('{}'.format(ctx.author)).value)
        player = Player.build(user,role,Tops)
        Queues[server][region].top_queue[player.disc_name] = player
        await ctx.respond(player.disc_name + ' has joined the Top queue')

@bot.slash_command()
async def leavequeue(ctx, region: Option(choices=['NA', 'EUW']),role: Option(choices=roles)):
    user = '{}'.format(ctx.author)
    server = ctx.guild_id
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
async def show2v2queue(ctx,region: Option(choices=['NA', 'EUW'])): 
    server = ctx.guild_id
    await ctx.respond(
        str(len(Queues[server][region].adc_queue)) + ' in the ADC queue' 
        + '\n'  +
        str(len(Queues[server][region].sup_queue)) + ' in the Support queue')

@bot.slash_command()
async def showtopqueue(ctx,region: Option(choices=['NA', 'EUW'])): 
    server = ctx.guild_id
    await ctx.respond(
        str(len(Queues[server][region].top_queue)) + ' in the Top queue')

@bot.slash_command()
async def showmidqueue(ctx,region: Option(choices=['NA', 'EUW'])): 
    server = ctx.guild_id 
    await ctx.respond(
        str(len(Queues[server][region].mid_queue)) + ' in the Mid queue')

#Pop queue    
@tasks.loop(seconds=30) #make 5min in final deploy
async def pop_queue():  #currently looping forever make it so the players are removed from the queue when added to a match.
    regions =['NA', 'EUW']
    server_ids = Guilds.col_values(col=1)[1:] 
    for server in server_ids:
        for region in regions:
            if len(Queues[server][region].top_queue)>=2:
                match_info = choose_solo('Top')
                players = match_info[0] 
                match = match_info[1]
                creator_msg = match[0]
                name_msg = match[1]
                type_msg = match[2]
                pwd_msg = match[3]
                bluelaner = match[4][0]
                redlaner = match[4][1]
                diff_msg = match[5]
                users = (players['Blue'],players['Red'])
                await popmsg(users,str(creator_msg) + '\n' + str(name_msg) + '\n' + str(type_msg) + '\n' + str(pwd_msg) +  '\n' + str(bluelaner) + '\n' + str(redlaner) + '\n' + str(diff_msg),DM=True,channel=False,channel_name=False)
            if len(Queues[server][region].mid_queue)>=2:
                match_info = choose_solo('Mid')
                players = match_info[0] 
                match = match_info[1]
                creator_msg = match[0]
                name_msg = match[1]
                type_msg = match[2]
                pwd_msg = match[3]
                bluelaner = match[4][0]
                redlaner = match[4][1]
                diff_msg = match[5]
                users = (players['Blue'],players['Red'])
                await popmsg(users,str(creator_msg) + '\n' + str(name_msg) + '\n' + str(type_msg) + '\n' + str(pwd_msg) +  '\n' + str(bluelaner) + '\n' + str(redlaner) + '\n' + str(diff_msg),DM=True,channel=False,channel_name=False)
            if len(Queues[server][region].adc_queue) >= 2 and len(Queues[server][region].sup_queue) >= 2:
                await choose_duo()   
bot.run(token)                                                                                                                                           