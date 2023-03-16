from dotenv import load_dotenv,find_dotenv 
import discord
from discord.ext import commands, tasks
from discord.commands import Option 
import json
import os
import sqlite3



load_dotenv(find_dotenv())

#Discord Bot Initiation
disc_token_path = os.environ.get("PVP_TOKEN")
with open (disc_token_path) as file1:
    token = json.load(file1)['TOKEN']
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents) 

#SQL Server Connect
db_path = os.environ.get("DB")
conn = sqlite3.connect(db_path) 
c = conn.cursor()