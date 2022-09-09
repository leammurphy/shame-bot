import discord
from discord.ext import commands
import os
import random
import praw
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="//", intents=intents)

class reddit_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(
            client_id = os.environ['REDDIT_ID'],
            client_secret = os.environ['REDDIT_SECRET'],
            user_agent = "pythonpraw"
        )  

    def subreddit(self, sub):
        subreddit = self.reddit.subreddit(sub)
        photos = []
        top = subreddit.top(limit = 25)
        
        for photo in top:
            photos.append(photo)

        random_photo = random.choice(photos)
        
        name = random_photo.title
        url = random_photo.url

        return {"name": name, "url": url}

    @bot.command()
    async def film(self, ctx):
        film = self.subreddit("analog")

        em = discord.Embed(title = film["name"])
        em.set_image(url = film["url"])
        await ctx.send("What do you think?")
        await ctx.send(embed = em)
        await ctx.message.delete()

    @bot.command()
    async def meme(self, ctx):
        meme = self.subreddit("shitposting")

        em = discord.Embed(title = meme["name"])
        em.set_image(url = meme["url"])

        await ctx.send("HA, good meme")
        await ctx.send(embed = em)
        await ctx.message.delete()

async def setup(bot):
    await bot.add_cog(reddit_cog(bot))


