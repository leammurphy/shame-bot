import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="//", intents=intents)

class music_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.is_playing = False

        #list containing [song, channel]
        self.music_queue = []
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            "noplaylist":'True'
        }

        self.voice_channel = ""

    # Utils
    # make an instance of ytdl, get multiple urls and return it back
    def search_yt(self, item):
        with YoutubeDL(self.ydl_opts) as ydl:
            try:
                info = ydl.extract_info("ytsearch:%s" % item, download=False)['entries'][0]
            except Exception:
                return False
            
            return {'source': info['formats'][0]['url'], 'title': info['title']}
    
    # if there is music in the queue get the first url, pop it, repeat. Otherwise, there is nothing to play.
    def play_next(self):
        if len(self.music_queue) > 0:
            self.is_playing = True

            m_url = self.music_queue[0][0]['source']

            self.music_queue.pop(0)

            self.voice_channel.play(discord.FFmpegPCMAudio(m_url), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    async def play_music(self):
        if len(self.music_queue) > 0:
            self.is_playing = True
        
            m_url = self.music_queue[0][0]['source']

            if self.voice_channel == "" or not self.voice_channel.is_connected():
                self.voice_channel = await self.music_queue[0][1].connect()
            else:
                self.voice_channel = await self.bot.move_to(self.music_queue[0][1])

            self.music_queue.pop(0)

            self.voice_channel.play(discord.FFmpegPCMAudio(m_url), after=lambda e: self.play_next())
        else:
            self.is_playing = False

    # @bot.command()
    # async def join(self, ctx):
    #     voice_state = ctx.author.voice
    #     if voice_state is None:
    #         await ctx.reply("pssst, join a voice_channel first")
    #     else:
    #         await voice_state.channel.connect()

    @bot.command()
    async def play(self, ctx, *args):
        voice_state = ctx.author.voice
        query = " ".join(args)

        if voice_state is None:
            await ctx.reply("pssst, join a voice channel first")
        else:
            # voice_channel = discord.utils.get(ctx.guild.voice_channels, name=ctx.author.voice.channel.name)
            voice_channel = voice_state.channel
            song = self.search_yt(query)
            if type(song) == type(True):
                await ctx.reply("Mission Failed. no playlists or livestreams allowed")
            else:
                await ctx.reply("Okay, adding " + song["title"] + " to the queue")
                self.music_queue.append([song, voice_channel])
                
                if self.is_playing == False:
                    await self.play_music()
    
    @bot.command()
    async def q(self, ctx):
        retval = ""
        for i in range(0, len(self.music_queue)):
            retval += self.music_queue[i][0]['title'] + "\n"
        if retval != "":
            await ctx.reply(retval)
        else:
            await ctx.reply("Nothing here")

    @bot.command()
    async def skip(self, ctx):
        print("called")
        if self.voice_channel != "":
            self.voice_channel.stop()
            await ctx.reply("ugggh, fine. I liked that song y'know.... Now Playing " + self.music_queue[0][0]['title'])
            await self.play_music()

    @bot.command()
    async def leave(self, ctx):
        voice = discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild)

        if voice == None:
            await ctx.reply("umm... did you think to invite me first?")
            return
        if voice.is_connected():
            await ctx.reply("goodbye, " + ctx.author.name)
            await voice.disconnect()

async def setup(bot):
    await bot.add_cog(music_cog(bot))