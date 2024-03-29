#KuroBot v0.7.5-indev
import discord, logging, random, time, math, os, datetime, sys
from discord.ext import tasks, commands

import cogs.disable
import utils.help
import config.config as config

logging.basicConfig(level=logging.WARNING)

intents = discord.Intents.default()
intents.members = True

initTime = time.time()

activity = discord.Activity(type=config.ACTIVITY_TYPE,
                            name=config.ACTIVITY_NAME)

bot = commands.Bot(command_prefix='$', activity=activity, help_command=utils.help.HelpCommand())

version = "0.7.5-indev"

platform = str(sys.platform)

print('Kuro Bot v'+version+' - by vitobru and alatartheblue42')
print('Running on: '+platform)
print('Loading extensions...')

for extension in config.EXTENSIONS:
    try:
        bot.load_extension(extension)
    except Exception as err:
        print(err)
        logging.log(logging.ERROR, "Failed to load extension: {extension}!")
print("Loading extensions complete!")

async def is_dev(ctx):
    return ctx.author.id in config.DEVS

@tasks.loop(minutes=30)
async def clear_mp3():
    try:
        print("Clearing temp files...")
        if sys.platform.startswith('linux'):
            os.system("rm -f resources/*.mp3")
            os.system("rm -f *.rdb")
        elif sys.platform.startswith('win32'):
            os.system("del /q resources\*.mp3")
            os.system("del /q resources\*.tmp")
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

@bot.command(name='prefix', help='fetches kuro\'s current prefix.')
@cogs.disable.Disable.is_disabled()
async def prefix(ctx):
    response = "The current set prefix is: `"+bot.command_prefix+"`"
    await ctx.send(response)

@prefix.error
async def prefix_error(ctx, error):
    if isinstance(error, cogs.disable.Disabled):
        await ctx.send(error)

@bot.command(name='invite', help='sends an embed with kuro\'s invite link.')
@cogs.disable.Disable.is_disabled()
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
    if isinstance(error, cogs.disable.Disabled):
        await ctx.send(error)

@bot.group(name='nsfw', help='contains NSFW commands.')
@commands.is_nsfw()
@cogs.disable.Disable.is_disabled()
async def nsfw(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('NSFW isn\'t a command. It\'s a group.')

@nsfw.error
async def nsfw_channel(ctx, error):
    if isinstance(error, commands.errors.NSFWChannelRequired):
        await ctx.send("This isn't an NSFW channel, dumbass.")
    if isinstance(error, cogs.disable.Disabled):
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

@bot.command(name='purge', help='has kuro delete up to 100 messages.')
@commands.has_guild_permissions(manage_messages=True)
@cogs.disable.Disable.is_disabled()
async def purge(ctx, arg):
    try:
        howmany = int(arg)
    except:
        await ctx.send("Invalid argument for how many messages to be deleted.")
        return
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
    if isinstance(error, cogs.disable.Disabled):
        await ctx.send(error)

@bot.command(name='whois', help='fetches a mentioned user\'s info.')
@cogs.disable.Disable.is_disabled()
async def whois(ctx, member: discord.Member):
    embed = discord.Embed()
    rolenames = []
    if member.id != 261232036625252352:
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
    else:
        embed.set_thumbnail(url=member.avatar_url)
        embed.set_author(name="Whois: "+member.name)
        embed.set_footer(text="KuroBot")
        embed.add_field(name="Huh?", value="I don't really know who this guy is. They don't actually do any work.")
        await ctx.send(embed=embed)

@whois.error
async def whois_error(ctx, error):
    if isinstance(error, cogs.disable.Disabled):
        await ctx.send(error)

@bot.command(name='kuro', help='sends a kuro.')
@cogs.disable.Disable.is_disabled()
async def kuro(ctx):
    file = discord.File("resources/kuro.png", filename="kuro.png")
    embed = discord.Embed(title="Kuro")
    embed.set_image(url="attachment://kuro.png")
    embed.set_footer(text="KuroBot")
    await ctx.send(file=file, embed=embed)

@kuro.error
async def kuro_error(ctx, error):
    if isinstance(error, cogs.disable.Disabled):
        await ctx.send(error)

@bot.command(name='latency', help="displays kuro's current latency")
@cogs.disable.Disable.is_disabled()
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
    if isinstance(error, cogs.disable.Disabled):
        await ctx.send(error)

@bot.command(name='uptime', help='will display an embed showing how long kuro has been running for.')
@cogs.disable.Disable.is_disabled()
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
    if isinstance(error, cogs.disable.Disabled):
        await ctx.send(error)

@bot.command(name='about', help='will show an about dialog,\nshowing info about the bot.')
@cogs.disable.Disable.is_disabled()
async def about(ctx):
    embed = discord.Embed(title="KuroBot v"+version, description="A bot written in discord.py by\nvito#1072 and\nalatartheblue42#1891.")
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.set_footer(text="KuroBot")
    embed.add_field(name="Website", value="http://sgecrest.ddns.net")
    embed.add_field(name="GitHub", value=config.REPO_LINK)
    await ctx.send(embed=embed)

@about.error
async def about_error(ctx, error):
    if isinstance(error, cogs.disable.Disabled):
        await ctx.send(error)

@bot.command(name='alpha-warning', help='displays message relating\nto alpha release.')
@cogs.disable.Disable.is_disabled()
async def alpha(ctx):
    embed = discord.Embed(title="This is only an alpha release!", description="Kuro is currently only in her alpha release stage,\nmeaning that she's not perfect.\nPlease submit any complaints to:\nalatartheblue42#1891 or vito#1072")
    embed.set_thumbnail(url=bot.user.avatar_url)
    embed.set_footer(text="KuroBot")
    await ctx.send(embed=embed)

@alpha.error
async def alpha_error(ctx, error):
    if isinstance(error, cogs.disable.Disabled):
        await ctx.send(error)

@bot.command(name='test', help='[DEVS ONLY] has Kuro echo your message.')
@commands.check(is_dev)
@cogs.disable.Disable.is_disabled()
async def test(ctx, *args):
    args = " ".join(args)
    await ctx.send(args)

@test.error
async def test_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('You don\'t have permission to use that command.')
    if isinstance(error, cogs.disable.Disabled):
        await ctx.send(error)

@bot.command(name='exit', help="[OWNER ONLY] shuts-down KuroBot.")
@commands.check(is_dev)
@cogs.disable.Disable.is_disabled()
async def exit(ctx):
    await ctx.send("Okay, master...")
    await bot.logout()

@exit.error
async def exit_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send('You don\'t have permission to make me leave.')
    if isinstance(error, cogs.disable.Disabled):
        await ctx.send(error)

@bot.command(name='google', help='kuro will google whatever you typed.')
@cogs.disable.Disable.is_disabled()
async def google(ctx, *args):
    query = "+".join(args)
    embed = discord.Embed(description="https://www.google.com/search?hl=en_US&q="+query)
    embed.set_author(name="Google Search")
    embed.set_footer(text="KuroBot")
    await ctx.send(embed=embed)

@google.error
async def google_error(ctx, error):
    if isinstance(error, cogs.disable.Disabled):
        await ctx.send(error)

if __name__ == '__main__':
    bot.run(config.TOKEN)