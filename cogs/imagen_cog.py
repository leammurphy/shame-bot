import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import io
import warnings
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="//", intents=intents)

class imagen_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # To get your API key, visit https://beta.dreamstudio.ai/membership
        self.api_endpoint = client.StabilityInference(
            key=os.environ['STABILITY_KEY'], 
            verbose=True,
        )
    def query(self, payload):
        answers = self.api_endpoint.generate(
            prompt = payload
        )

        for resp in answers:
            for artifact in resp.artifacts:
                if artifact.finish_reason == generation.FILTER:
                    warnings.warn(
                        "Your request activated the API's safety filters and could not be processed."
                        "Please modify the prompt and try again.")
                if artifact.type == generation.ARTIFACT_IMAGE:
                    img = io.BytesIO(artifact.binary)
                    # img = Image.open(io.BytesIO(artifact.binary))
                    return img

    @bot.command()
    async def gen(self, ctx, *args):
        query = " ".join(args)
        async with ctx.channel.typing():
          response = self.query(query)

        await ctx.reply(file=discord.File(response, 'cool_image.png'))

async def setup(bot):
    await bot.add_cog(imagen_cog(bot))