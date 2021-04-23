'''
Copyright (©) 2020 Kiet Pham <kiet.riley2005@gmail.com>
This software/program has a copyright license, more information is in the 'LICENSE' file
IF YOU WANT TO USE/COPY/MODIFY/REPRODUCE/RE-DISTRIBUTE THIS PROGRAM, YOU MUST INCLUDE A COPY OF THE LICENSE

Author Name: Kiet Pham
Author Contact: kiet.riley2005@gmail.com
Discord: CaptainVietnam6#7932
Discord Server: https://discord.gg/3z76p8H5yj
GitHub: https://github.com/CaptainVietnam6
Instagram: @itz_kietttttttttt
Program Status: ACTIVE, ABANDONED
'''

import discord
from discord.ext import commands
from discord.utils import get
from discord.ext.commands import cooldown
from discord.ext.commands import BucketType
from discord import FFmpegPCMAudio

import os
from os import system
import random
from random import randint
import time
import youtube_dl
import shutil

from BOT_TOKEN import BOT_TOKEN
from keep_alive import keep_alive


bot_prefixes = [",", "/"]
client = commands.Bot(command_prefix = bot_prefixes)

client.remove_command("help")


#ALERTS WHEN MONARCHMUSICBOT IS READY
@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.online, activity = discord.Game("Programmed by CaptainVietnam6#0001 in Python 3.8.2"))
    time.sleep(3)
    print("MonarchMusicBot is ready")

    #notifs for Monarch SMP Server
    channel = client.get_channel(767474825538437120)
    await channel.send("MonarchMusicBot is online")
    #notifs for CV6's Playground server
    channel = client.get_channel(816179144961818634)
    await channel.send("MonarchMusicBot is online")
    #notifs for CV6's Bots server
    channel = client.get_channel(812974446801059860)
    await channel.send("MonarchMusicBot is online")

    #joins vc on ready
    channel = client.get_channel(815933179378270208)
    await channel.connect()


#RETURNS BOT'S PING IN MILLISECONDS
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong motherfucker {client.latency * 1000}ms")


'''
#GTA V roast meme LAMAR SIDE
@client.command(aliases = ["loc", "Loc", "LOC", "crib", "Crib", "gtavroast", "GTAVroast"])
async def _loclamar(ctx):
    for i in range(1):
        time.sleep(float(0))
        await ctx.send("Wassup, can a loc come up in your crib?\n")
        time.sleep(float(2.5))
        await ctx.send("Ah, n-word, don't hate me 'cause I'm beautiful, n-word.")
        time.sleep(float(0.5))
        await ctx.send("Maybe if you got rid of that old yee-yee ass haircut you got")
        time.sleep(float(0.5))
        await ctx.send("you'd get some bitches on your dick.")
        time.sleep(float(0.5))
        await ctx.send("Oh, better yet,")
        time.sleep(float(0.25))
        await ctx.send("maybe Tanisha'll call your dog-ass")
        time.sleep(float(0.50))
        await ctx.send("if she ever stop fucking with that brain surgeon or lawyer she fucking with")
        time.sleep(float(0.75))
        await ctx.send("N-word")
'''


'''START OF MUSIC AND VOICE CHANNEL RELATED COMMANDS'''

