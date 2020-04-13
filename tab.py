#!/usr/bin/env python3

import os 
from os import path
import praw
import random
from getspotify import getTopSongs
from datetime import datetime
from discord.ext import commands
from dotenv import load_dotenv
import time
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
                     user_agent='_tab'
                    )


bot = commands.Bot(command_prefix='.')

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

@bot.command(name='top',
             help='Responds with top x songs from the daily Spotify Top 200'
            )
async def top10(ctx, numsongs):
    if int(numsongs) > 199:
        await ctx.send('Number must be less than 200')
    potential_csv = 'top-' + str(datetime.date(datetime.now())) + '.csv'
    try:
        if (path.exists(potential_csv)):
            with open(potential_csv, 'r') as data: 
                topsongs = pd.read_csv(data, delimiter=',',
                           names = ['Rank', 'Artist', 'Song'],
                           nrows=int(numsongs) 
                           )
                await ctx.send(topsongs)
        else:
            getTopSongs()
            with open(potential_csv, 'r') as data: 
                topsongs = pd.read_csv(data, delimiter=',', 
                           names= ['Rank', 'Song', 'Artist'],
                           nrows=int(numsongs)
                           )
                await ctx.send(topsongs)
    except:
        await ctx.send('Unable to process request')


@bot.command(name='stream',
             help='streams the posts from r/ACTrade'
            )
async def streamACT(ctx):    
    for sub in reddit.subreddit('ACTrade').stream.submissions(pause_after=6, skip_existing=True):
        if sub is None:
            continue
        await ctx.send(sub.url)

bot.run(TOKEN)
