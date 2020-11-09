import discord
import yaml
import urllib.request
import urllib.parse
import json
import requests
from discord.ext import commands

def load_config(config_file = 'config.yaml'):
    with open(config_file) as file:
        config = yaml.safe_load(file)
    return config

CONFIG = load_config()

client = commands.Bot(command_prefix='.')

@client.event
async def on_ready():
    print('')
    print('𝔫𝔲𝔤𝔟𝔬𝔱') 
    print('')
    print(f'Logged in as {client.user}')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you 👀"))

@client.command()
async def ping(ctx):
    await ctx.send("pong")

@client.command()
async def gis(ctx, *, query):
    print(f'{ctx.author} searched for {query}')
    images = await search(query)
    result = strip_pinterest(images)
    await ctx.send(result)

async def search(query):
    api_url = 'https://www.googleapis.com/customsearch/v1?'
    api_key = CONFIG['imagesearch']['google_api_key']
    search_engine_id = CONFIG['imagesearch']['search_engine_id']
    query = urllib.parse.quote(query)
    uri = urllib.request.urlopen(f'{api_url}key={api_key}&cx={search_engine_id}&searchType=image&num=10&q={query}')
    images = json.loads(uri.read().decode())
    return images['items']

def strip_pinterest(results):
    for result in results:
        if 'pinimg' not in result['link']:
            return result['link']


@client.command()
async def lastfm(ctx, username):
    track = await get_last_track(username)
    print(f'{ctx.author} ({username}) scrobbled: {track}')
    await ctx.send(track)

async def call_lastfm_api(args):
    api_key = CONFIG['lastfm']['api_key']
    api_url = f'http://ws.audioscrobbler.com/2.0/?&format=json&api_key={api_key}'

    for key, value in args.items():
        api_url += f'&{key}={value}'

    uri = urllib.request.urlopen(f'{api_url}')
    track = json.loads(uri.read().decode())
    return track['recenttracks']['track']

async def get_last_track(username):
    last_track = await call_lastfm_api({'method': 'user.getrecenttracks', 'user': username, 'limit': '1'})

    track_name = last_track[0]['name']
    track_mbid = last_track[0]['mbid']
    artist_name = last_track[0]['artist']['#text']
    album_name = last_track[0]['album']['#text']

    return f'♫ **{track_name}** by **{artist_name}** on **{album_name}**'



client.run(CONFIG['bot_token'])