'''
#VOICE CHANNEL JOIN
@client.command(pass_context = True, aliases = ["Join", "join", "j", "J", "connect", "Connect"])
async def _join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send("I joined your voice channel :D")
        print("MonarchBot joined a voice channel")


#VOICE CHANNEL LEAVE
@client.command(pass_context = True, aliases = ["Leave", "leave", "L", "l", "Disconnect", "disconnect"])
async def _leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild = ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"MonarchBot is disconnected from {channel} voice channel")
        await ctx.send(f"I left the '{channel}' voice channel :(")
    else:
        print("command given to leave voice channel but bot wasn't in a voice channel")
        await ctx.send("Invalid command: bot wasn't in any voice channels retard")


#VOICE CHANNEL PLAY YOUTUBE URL
@client.command(pass_context = True, aliases = ["play", "Play", "p", "P"])
async def _play(ctx, url: str):
    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_queue = length - 1 #outprints how many are left in queue after new song is played
            try:
                first_file = os.listdir(DIR)[0] #first file inside directory
            except:
                print("No more songs in queue\n")
                queues.clear
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "//" + first_file)
            
            if length != 0:
                print("Sone finished playing, loading next song\n")
                print(f"Songs still in queue: {still_queue}")
                is_song_there = os.path.isfile("song.mp3")
                if is_song_there: 
                    os.remove("song.mp3")
                shutil.move(song_path, main_location) #moves queued song to main directory
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, "song.mp3")
                vcvoice.play(discord.FFmpegPCMAudio("song.mp3"), after = lambda e: check_queue()) #plays the song
                vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
                vcvoice.source.value = 0.05
            
            else: #if queues = 0, clearns it
                queues.clear()
                return

        else: #is there is no queue folder
            queues.clear
            print("No songs queued after last song\n")

    #end of queue section thingy for play command
    is_song_there = os.path.isfile("song.mp3")
    try: #code will try to remove song, if it's playing then no remove
        if is_song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed an old song file")
    except PermissionError:
        print("Failed to remove song file, song file in use")
        ctx.send("Error: song file cannot be removed because it's playing idiot")
        return

    #this section is here to remove the old queue folder
    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:   #if there is an old queue file, it will try to remove it
            print("Removed old queue folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old queue folder")

    #rest of play command to play songs
    await ctx.send("Getting everything ready :D (this may take a bit to load)")
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "256",
        }], #code above to specify options in ydl
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloaded audio file\n")
        ydl.download([url])
    #renames file name 
    for file in os.listdir("./"): #./ for current directory
        if file.endswith(".mp3"):
            audio_file_name = file
            print(f"Renamed File {file}\n")
            os.rename(file, "song.mp3")
    #checks to see if audio has finished playing, after then it will print
    vcvoice.play(discord.FFmpegPCMAudio("song.mp3"), after = lambda e: check_queue())
    vcvoice.source = discord.PCMVolumeTransformer(vcvoice.source)
    vcvoice.source.value = 0.05
    new_name = audio_file_name.rsplit("-", 2)
    await ctx.send(f"Playing {new_name}")
    print("playing\n")


#VOICE CHANNEL MUSIC PAUSE COMMAND
@client.command(pass_context = True, aliases = ["pause", "Pause"])
async def _pause(ctx):
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    
    if vcvoice and voice.is_playing():
        vcvoice.pause()
        print("Music paused")
        await ctx.send("Music paused")
    else:
        print("Music wasn't playing but there was a request to pause music")
        await ctx.send("Music wasn't playing so i can't pause it retard")


#VOICE CHANNEL MUSIC RESUME COMMAND
@client.command(pass_context = True, aliases = ["resume", "Resume"])
async def _resume(ctx):
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)
    
    if vcvoice and voice.is_paused():
        vcvoice.resume()
        print("Music resumed")
        await ctx.send("Music has been resumed pogs")
    else:
        print("Music was not paused but a request was sent for music pause")
        await ctx.send("Music can't be resumed if it wasn't paused dumbass smh")


#VOICE CHANNEL MUSIC STOP COMMAND
@client.command(pass_context = True, aliases = ["stop", "Stop"])
async def _stop(ctx):
    vcvoice = discord.utils.get(client.voice_clients, guild = ctx.guild)

    queues.clear() #clears queue when stop command ran

    if vcvoice and voice.is_playing():
        vcvoice.stop()
        print("Music stopped")
        await ctx.send("Music stopped")
    else:
        print("Music could not be stopped")
        await ctx.send("Music can't be stopped if there aint music playing")


#VOICE CHANNEL MUSIC queue
#this command is for music to be queued up if you use the ".play" multiple times while music is still playing
queues = {}

@client.command(pass_context = True, aliases = ["Queue", "queue", "Q", "q"])
async def _queue(ctx, url: str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")      #sees if there is any song files in queue, if there is any then it counts them
    DIR = os.path.abspath(os.path.realpath("Queue"))
    queue_num = len(os.listdir(DIR)) #gets/counts ammount of files in the queue
    queue_num += 1 #adds another to queue
    add_queue = True
    while add_queue:
        if queue_num in queues:
            queue_num += 1
        else:
            add_queue = False
            queues[queue_num] = queue_num
        
    queue_path = os.path.abspath(os.path.realpath("Queue") + f"//song{queue_num}.%(ext)s")
    #takes the real path of song in queue and number of it
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl" : queue_path,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "1024",
        }], #code above to specify options in ydl
    }
    #downloads song and puts into queue path above ^
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloaded audio file\n")
        ydl.download([url])
    await ctx.send("Adding song " + str(queue_num) + " to the queue")
    print("added a song to queue\n")
'''

