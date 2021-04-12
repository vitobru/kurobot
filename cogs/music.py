"""Handles music commands and functions"""
import re
import redis
import json
import youtube_dl
import uuid

import discord
import discord.ext.commands as commands
from discord.ext.commands import Cog
from discord.ext import tasks
from typing import Optional

import cogs.disable

class NoopLogger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        pass

vclients = {}

queues = redis.Redis(host='localhost',port=6379,db=0)

class Music(Cog):
    
    @tasks.loop(seconds=5.0)
    async def ensure_queue_loop(self): #facilitates the queue for the bot's music feature
        try:
            for vc in vclients.values():
                if vc.is_playing() or vc.is_paused():
                    return
                else:
                    next_song=""
                    queue=[]
                    try:
                        queue = json.loads(queues.get(vc.guild.id))
                        next_song = queue[0]
                        queue = queue[1:]
                        queues.set(vc.guild.id,json.dumps(queue))
                        vc.play(discord.FFmpegPCMAudio(next_song))
                    except:
                        pass
        except:
            pass
    
    def __init__(self):
        self.ensure_queue_loop.start()

    @commands.command(name='play', help='has kuro play a youtube link or uploaded file.')
    @cogs.disable.Disable.is_disabled()
    async def play(self, ctx, link: Optional[str]):
        if link is not None:
            linkstr = "".join(link)
            validator = re.compile(
            r'^(?:http)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' #optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            if(re.match(validator, linkstr)is not None):
                if "list" in linkstr:
                    await ctx.send("Playlist functionality is not supported in this bot. Sorry!")
                    return
                if "playlist" in linkstr:
                    await ctx.send("Playlist functionality is not supported in this bot. Sorry!")
                    return
                filename = str(uuid.uuid4())
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': "resources/"+filename+".tmp",
                    'logger': NoopLogger()
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([linkstr])
                    filename = "resources/"+filename+".mp3"
                    for vc in ctx.guild.voice_channels:
                        for memb in vc.members:
                            if memb.id == ctx.author.id:
                                try:
                                    if(vclients[ctx.guild.id]):
                                        if(vclients[ctx.guild.id].is_playing() or vclients[ctx.guild.id].is_paused()):
                                            queue = []
                                            try:
                                                queue = json.loads(queues.get(ctx.guild.id))
                                            except:
                                                queue = [filename]
                                            if(isinstance(queue, bytes)):
                                                queue = [filename]
                                            else:
                                                queue.append(filename)
                                            queues.set(ctx.guild.id,json.dumps(queue))
                                            await ctx.send("Added to queue.")
                                        else:
                                            await ctx.send("Playing now...")
                                            vclients[ctx.guild.id].play(discord.FFmpegPCMAudio(filename))
                                except:
                                    vclients[ctx.guild.id] = await vc.connect()
                                    await ctx.channel.send("Playing now...")
                                    vclients[ctx.guild.id].play(discord.FFmpegPCMAudio(filename))
            else:
                await ctx.send("Invalid music link.")
                return
        else:
            if(len(ctx.message.attachments)>0):
                if("mp3" in ctx.message.attachments[0].url):
                    filename = "resources/"+str(uuid.uuid4())+".mp3"
                    await ctx.message.attachments[0].save(filename)
                    for vc in ctx.guild.voice_channels:
                        for memb in vc.members:
                            if memb.id == ctx.author.id:
                                try:
                                    if(vclients[ctx.guild.id]):
                                        if(vclients[ctx.guild.id].is_playing() or vclients[ctx.guild.id].is_paused()):
                                            queue = []
                                            try:
                                                queue = json.loads(queues.get(ctx.guild.id))
                                            except:
                                                queue = [filename]
                                            if(isinstance(queue, bytes)):
                                                queue = [filename]
                                            else:
                                                queue.append(filename)
                                            queues.set(ctx.guild.id,json.dumps(queue))
                                            await ctx.send("Added to queue.")
                                        else:
                                            await ctx.send("Playing now...")
                                            vclients[ctx.guild.id].play(discord.FFmpegPCMAudio(filename))
                                except:
                                    vclients[ctx.guild.id] = await vc.connect()
                                    await ctx.send("Playing now...")
                                    vclients[ctx.guild.id].play(discord.FFmpegPCMAudio(filename))
                else:
                    await ctx.send("I can't play anything from attachments other than MP3 files.")
                    return

    @play.error
    async def play_error(self, ctx, error):
        if isinstance(error, cogs.disable.Disabled):
            await ctx.send(error)

    @commands.command(name='queue', help='queue?')
    @cogs.disable.Disable.is_disabled()
    async def queue(self, ctx):
        queue = queues.get(ctx.guild.id)
        await ctx.send(queue)

    @queue.error
    async def queue_error(self, ctx, error):
        if isinstance(error, cogs.disable.Disabled):
            await ctx.send(error)

    @commands.command(name='join', help='has kuro join the voice channel you are in.')
    @cogs.disable.Disable.is_disabled()
    async def join(self, ctx):
        await ctx.send("If I do not connect to the channel, leave and rejoin the voice channel to mitigate this issue. Thank you! :heart:")
        for vc in ctx.guild.voice_channels:
            for memb in vc.members:
                if memb.id == ctx.author.id:
                    vclients[ctx.guild.id] = await vc.connect()
                else:
                    await ctx.send('You must be in a VC for me to join.')

    @join.error
    async def join_error(self, ctx, error):
        if isinstance(error, cogs.disable.Disabled):
            await ctx.send(error)

    @commands.command(name='stop', help='has kuro stop any playing music and leave the VC')
    @commands.has_guild_permissions(priority_speaker=True)
    @cogs.disable.Disable.is_disabled()
    async def stop(self, ctx):
        if(vclients[ctx.guild.id]):
            await vclients[ctx.guild.id].disconnect()
            await ctx.send("Stopping...")

    @stop.error
    async def stop_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You must have Priority Speaker permissions.")
        if isinstance(error, cogs.disable.Disabled):
            await ctx.send(error)

    @commands.command(name='pause')
    @cogs.disable.Disable.is_disabled()
    async def pause(self, ctx):
        if(vclients[ctx.guild.id].is_paused()):
            await ctx.send("I'm already paused.")
            return
        else:
            vclients[ctx.guild.id].pause()
            await ctx.send("Pausing...")

    @pause.error
    async def pause_error(self, ctx, error):
        if isinstance(error, cogs.disable.Disabled):
            await ctx.send(error)

    @commands.command(name='resume')
    @cogs.disable.Disable.is_disabled()
    async def resume(self, ctx):
        if(vclients[ctx.guild.id].is_playing()):
            await ctx.send("I'm already playing something.")
            return
        else:
            vclients[ctx.guild.id].resume()
            await ctx.send("Resuming...")

    @resume.error
    async def resume_error(self, ctx, error):
        if isinstance(error, cogs.disable.Disabled):
            await ctx.send(error)

    @commands.command(name='skip')
    @cogs.disable.Disable.is_disabled()
    async def skip(self, ctx):
        if(vclients[ctx.guild.id]):
            vclients[ctx.guild.id].stop()
            await ctx.send("Skipping...")
        else:
            await ctx.send("I'm not playing anything.")

    @skip.error
    async def skip_error(self, ctx, error):
        if isinstance(error, cogs.disable.Disabled):
            await ctx.send(error)

def setup(bot: commands.Bot):
    bot.add_cog(Music())