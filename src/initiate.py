import discord
from discord.ext import commands, tasks
from discord.commands import Option 
from connect import *
from dotenv import load_dotenv,find_dotenv 
import os
import json

#Discord Bot Initiation
load_dotenv(find_dotenv())
disc_token_path = os.environ.get("SECRETS")
with open (disc_token_path) as file1:
    token = json.load(file1)['TOKEN']
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents) 
