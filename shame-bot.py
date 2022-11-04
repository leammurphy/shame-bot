import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
import random
import requests
import json
from bs4 import BeautifulSoup
import os
from os import getenv
import helpers
import datetime
from discord.ext import tasks

from cogs.music_cog import music_cog
from cogs.speech_cog import speech_cog
from cogs.imagen_cog import imagen_cog
from cogs.reddit_cog import reddit_cog

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="//", intents=intents)


bot.add_cog(music_cog(bot))
bot.add_cog(speech_cog('DialoGPT-medium-Zuko'))
bot.add_cog(imagen_cog(bot))
bot.add_cog(reddit_cog(bot))

load_dotenv()

@bot.event
async def on_ready():
    print(str(bot.user.name) + ' has connected to Discord!')
    guild = discord.utils.get(bot.guilds)
    await bot.change_presence(activity = discord.Activity(
                          type = discord.ActivityType.watching,
                          name = 'time pass by...'))
    # await bot.change_presence(activity = discord.Game('League of Legends'))
    print("The value of guild is " + str(guild ))

@bot.event
async def on_message(message):
    words = open('json/words.json')
    encouragements = open('json/encouragements.json')

    await bot.process_commands(message)
    if message.author == bot.user:
        return
    msg = message.content
    if any(word in msg for word in json.load(words)):
        await message.reply(random.choice(json.load(encouragements)))

# COMMANDS
@bot.command()
async def echo(ctx, *args):
    m_args = " ".join(args)
    await ctx.send(m_args)

@bot.command()
async def hello(ctx):
    greetings = open('json/greetings.json')
    greeting = random.choice(json.load(greetings))
    await ctx.reply(greeting)

@bot.command()
async def rollD20(ctx):
    dice = [
        str(random.choice(range(1, 20)))
    ]
    await ctx.reply(', '.join(dice))

@bot.command()
async def inspire(ctx):
    quote = helpers.get_quote()
    await ctx.reply(quote)
    await ctx.message.delete()

@bot.command()
async def news(ctx):
    the_news = helpers.get_news()
    await ctx.send("Okay, getting todays news")
    await asyncio.sleep(3)
    await ctx.send("--------  Today's top 5 Headlines  --------")
    await asyncio.sleep(1)
    for a in the_news: 
        await ctx.send(a["title"] + " " + a["url"])
    await ctx.send("-------- -------- -------- -------- --------")
    await ctx.message.delete()

@bot.command()
async def stocks(ctx, *args):
    ticker = args[0]
    the_stock = helpers.get_stocks(ticker)
    await ctx.send(' -------- ' + ticker + ' -------- ')
    await ctx.send("open: " + str(the_stock[0]))
    await ctx.send("close: " + str(the_stock[1]))

@bot.command()
async def yomama(ctx):
    joke = helpers.get_yomama()
    await ctx.send(joke)
    await ctx.message.delete()

# might replace this webscrape with the offical deviantart api
@bot.command()
async def dva(ctx):
    urls = open('json/dva-urls.json')
    url = random.choice(json.load(urls))
    print(url)
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    images = soup.find_all('img')

    image_data = []
    for image in images:
        link = image['src']
        name = image['alt']
        image_data.append([name, link]) 

    # this isn't working. 
    # for name, link in image_data:
        # print("1:", name,"2:", link)
        # if  "data:image/png" in link or "avatar" in name:
        #     index = image_data.index([name, link])
        #     print(name, link, index)
        #     image_data.pop(index)

    for image in image_data:
        if "data:image/png" in image[1]:
            index = image_data.index(image)
            image_data.pop(index)
    for image in image_data:
        if "avatar" in image[0]:
            index = image_data.index(image)
            image_data.pop(index)
     
    # the first seven images in the array are not relevant to the scrape so they can be removed.
    cleaned_imgs = image_data[7:]
    random_photo = random.choice(cleaned_imgs)
    
    name = random_photo[0]
    link = random_photo[1]

    em = discord.Embed(title = name)
    em.set_image(url = link)

    await ctx.send(embed = em)
    await ctx.message.delete()

@bot.command()
async def date(ctx):
    today = datetime.date.today()
    # print(today)
    await ctx.send(today)
    await ctx.message.delete()
    # 1017667556871512134

@tasks.loop(hours=18.0)
async def gimme():
    today = datetime.date.today()
    channel = bot.get_channel(914709454929416254)
    await channel.send(today)
@bot.event
async def on_ready():
    gimme.start()
# This was required for hosting on Heroku
# async def load_extensions():
#     for filename in os.listdir("cogs"):
#         if filename.endswith(".py"):
#             # cut off the .py from the file name
#             await bot.load_extension(f"cogs.{filename[:-3]}")

# async def main():
#     async with bot:
#         await load_extensions()
#         await bot.start(getenv('TOKEN'))

# asyncio.run(main())
bot.run(getenv('TOKEN'))
