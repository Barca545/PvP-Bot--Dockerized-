import gspread
import dotenv 
import discord
from discord.ext import commands, tasks
from discord.commands import Option 
import os
import json

#dotenv In
dotenv.load_dotenv()

#Discord Bot Initiation
with open ('Discord_token.json') as file1:
    token = json.load(file1)['TOKEN']
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents) 

#Gspread initiation 
with open ('v2-bot-374602-e64743327d13.json') as file2:
    credentials = json.load(file2)
gc = gspread.service_account_from_dict(credentials)

bot_database = gc.open_by_url('https://docs.google.com/spreadsheets/d/134T4caUqFHG3crrS_Rk9Z3ON5o6mc19tPt4kTm4R834')
Botlaners = bot_database.get_worksheet_by_id(0)
Supports = bot_database.get_worksheet_by_id(1953196714)
Tops = bot_database.get_worksheet_by_id(839126568)
Mids = bot_database.get_worksheet_by_id(431869411)
Guilds = bot_database.get_worksheet_by_id(1531822391)