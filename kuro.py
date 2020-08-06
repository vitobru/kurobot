#KuroBot v0.3.4
import discord, pickledb, random, time, math, re, youtube_dl, os, glob, uuid, datetime

initTime = time.time()

print("Clearing temp files...")
files = glob.glob('./*.mp3')
for file in files:
    try:
        os.remove(file)
    except:
        print("Error while deleting ",file)

# put your token into the "token" file.

TOKEN=str(open("token","r").read())

client = discord.Client()

version = "0.3.4"

prefix = "$"

vclients = {}

disabledCommands=pickledb.load('disabledCommands.db',False)
prefixes=pickledb.load('prefixes.db',False)

def setDB(database,key,val):
    if(database.set(key,val)):
        database.dump()
        return 1
    else:
        return -1

class NoopLogger(object):
    def debug(self, msg):
        pass
    def warning(self, msg):
        pass
    def error(self, msg):
        pass

print('Kuro Bot v'+version+' - by Vitobru and armeabi')

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if isinstance(message.channel, discord.DMChannel):
        return
    
    disabled = disabledCommands.get(str(message.guild.id))
    if disabled is not False:
        if message.content.replace(prefix,"") in disabled:
            if(message.content.replace(prefix,"") in ["disable","setprefix"]):
                pass
            else:
                return
        else:
            pass
    else:
        pass

    if message.content == (prefix+'invite'):
        embed = discord.Embed(title="KuroBot v"+version, description="**Invite Kuro to your server!**\nUse this [invite](https://discord.com/api/oauth2/authorize?client_id=740065310727602236&permissions=36816897&scope=bot) to invite her~")
        embed.set_thumbnail(url=client.user.avatar_url)
        embed.set_footer(text="KuroBot")
        embed.add_field(name="Thank you for considering using KuroBot!", value=":heart:")
        await message.channel.send(embed=embed)
    
    if message.content.startswith(prefix+'disable'):
        admFlag=0
        for role in message.author.roles:
            if(role.permissions.manage_server):
                admFlag=1
        if(admFlag==1):
            todisable = " ".join(message.content.split(" ")[1:])
            if((setDB(disabledCommands,str(message.guild.id),todisable))==1):
                await message.channel.send("Success.")
        else:
            await message.channel.send("You don't seem to have the `Manage Server` permission in any of your roles.")

    if message.content.startswith(prefix+'nsfw'):
        if(not message.channel.is_nsfw()):
            await message.channel.send("Hm, it seems this channel isn't marked NSFW. Try again somewhere else.")
            return
        args = message.content.split(" ")[1:]
        if args[0]=="kiss":
            kuro_kiss = [                                                                                     
                'https://cdn.discordapp.com/attachments/734623501788512258/739787730476859502/kuro-illya-makeout.gif',
                'https://img2.gelbooru.com/images/6a/9e/6a9e51ca1241bc59a9a556e946078cb0.gif',
                'https://i.pinimg.com/originals/f3/e8/e4/f3e8e48b571ea57d0e013fa508346b7b.gif',       
                'https://pa1.narvii.com/6202/814df9da373b94a18c76e1e7b4283a8e619f801f_hq.gif',       
                'https://img2.gelbooru.com/images/6d/71/6d7117d93a9d99d60a97edc5595b240d.gif']
            response = random.choice(kuro_kiss)
            await message.channel.send(response)
        elif args[0]=="quote":
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
            await message.channel.send(response)
        elif args[0]=="e621":
            await message.channel.send("**Source coming soon!**")
            return
        elif args[0]=="danbooru":
            await message.channel.send("**Source coming soon!**")
            return
        elif args[0]=="gelbooru":
            await message.channel.send("**Source coming soon!**")
            return
        elif args[0]=="rule34":
            await message.channel.send("**Source coming soon!**")
            return
        elif args[0]=="paheal":
            await message.channel.send("**Source coming soon!**")
            return
        elif args[0]=="yandere":
            await message.channel.send("**Source coming soon!**")
            return
        else:
            await message.channel.send("Invalid source.")
            
    if message.content == (prefix+'join'):
        for vc in message.guild.voice_channels:
            for memb in vc.members:
                try:
                    if memb.id == message.author.id:
                        vclients[message.guild.id] = await vc.connect()
                except:
                    await message.channel.send("You must be in a VC.")
        
    if message.content == (prefix+'leave'):
        if(not message.author.id == 408372847652634624):
            return
        else:
            try:
                if(vclients[message.guild.id]):
                    await vclients[message.guild.id].disconnect()
                    await message.channel.send("Leaving...")
            except:
                await message.channel.send("I'm not in a VC.")
    
    if message.content.startswith(prefix+'play'):
        linkstr = "".join(message.content.split(" ")[1:])
        validator = re.compile(
        r'^(?:http)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if(re.match(validator, linkstr)is not None):
            filename = str(uuid.uuid4())
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'outtmpl': filename+".tmp",
                'logger': NoopLogger()
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([linkstr])
                filename = filename+".mp3"
                for vc in message.guild.voice_channels:                                                       
                    for memb in vc.members:                                                                   
                        if memb.id == message.author.id:                                                      
                            try:                                                                              
                                if(vclients[message.guild.id]):                                               
                                    if(vclients[message.guild.id].is_playing() or vclients[message.guild.id].is_paused()):                                                                                                  
                                        await message.channel.send("I'm already playing something.")          
                                    else:                                                                     
                                        await message.channel.send("Playing now...")                          
                                        vclients[message.guild.id].play(discord.FFmpegPCMAudio(filename))     
                            except:                                                                           
                                vclients[message.guild.id] = await vc.connect()                               
                                await message.channel.send("Playing now...")                                  
                                vclients[message.guild.id].play(discord.FFmpegPCMAudio(filename))
        elif(len(message.attachments)>0):
            if("mp3" in message.attachments[0].url):
                filename = str(uuid.uuid4())+".mp3"
                await message.attachments[0].save(filename)
                for vc in message.guild.voice_channels:
                    for memb in vc.members:
                        if memb.id == message.author.id:
                            try:
                                if(vclients[message.guild.id]):
                                    if(vclients[message.guild.id].is_playing() or vclients[message.guild.id].is_paused()):
                                        await message.channel.send("I'm already playing something.")
                                    else:
                                        await message.channel.send("Playing now...")
                                        vclients[message.guild.id].play(discord.FFmpegPCMAudio(filename))
                            except:
                                vclients[message.guild.id] = await vc.connect()
                                await message.channel.send("Playing now...")
                                vclients[message.guild.id].play(discord.FFmpegPCMAudio(filename))
            else:
                await message.channel.send("I can't play anything from attachments other than MP3 files.")
        else:
            await message.channel.send("Invalid music link.")
            return

    if message.content == (prefix+'pause'):
        if(vclients[message.guild.id].is_paused()):
            await message.channel.send("I'm already paused.")
            return
        else:
            vclients[message.guild.id].pause()
            await message.channel.send("Pausing...")

    if message.content == (prefix+'resume'):
        if(vclients[message.guild.id].is_playing()):
            await message.channel.send("I'm already playing something.")
            return
        else:
            vclients[message.guild.id].resume()
            await message.channel.send("Resuming...")

    if message.content == (prefix+'stop'):
        if(vclients[message.guild.id]):
            vclients[message.guild.id].stop()
            await message.channel.send("Stopping...")
        else:
            await message.channel.send("I'm not playing anything.")

    if message.content.startswith(prefix+'purge'):
        admFlag=0
        for role in message.author.roles:
            if(role.permissions.manage_messages):
                admFlag=1
        if(admFlag==1):
            try:
                howmany = int(message.content.split(" ")[1])
            except:
                await message.channel.send("Invalid argument for how many messages to be deleted.")
                return
            # boilerplate makes me want to kill myself
            deleted = await message.channel.purge(limit=howmany)
            await message.channel.send('Deleted {} message(s).'.format(len(deleted)))
        else:
            await message.channel.send("You don't seem to have the `Manage Messages` permission in any of your roles.")

    if message.content.startswith(prefix+'whois'):
        user_query = message.mentions[0]
        embed = discord.Embed()
        rolenames = []
        for role in user_query.roles:
            rolenames.append(role.name)
        rolenames = rolenames[1:]
        embed.set_thumbnail(url=user_query.avatar_url)
        embed.set_author(name="Whois: "+user_query.name)
        embed.set_footer(text="KuroBot")
        embed.add_field(name="Full name:", value=user_query.name+"#"+user_query.discriminator, inline=True)
        embed.add_field(name="Nickname:", value=user_query.nick, inline=True)
        embed.add_field(name="Joined:", value=user_query.joined_at.strftime("%m/%d/%Y, at %I:%M:%S %p in the timezone of this server"), inline=True)
        embed.add_field(name="ID", value=user_query.id, inline=True)
        embed.add_field(name="Roles ["+str(len(user_query.roles[1:]))+"]", value=",".join(rolenames), inline=True)
        embed.add_field(name="Created:", value=user_query.created_at.strftime("%m/%d/%Y, at %I:%M:%S %p UTC"), inline=True)
        await message.channel.send(embed=embed)
            
    if message.content == (prefix+'kuro'):
        file = discord.File("resources/kuro.png", filename="kuro.png")
        embed = discord.Embed(title="Kuro")
        embed.set_image(url="attachment://kuro.png")
        embed.set_footer(text="KuroBot")
        await message.channel.send(file=file, embed=embed)
        
    if message.content == (prefix+'latency'):
        timestr = str(round(client.latency,3))
        timestr = timestr.replace(".","")
        timestr = timestr.lstrip("0")
        embed = discord.Embed(title="Latency")
        embed.set_footer(text="KuroBot")
        embed.add_field(name="millis", value=(timestr))
        await message.channel.send(embed=embed)

    if message.content == (prefix+'uptime'):
        tsecs=math.floor(time.time()-initTime)
        secs=tsecs%60
        tmins=tsecs//60 # 1 min = 60 secs
        mins=tmins%60
        thrs=tmins//60 # 1 hr = 60 mins
        hrs=thrs%60
        tdys=thrs//24 # 1 dy = 24 hrs
        dys=tdys%24
        embed = discord.Embed(title="Uptime")
        embed.set_footer(text="KuroBot")
        embed.add_field(name="seconds", value=str(secs))
        embed.add_field(name="minutes", value=str(mins))
        embed.add_field(name="hours", value=str(hrs))
        embed.add_field(name="days", value=str(dys))
        await message.channel.send(embed=embed)
    
    if message.content == (prefix+'about'):
        embed = discord.Embed(title="KuroBot v"+version, description="A bot written in discord.py by\nvito#1072 and armeabi#3621.")
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/740369729188921345/740404293718245376/smug-upscale.png?width=529&height=482")
        embed.set_footer(text="KuroBot")
        embed.add_field(name="GitHub", value="https://github.com/vitobru/kurobot")
        await message.channel.send(embed=embed)

    if message.content == (prefix+'exit'):
        if(not message.author.id == 408372847652634624):
            return
        else:
            await message.channel.send("Okay, master...")
            await client.logout()
            quit()
    
    if message.content == (prefix+'help'):
        embed = discord.Embed()
        embed.set_footer(text="KuroBot")
        embed.add_field(name="about", value="will show an about dialog,\nshowing info about the bot.", inline=True)
        embed.add_field(name="disable", value="[ADMIN ONLY] disables commands,\nseparate multiples with spaces.",inline=True)
        embed.add_field(name="google", value="lemme google that for ya. \nreturns a google URL for \nwhatever you typed in.", inline=True)
        embed.add_field(name="nsfw", value="[NSFW] multi-source nsfw command,\ndocs will be created soon.", inline=True)
        embed.add_field(name="whois", value="mention a user and get\ninfo about them.",inline=True)
        embed.add_field(name="kuro", value="simply sends a kuro.", inline=True)
        embed.add_field(name="uptime", value="returns the bot's uptime.",inline=True)
        embed.add_field(name="latency", value="returns the bot's latency.",inline=True)
        embed.add_field(name="leave", value="[OWNER ONLY] disconnects kuro from vc.", inline=True)
        embed.add_field(name="join", value="has kuro join your channel.",inline=True)
        embed.add_field(name="play", value="plays an uploaded mp3\nfile or youtube/soundcloud\netc. link", inline=True)
        embed.add_field(name="purge", value="[ADMIN ONLY] purges up to 100 messages\nfrom a channel.", inline=True)
        embed.add_field(name="pause", value="pauses music playback.",inline=True)
        embed.add_field(name="resume", value="resumes music playback.",inline=True)
        embed.add_field(name="stop", value="stops music playback.",inline=True)
        embed.add_field(name="more to be added soon", value="please check back for\nmore commands!", inline=True)

        await message.channel.send(embed=embed)
        
    if message.content.startswith(prefix+'google'):
        query = "+".join(message.content.split(" ")[1:])
        embed = discord.Embed(description="https://www.google.com/search?hl=en_US&q="+query)
        embed.set_author(name="Google Search")
        embed.set_footer(text="KuroBot")
        await message.channel.send(embed=embed)

client.run(TOKEN)
