#KuroBot v0.6.1-indev
import discord, random, time, math, re, youtube_dl, os, uuid, datetime, redis, json, aiosqlite
from aiosqlite import Error
from discord.ext import tasks, commands
from typing import Optional
intents = discord.Intents.default()
intents.members = True

initTime = time.time()

#Put your token into the "token" file.

TOKEN=str(open("token","r").read())

bot = commands.Bot(command_prefix='%')

version = "0.6.1-indev"

vclients = {}

queues = redis.Redis(host='localhost',port=6379,db=0)

async def createtable():
    db = await aiosqlite.connect(r'resources/disabled.db')
    await db.execute("CREATE TABLE IF NOT EXISTS disabled (guild_id integer NOT NULL, command text NOT NULL);")
    await db.commit()
    await db.close()

class Disabled(commands.CheckFailure):
    pass

def is_disabled():
    async def predicate(ctx):
        await createtable()
        db = await aiosqlite.connect(r'resources/disabled.db')
        cursor = await db.execute("SELECT guild_id, command FROM disabled WHERE guild_id = "+str(ctx.guild.id)+" AND command = '"+str(ctx.command)+"';")
        fetch = await cursor.fetchone()
        if fetch is not None: #checks to make sure the row isn't empty or non-existent or whatever
            fetch = str(fetch[1])
            if fetch in ("disable","enable"): #makes sure the disabled command isn't the disable or enable commands
                await db.close()
                raise Disabled("This command cannot be disabled.")
            else: #handles if the disabled command is actually disabled
                await db.close()
                raise Disabled("This command has been disabled.")
        else:
            await db.close()
            return True
    return commands.check(predicate)

async def is_dev(ctx):
    return ctx.author.id in (408372847652634624,261232036625252352)

class NoopLogger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        pass

print('Kuro Bot v'+version+' - by vitobru and alatartheblue42')

@tasks.loop(seconds=5.0)
async def ensure_queue_loop():
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
ensure_queue_loop.start()

@tasks.loop(minutes=30)
async def clear_mp3():
    try:
        print("Clearing temp files...")
        os.system("rm -f resources/*.mp3")
        os.system("rm -f *.rdb")
    except:
        print("No files were found to clear.")
clear_mp3.start()

@bot.event
async def on_ready():
    print('Logged in as '+bot.user.name+"#"+bot.user.discriminator)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

@bot.command(name='queue', help='queue?')
@is_disabled()
async def queue(ctx):
    queue = queues.get(ctx.guild.id)
    await ctx.send(queue)

@queue.error
async def queue_error(ctx, error):
    if isinstance(error, Disabled):
        await ctx.send(error)

@bot.command(name='disable', help='hopefully disables the specified command.')
@commands.has_guild_permissions(manage_guild=True)
async def disable(ctx, arg):
    await createtable()
    db = await aiosqlite.connect(r'resources/disabled.db')
    try:
        arg = str(arg)
        insert = """INSERT INTO disabled
        VALUES ("""+str(ctx.guild.id)+""", '"""+arg+"""');"""
        await db.execute(insert)
        await db.commit()
        await db.close()
        await ctx.send("Success.")
    except:
        insert = """INSERT INTO disabled
        VALUES ("""+str(ctx.guild.id)+""", '"""+arg+"""');"""
        await ctx.send("Couldn't perform operation.")
        await ctx.send("The attempted query was: `"+insert+"`")
        await db.close()

@disable.error
async def disable_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You must have Manage Server permissions enabled. Sorry.")

@bot.command(name='enable', help='hopefully re-enables the specified command.')
@commands.has_guild_permissions(manage_guild=True)
async def enable(ctx, arg):
    arg = str(arg)
    await createtable()
    db = await aiosqlite.connect(r'resources/disabled.db')
    try:
        cursor = await db.execute("SELECT guild_id, command FROM disabled WHERE guild_id = "+str(ctx.guild.id)+" AND command = '"+arg+"';")
        delete = """DELETE FROM disabled
        WHERE guild_id = """+str(ctx.guild.id)+"""
        AND command = '"""+arg+"""';
        """
        await cursor.execute(delete)
        await db.commit()
        await db.close()
        await ctx.send("Success.")
    except:
        delete = """DELETE FROM disabled
        WHERE guild_id = """+str(ctx.guild.id)+"""
        AND command = '"""+arg+"""';
        """
        await ctx.send("Couldn't perform operation.")
        await ctx.send("The attempted query was: `"+delete+"`")
        await db.close()     

@enable.error
async def enable_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You must have Manage Server permissions enabled. Sorry.")

@bot.command(name='prefix', help='fetches kuro\'s current prefix.')
@is_disabled()
async def prefix(ctx):
    response = "The current set prefix is: `"+bot.command_prefix+"`"
    await ctx.send(response)

