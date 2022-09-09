import discord
from discord.ext import commands
import os
import json
import requests

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="//", intents=intents)

# this is my Hugging Face profile link
API_URL = 'https://api-inference.huggingface.co/models/chulainn/'

class speech_cog(commands.Cog):
    def __init__(self, model_name):
        super().__init__()
        self.api_endpoint = API_URL + model_name

        # retrieve the secret API token from the system environment
        huggingface_token = os.environ['HUGGINGFACE_TOKEN']

        # format the header in our request to Hugging Face
        self.request_headers = {
            'Authorization': 'Bearer {}'.format(huggingface_token)
        }

    def query(self, payload):
        """
        make request to the Hugging Face model API
        """
        data = json.dumps(payload)
        response = requests.request('POST',
                                    self.api_endpoint,
                                    headers=self.request_headers,
                                    data=data)
        ret = json.loads(response.content.decode('utf-8'))
        return ret

    @bot.command()
    async def say(self, ctx, *args):
        query = " ".join(args)

        payload = {'inputs': {'text': query}}
        async with ctx.channel.typing():
          response = self.query(payload)
        bot_response = response.get('generated_text', None)
        
        # we may get ill-formed response if the model hasn't fully loaded
        # or has timed out
        if not bot_response:
            if 'error' in response:
                print('`Error: {}`'.format(response['error']))
                bot_response = "Let me get ready"
            else:
                bot_response = 'Hmm... something is not right.'

        await ctx.channel.send(bot_response)

async def setup(bot):
    await bot.add_cog(speech_cog('DialoGPT-medium-Zuko'))