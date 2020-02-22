#!/usr/bin/env python3

import os 
import io
import aiohttp
import praw
import random
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent='ABot'
                    )


# client = discord.Client()
bot = commands.Bot(command_prefix='!')

def get_links(submissions):
    urls = []
    for sub in submissions:
        if '.png' or '.jpg' in sub.url:
            urls.append(sub.url)
    return urls

@bot.command(name='meme', 
             help='Responds with a meme from hot of r/ProgrammerHumor'
            )
async def meme(ctx):
    submissions = get_links(reddit.subreddit('ProgrammerHumor').hot(limit=50))
    url_choice = random.choice(submissions)
    # async with aiohttp.ClientSession() as session:
    #     async with session.get(url_choice) as resp:
    #         if resp.status != 200: 
    #             return await ctx.send('Error, could not download file...')
    #         data = io.BytesIO(await resp.read())
    #         await ctx.send(file=bot.File(data, 'meme.png'))
    await ctx.send(url_choice)

bot.run(TOKEN)
