import openai
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.environ['OPENAI_KEY']
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="//", intents=intents)

class openai_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    def query(self, payload):
        completion = openai.Completion.create(engine="text-davinci-002", max_tokens=2048, prompt="summarize the following article:" + payload )
        return completion
    @bot.command()
    async def tldr(self, ctx, *args):
        query = " ".join(args)
        async with ctx.channel.typing():
          response = self.query(query)
        await ctx.reply(response.choices[0].text)

async def setup(bot):
    await bot.add_cog(openai_cog(bot))