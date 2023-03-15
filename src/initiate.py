import gspread
import dotenv
from dotenv import load_dotenv,find_dotenv 
import discord
from discord.ext import commands, tasks
from discord.commands import Option 
import json
import os
import sqlite3
import pandas as pd


load_dotenv(find_dotenv())

#Discord Bot Initiation
disc_token_path = os.environ.get("PVP_TOKEN")
with open (disc_token_path) as file1:
    token = json.load(file1)['TOKEN']
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents) 

#SQL Server Connect
conn = sqlite3.connect('pvpserver') 
c = conn.cursor()