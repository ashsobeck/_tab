#!/usr/bin/env python3

import os 
from os import path
import praw
import random
from getspotify import getTop10
from datetime import date
from discord.ext import commands
from dotenv import load_dotenv
import pandas as pd


#loads the .env file that has tokens and ids for reddit needed
#to login to discord and reddit
load_dotenv()
#this is for loading tokens or other things you don't want in the actual program
# for example in a .env file, you could say TOKEN=sadfjkhorg412387234651472 (not a real token)
TOKEN = os.getenv('DISCORD_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent='ABot'
                    )


bot = commands.Bot(command_prefix='!')

def get_links(submissions):
    urls = []
    #goes through each link and sees if there is 
    #an image link
    for sub in submissions:
        if '.png' or '.jpg' in sub.url:
            urls.append(sub.url)
    return urls

@bot.command(name='meme', 
             help='Responds with a meme from hot of r/ProgrammerHumor'
            )
async def meme(ctx):
    #gets the links with .jpg or .png in the name
    submissions = get_links(reddit.subreddit('ProgrammerHumor').hot(limit=50))
    #randomly chooses the meme
    url_choice = random.choice(submissions)
    #bot sends message
    await ctx.send(url_choice)

@bot.command(name='top10',
             help='Responds with top 10 songs from the daily Spotify Top 200'
            )
async def top10(ctx):
    potential_csv = 'top10' + date.strftime('%Y-%m-%d') + '.csv'
    if (path.exists(potential_csv)):
        with open(potential_csv, 'r') as data: 
            topsongs = pd.read_csv(data)
            await ctx.send(topsongs)
    else:
        getTop10()
        with open(potential_csv, 'r') as data: 
            topsongs = pd.read_csv(data)
            await ctx.send(topsongs)


bot.run(TOKEN)
