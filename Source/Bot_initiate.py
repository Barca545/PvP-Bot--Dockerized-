import gspread
import dotenv 
import discord
from discord.ext import commands, tasks
from discord.commands import Option 
import os

#dotenv In
dotenv.load_dotenv()

#Discord Bot Initiation
token = str(os.getenv("DISC_TOKEN"))
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents) 

#Gspread Initation
type = os.getenv("TYPE")
project_id = os.getenv("PROJECT_ID")
private_key_id= os.getenv("PRIVATE_KEY_ID")
private_key= os.getenv("PRIVATE_KEY")
client_email= os.getenv("CLIENT_EMAIL")
client_id= os.getenv("CLIENT_ID")
auth_uri= os.getenv("AUTH_URI")
token_uri= os.getenv("TOKEN_URI")
auth_provider_x509_cert_url= os.getenv("AUTH_PROVIDER_X509_CERT_URL")
client_x509_cert_url= os.getenv("CLIENT_X509_CERT_URL")
credentials = {
    "type": type,
    "project_id": project_id,
    "private_key_id": private_key_id,
    "private_key": private_key,
    "client_email": client_email,
    "client_id": client_id,
    "auth_uri":auth_uri,
    "token_uri":token_uri,
    "auth_provider_x509_cert_url":auth_provider_x509_cert_url,
    "client_x509_cert_url":client_x509_cert_url
}
gc = gspread.service_account_from_dict(credentials)


bot_database = gc.open_by_url('https://docs.google.com/spreadsheets/d/134T4caUqFHG3crrS_Rk9Z3ON5o6mc19tPt4kTm4R834')
Botlaners = bot_database.get_worksheet_by_id(0)
Supports = bot_database.get_worksheet_by_id(1953196714)
Tops = bot_database.get_worksheet_by_id(839126568)
Mids = bot_database.get_worksheet_by_id(431869411)


