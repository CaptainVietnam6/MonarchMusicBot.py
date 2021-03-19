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


'''END OF MUSIC AND VOICE CHANNEL RELATED COMMANDS'''


keep_alive()
client.run(BOT_TOKEN)