import discord
from discord.ext import commands
import random
import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
import youtube_dl
from youtube_dl import YoutubeDL

# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''

ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # ipv6 addresses cause issues sometimes
}

ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)


class VoiceConnectionError(commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')
        self.duration = data.get('duration')

        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        embed = discord.Embed(title="", description=f"Queued [{data['title']}]({data['webpage_url']}) [{ctx.author.mention}]", color=discord.Color.green())
        await ctx.send(embed=embed)

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer:
    """A class which is assigned to each guild using the bot for Music.
    This class implements a queue and loop, which allows for different guilds to listen to different playlists
    simultaneously.
    When the bot disconnects from the Voice it's instance will be destroyed.
    """

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = .5
        self.current = None

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(300):  # 5 minutes...
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'There was an error processing your song.\n'
                                             f'```css\n[{e}]\n```')
                    continue

            source.volume = self.volume
            self.current = source

            self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
            embed = discord.Embed(title="Now playing", description=f"[{source.title}]({source.web_url}) [{source.requester.mention}]", color=discord.Color.green())
            self.np = await self._channel.send(embed=embed)
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(commands.Cog):
    """Music related commands."""

    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, commands.NoPrivateMessage):
            try:
                return await ctx.send('This command can not be used in Private Messages.')
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send('Error connecting to Voice Channel. '
                           'Please make sure you are in a valid channel or provide me with one')

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @commands.command(name='join', aliases=['connect', 'j'], description="connects to voice")
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        """Connect to voice.
        Parameters
        ------------
        channel: discord.VoiceChannel [Optional]
            The channel to connect to. If a channel is not specified, an attempt to join the voice channel you are in
            will be made.
        This command also handles moving the bot to different channels.
        """
        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                embed = discord.Embed(title="", description="No channel to join. Please call `,join` from a voice channel.", color=discord.Color.green())
                await ctx.send(embed=embed)
                raise InvalidVoiceChannel('No channel to join. Please either specify a valid channel or join one.')

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')
        if (random.randint(0, 1) == 0):
            await ctx.message.add_reaction('👍')
        await ctx.send(f'**Joined `{channel}`**')

    @commands.command(name='play', aliases=['sing','p'], description="streams music")
    async def play_(self, ctx, *, search: str):
        """Request a song and add it to the queue.
        This command attempts to join a valid voice channel if the bot is not already in one.
        Uses YTDL to automatically search and retrieve a song.
        Parameters
        ------------
        search: str [Required]
            The song to search and retrieve using YTDL. This could be a simple search, an ID or URL.
        """
        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)

        player = self.get_player(ctx)

        # If download is False, source will be a dict which will be used later to regather the stream.
        # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

        await player.queue.put(source)

    @commands.command(name='pause', description="pauses music")
    async def pause_(self, ctx):
        """Pause the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            embed = discord.Embed(title="", description="I am currently not playing anything", color=discord.Color.green())
            return await ctx.send(embed=embed)
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.send("Paused ⏸️")

    @commands.command(name='resume', description="resumes music")
    async def resume_(self, ctx):
        """Resume the currently paused song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel", color=discord.Color.green())
            return await ctx.send(embed=embed)
        elif not vc.is_paused():
            return

        vc.resume()
        await ctx.send("Resuming ⏯️")

    @commands.command(name='skip', description="skips to next song in queue")
    async def skip_(self, ctx):
        """Skip the song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel", color=discord.Color.green())
            return await ctx.send(embed=embed)

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        vc.stop()
    
    @commands.command(name='remove', aliases=['rm', 'rem'], description="removes specified song from queue")
    async def remove_(self, ctx, pos : int=None):
        """Removes specified song from queue"""

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel", color=discord.Color.green())
            return await ctx.send(embed=embed)

        player = self.get_player(ctx)
        if pos == None:
            player.queue._queue.pop()
        else:
            try:
                s = player.queue._queue[pos-1]
                del player.queue._queue[pos-1]
                embed = discord.Embed(title="", description=f"Removed [{s['title']}]({s['webpage_url']}) [{s['requester'].mention}]", color=discord.Color.green())
                await ctx.send(embed=embed)
            except:
                embed = discord.Embed(title="", description=f'Could not find a track for "{pos}"', color=discord.Color.green())
                await ctx.send(embed=embed)
    
    @commands.command(name='clear', aliases=['clr', 'cl', 'cr'], description="clears entire queue")
    async def clear_(self, ctx):
        """Deletes entire queue of upcoming songs."""

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel", color=discord.Color.green())
            return await ctx.send(embed=embed)

        player = self.get_player(ctx)
        player.queue._queue.clear()
        await ctx.send('**Cleared**')

    @commands.command(name='queue', aliases=['q', 'playlist', 'que'], description="shows the queue")
    async def queue_info(self, ctx):
        """Retrieve a basic queue of upcoming songs."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel", color=discord.Color.green())
            return await ctx.send(embed=embed)

        player = self.get_player(ctx)
        if player.queue.empty():
            embed = discord.Embed(title="", description="queue is empty", color=discord.Color.green())
            return await ctx.send(embed=embed)

        seconds = vc.source.duration % (24 * 3600) 
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        if hour > 0:
            duration = "%dh %02dm %02ds" % (hour, minutes, seconds)
        else:
            duration = "%02dm %02ds" % (minutes, seconds)

        # Grabs the songs in the queue...
        upcoming = list(itertools.islice(player.queue._queue, 0, int(len(player.queue._queue))))
        fmt = '\n'.join(f"`{(upcoming.index(_)) + 1}.` [{_['title']}]({_['webpage_url']}) | ` {duration} Requested by: {_['requester']}`\n" for _ in upcoming)
        fmt = f"\n__Now Playing__:\n[{vc.source.title}]({vc.source.web_url}) | ` {duration} Requested by: {vc.source.requester}`\n\n__Up Next:__\n" + fmt + f"\n**{len(upcoming)} songs in queue**"
        embed = discord.Embed(title=f'Queue for {ctx.guild.name}', description=fmt, color=discord.Color.green())
        embed.set_footer(text=f"{ctx.author.display_name}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=embed)

    @commands.command(name='np', aliases=['song', 'current', 'currentsong', 'playing'], description="shows the current playing song")
    async def now_playing_(self, ctx):
        """Display information about the currently playing song."""
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel", color=discord.Color.green())
            return await ctx.send(embed=embed)

        player = self.get_player(ctx)
        if not player.current:
            embed = discord.Embed(title="", description="I am currently not playing anything", color=discord.Color.green())
            return await ctx.send(embed=embed)
        
        seconds = vc.source.duration % (24 * 3600) 
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        if hour > 0:
            duration = "%dh %02dm %02ds" % (hour, minutes, seconds)
        else:
            duration = "%02dm %02ds" % (minutes, seconds)

        embed = discord.Embed(title="", description=f"[{vc.source.title}]({vc.source.web_url}) [{vc.source.requester.mention}] | `{duration}`", color=discord.Color.green())
        embed.set_author(icon_url=self.bot.user.avatar_url, name=f"Now Playing 🎶")
        await ctx.send(embed=embed)

    @commands.command(name='volume', aliases=['vol', 'v'], description="changes Kermit's volume")
    async def change_volume(self, ctx, *, vol: float=None):
        """Change the player volume.
        Parameters
        ------------
        volume: float or int [Required]
            The volume to set the player to in percentage. This must be between 1 and 100.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I am not currently connected to voice", color=discord.Color.green())
            return await ctx.send(embed=embed)
        
        if not vol:
            embed = discord.Embed(title="", description=f"🔊 **{(vc.source.volume)*100}%**", color=discord.Color.green())
            return await ctx.send(embed=embed)

        if not 0 < vol < 101:
            embed = discord.Embed(title="", description="Please enter a value between 1 and 100", color=discord.Color.green())
            return await ctx.send(embed=embed)

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        embed = discord.Embed(title="", description=f'**`{ctx.author}`** set the volume to **{vol}%**', color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(name='leave', aliases=["stop", "dc", "disconnect", "bye"], description="stops music and disconnects from voice")
    async def leave_(self, ctx):
        """Stop the currently playing song and destroy the player.
        !Warning!
            This will destroy the player assigned to your guild, also deleting any queued songs and settings.
        """
        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            embed = discord.Embed(title="", description="I'm not connected to a voice channel", color=discord.Color.green())
            return await ctx.send(embed=embed)

        if (random.randint(0, 1) == 0):
            await ctx.message.add_reaction('👋')
        await ctx.send('**Successfully disconnected**')

        await self.cleanup(ctx.guild)


def setup(bot):
    bot.add_cog(Music(bot))

'''END OF MUSIC AND VOICE CHANNEL RELATED COMMANDS'''


keep_alive()
client.run(BOT_TOKEN)