@prefix.error
async def prefix_error(ctx, error):
    if isinstance(error, Disabled):
        await ctx.send(error)

@bot.command(name='invite', help='sends an embed with kuro\'s invite link.')
@is_disabled()
async def invite(ctx):
    embed = discord.Embed(
        title="KuroBot v"+version,
        description="**Invite Kuro to your server!**\nUse this [invite](https://discord.com/api/oauth2/authorize?client_id=740065310727602236&permissions=36816897&scope=bot) to invite her~"
    )
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.set_footer(text="KuroBot")
    embed.add_field(name="Thank you for considering using KuroBot!", value=":heart:")
    await ctx.send(embed=embed)

@invite.error
async def invite_error(ctx, error):
    if isinstance(error, Disabled):
        await ctx.send(error)

@bot.group(name='nsfw')
@commands.is_nsfw()
@is_disabled()
async def nsfw(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('NSFW isn\'t a command. It\'s a group.')

@nsfw.error
async def nsfw_channel(ctx, error):
    if isinstance(error, commands.errors.NSFWChannelRequired):
        await ctx.send("This isn't an NSFW channel, dumbass.")
    if isinstance(error, Disabled):
        await ctx.send(error)

@nsfw.command(name='kiss')
async def kiss(ctx):
    kuro_kiss = [
        'https://cdn.discordapp.com/attachments/734623501788512258/739787730476859502/kuro-illya-makeout.gif',
        'https://img2.gelbooru.com/images/6a/9e/6a9e51ca1241bc59a9a556e946078cb0.gif',
        'https://i.pinimg.com/originals/f3/e8/e4/f3e8e48b571ea57d0e013fa508346b7b.gif',
        'https://pa1.narvii.com/6202/814df9da373b94a18c76e1e7b4283a8e619f801f_hq.gif',
        'https://img2.gelbooru.com/images/6d/71/6d7117d93a9d99d60a97edc5595b240d.gif']
    response = random.choice(kuro_kiss)
    await ctx.send(response)

@nsfw.command(name='quote')
async def quote(ctx):
    kuro_quotes = [
        'Mana supply, pretty please?',
    (
        '...What is that look for? '
        'I get it, everyone else is taking off their clothes and wearing new outfits. '
        'You were looking forward to it, weren\'t you? What a pervert.'
    ),
        'I\'m a little tired. Mana transfer please, Master.',
        'I\'m low on energy... Isn\'t there a cute girl filled with some to spare around here somewhere? A Caster would be perfect.',
    (
        'I wonder what your magical energy tastes like... '
        'Hey, no need to run away. I was just kidding, silly. '
        'If I was serious, you wouldn\'t be able to resist. You wouldn\'t want to.'
    ),
    (
        'It\'s strange... I feel at ease just being in the same room as you. '
        'You\'re the first I\'ve felt this way with, outside of my family. '
        'Can I borrow your shoulder . . . just for a minute?'
    )]
    response = random.choice(kuro_quotes)
    await ctx.send(response)

@nsfw.command(name='e621')
async def e621(ctx):
    await ctx.send("**Source coming soon!**")

@nsfw.command(name='danbooru')
async def danbooru(ctx):
    await ctx.send("**Source coming soon!**")

@nsfw.command(name='gelbooru')
async def gelbooru(ctx):
    await ctx.send("**Source coming soon!**")

@nsfw.command(name='rule34')
async def rule34(ctx):
    await ctx.send("**Source coming soon!**")

@bot.command(name='join', help='has kuro join the voice channel you are in.')
@is_disabled()
async def join(ctx):
    for vc in ctx.guild.voice_channels:
        for memb in vc.members:
            if memb.id == ctx.author.id:
                vclients[ctx.guild.id] = await vc.connect()
            else:
                await ctx.send('You must be in a VC for me to join.')

@join.error
async def join_error(ctx, error):
    if isinstance(error, Disabled):
        await ctx.send(error)

@bot.command(name='stop', help='has kuro stop any playing music and leave the VC')
@commands.has_guild_permissions(priority_speaker=True)
@is_disabled()
async def stop(ctx):
    if(vclients[ctx.guild.id]):
        await vclients[ctx.guild.id].disconnect()
        await ctx.send("Stopping...")

@stop.error
async def stop_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You must have Priority Speaker permissions.")
    if isinstance(error, Disabled):
        await ctx.send(error)

@bot.command(name='play', help='has kuro play a youtube link or uploaded file.')
@is_disabled()
async def play(ctx, link: Optional[str]):
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
async def play_error(ctx, error):
    if isinstance(error, Disabled):
        await ctx.send(error)

@bot.command(name='pause')
@is_disabled()
async def pause(ctx):
    if(vclients[ctx.guild.id].is_paused()):
        await ctx.send("I'm already paused.")
        return
    else:
        vclients[ctx.guild.id].pause()
        await ctx.send("Pausing...")

@pause.error
async def pause_error(ctx, error):
    if isinstance(error, Disabled):
        await ctx.send(error)

@bot.command(name='resume')
@is_disabled()
async def resume(ctx):
    if(vclients[ctx.guild.id].is_playing()):
        await ctx.send("I'm already playing something.")
        return
    else:
        vclients[ctx.guild.id].resume()
        await ctx.send("Resuming...")

@resume.error
async def resume_error(ctx, error):
    if isinstance(error, Disabled):
        await ctx.send(error)

@bot.command(name='skip')
@is_disabled()
async def skip(ctx):
    if(vclients[ctx.guild.id]):
        vclients[ctx.guild.id].stop()
        await ctx.send("Skipping...")
    else:
        await ctx.send("I'm not playing anything.")

@skip.error
async def skip_error(ctx, error):
    if isinstance(error, Disabled):
        await ctx.send(error)

@bot.command(name='purge', help='has kuro delete up to 100 messages.')
@commands.has_guild_permissions(manage_messages=True)
@is_disabled()
async def purge(ctx, arg):
    try:
        howmany = int(arg)
    except:
        await ctx.send("Invalid argument for how many messages to be deleted.")
        return
    #boilerplate makes me want to kill myself
    if howmany == 0:
        ctx.send("I can't delete no messages.")
    elif howmany > 100:
        ctx.send("I can't delete more than 100 messages.")
    else:
        deleted = await ctx.channel.purge(limit=howmany)
        await ctx.send('Deleted {} message(s).'.format(len(deleted)))

@purge.error
async def purge_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You must have Manage Messages permissions enabled. Sorry.")
    if isinstance(error, Disabled):
        await ctx.send(error)

@bot.command(name='whois', help='fetches a mentioned user\'s info.')
@is_disabled()
async def whois(ctx, member: discord.Member):
    embed = discord.Embed()
    rolenames = []
    for role in member.roles:
        rolenames.append(role.name)
    if len(rolenames) != 1:
        rolenames = rolenames[1:]
    embed.set_thumbnail(url=member.avatar_url)
    embed.set_author(name="Whois: "+member.name)
    embed.set_footer(text="KuroBot")
    embed.add_field(name="Full name:", value=member.name+"#"+member.discriminator, inline=True)
    embed.add_field(name="Nickname:", value=member.nick, inline=True)
    embed.add_field(name="Joined:", value=member.joined_at.strftime("%m/%d/%Y, at %I:%M:%S %p in the timezone of this server"), inline=True)
    embed.add_field(name="ID", value=member.id, inline=True)
    embed.add_field(name="Roles ["+str(len(rolenames))+"]", value=",".join(rolenames), inline=True)
    embed.add_field(name="Created:", value=member.created_at.strftime("%m/%d/%Y, at %I:%M:%S %p UTC"), inline=True)
    await ctx.send(embed=embed)

@whois.error
async def whois_error(ctx, error):
    if isinstance(error, Disabled):
        await ctx.send(error)

@bot.command(name='kuro', help='sends a kuro.')
@is_disabled()
async def kuro(ctx):
    file = discord.File("resources/kuro.png", filename="kuro.png")
    embed = discord.Embed(title="Kuro")
    embed.set_image(url="attachment://kuro.png")
    embed.set_footer(text="KuroBot")
    await ctx.send(file=file, embed=embed)

@kuro.error
async def kuro_error(ctx, error):
    if isinstance(error, Disabled):
        await ctx.send(error)

@bot.command(name='latency', help="displays kuro's current latency")
@is_disabled()
async def latency(ctx):
    timestr = str(round(bot.latency,3))
    timestr = timestr.replace(".","")
    timestr = timestr.lstrip("0")
    embed = discord.Embed(title="Latency")
    embed.set_footer(text="KuroBot")
    embed.add_field(name="millis", value=(timestr))
    await ctx.send(embed=embed)

@latency.error
async def latency_error(ctx, error):
    if isinstance(error, Disabled):
        await ctx.send(error)

@bot.command(name='uptime', help='will display an embed showing how long kuro has been running for.')
@is_disabled()
async def uptime(ctx):
    # implementing part of the GNU coreutils uptime
    uptime=math.floor(time.time()-initTime)
    upsecs=uptime%60
    updays=uptime//86400
    uphours=(uptime-(updays*86400))//3600
    upmins=(uptime-(updays*86400)-(uphours*3600))//60
    embed = discord.Embed(title="Uptime")
    embed.set_footer(text="KuroBot")
    embed.add_field(name="days", value=str(updays))
    embed.add_field(name="hours", value=str(uphours))
    embed.add_field(name="minutes", value=str(upmins))
    embed.add_field(name="seconds", value=str(upsecs))
    await ctx.send(embed=embed)

@uptime.error
async def uptime_error(ctx, error):
    if isinstance(error, Disabled):
        await ctx.send(error)

@bot.command(name='about', help='will show an about dialog,\nshowing info about the bot.')
@is_disabled()
async def about(ctx):
    embed = discord.Embed(title="KuroBot v"+version, description="A bot written in discord.py by\nvito#1072 and\nalatartheblue42#1891.")
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.set_footer(text="KuroBot")
    embed.add_field(name="GitHub", value="https://github.com/vitobru/kurobot")
    await ctx.send(embed=embed)

@about.error
async def about_error(ctx, error):
    if isinstance(error, Disabled):
        await ctx.send(error)

@bot.command(name='alpha-warning', help='displays message relating\nto alpha release.')
@is_disabled()
async def alpha(ctx):
    embed = discord.Embed(title="This is only an alpha release!", description="Kuro is currently only in her alpha release stage,\nmeaning that she's not perfect.\nPlease submit any complaints to:\nalatartheblue42#1891 or vito#1072")
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.set_footer(text="KuroBot")
    await ctx.send(embed=embed)

@alpha.error
async def alpha_error(ctx, error):
    if isinstance(error, Disabled):
        await ctx.send(error)

@bot.command(name='test')
@commands.check(is_dev)
@is_disabled()
async def test(ctx, *args):
    args = " ".join(args)
    await ctx.send(args)

@test.error
async def test_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('You don\'t have permission to use that command.')
    if isinstance(error, Disabled):
        await ctx.send(error)

@bot.command(name='exit', help="[OWNER ONLY] shuts-down KuroBot.")
@commands.check(is_dev)
@is_disabled()
async def exit(ctx):
    await ctx.send("Okay, master...")
    await bot.logout()

@exit.error
async def exit_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('You don\'t have permission to make me leave.')
    if isinstance(error, Disabled):
        await ctx.send(error)

@bot.command(name='bot')
async def pleh(ctx):
    embed = discord.Embed()
    embed.set_footer(text="KuroBot")
    #embed.add_field(name="about", value="will show an about dialog,\nshowing info about the bot.", inline=True)
    embed.add_field(name="disable", value="[ADMIN ONLY] disables commands,\nseparate multiples with spaces.", inline=True)
    #embed.add_field(name="google", value="lemme google that for ya. \nreturns a google URL for \nwhatever you typed in.", inline=True)
    #embed.add_field(name="exit", value="[OWNER ONLY] shuts-down KuroBot.", inline=True)
    #embed.add_field(name="alpha-warning", value="displays message relating\nto alpha release.")
    embed.add_field(name="nsfw", value="[NSFW] multi-source nsfw command,\ndocs will be created soon.", inline=True)
    #embed.add_field(name="whois", value="mention a user and get\ninfo about them.", inline=True)
    #embed.add_field(name="kuro", value="simply sends a kuro.", inline=True)
    #embed.add_field(name="uptime", value="returns the bot's uptime.", inline=True)
    #embed.add_field(name="latency", value="returns the bot's latency.", inline=True)
    embed.add_field(name="stop", value="[ADMIN ONLY] disconnects kuro from vc.", inline=True)
    embed.add_field(name="join", value="has kuro join your channel.", inline=True)
    embed.add_field(name="play", value="plays an uploaded mp3\nfile or youtube/soundcloud\netc. link", inline=True)
    embed.add_field(name="purge", value="[ADMIN ONLY] purges up to 100 messages\nfrom a channel.", inline=True)
    #embed.add_field(name="prefix", value="lists kuro's currently set prefix", inline=True)
    embed.add_field(name="pause", value="pauses music playback.", inline=True)
    embed.add_field(name="resume", value="resumes music playback.", inline=True)
    embed.add_field(name="skip", value="skips current song.", inline=True)
    embed.add_field(name="more to be added soon", value="please check back for\nmore commands!", inline=True)
    await ctx.send(embed=embed)

@bot.command(name='google', help='kuro will google whatever you typed.')
@is_disabled()
async def google(ctx, *args):
    query = "+".join(args)
    embed = discord.Embed(description="https://www.google.com/search?hl=en_US&q="+query)
    embed.set_author(name="Google Search")
    embed.set_footer(text="KuroBot")
    await ctx.send(embed=embed)

@google.error
async def google_error(ctx, error):
    if isinstance(error, Disabled):
        await ctx.send(error)

bot.run(TOKEN)