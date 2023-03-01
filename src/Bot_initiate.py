import gspread
import dotenv
from dotenv import load_dotenv,find_dotenv 
import discord
from discord.ext import commands, tasks
from discord.commands import Option 
import json
import os


load_dotenv(find_dotenv())

gspread_cred_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
disc_token_path = os.environ.get("PVP_TOKEN")

#dotenv In
dotenv.load_dotenv()

#Discord Bot Initiation
with open (disc_token_path) as file1:
    token = json.load(file1)['TOKEN']
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents) 

#Gspread initiation 
with open (gspread_cred_path) as file2:
    credentials = json.load(file2)
gc = gspread.service_account_from_dict(credentials)

bot_database = gc.open_by_url('https://docs.google.com/spreadsheets/d/134T4caUqFHG3crrS_Rk9Z3ON5o6mc19tPt4kTm4R834')
Botlaners = bot_database.get_worksheet_by_id(0)
Supports = bot_database.get_worksheet_by_id(1953196714)
Tops = bot_database.get_worksheet_by_id(839126568)
Mids = bot_database.get_worksheet_by_id(431869411)
Guilds = bot_database.get_worksheet_by_id(1531822391)