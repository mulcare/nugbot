import discord
from discord.ext import commands
import requests
import yaml

def load_config(config_file = 'config.yaml'):
    with open(config_file) as file:
        config = yaml.safe_load(file)
    return config

CONFIG = load_config()

bot = commands.Bot(command_prefix='.')

# Add nugs you want to load to this list. There should be a file in the
# /nugs/ subdir that matches the name, e.g. /nugs/google.py is loaded
# by adding 'google' to the nugs list.

nugs = [
    'drewbot'
]

@bot.event
async def on_ready():
    print('[BOT] 𝔫𝔲𝔤𝔟𝔬𝔱') 
    print(f'[BOT] logged in as \"{bot.user}\"')
    load_nugs(nugs)
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you 👀"))

def load_nugs(nuglist):
    for nug in nuglist:
        try:
            bot.load_extension(f'nugs.{nug}')
            print(f'[BOT] nug loaded successfully: {nug}')
        except:
            print(f'[BOT] nug \"{nug}\" failed to load')

bot.run(CONFIG['bot_token'])