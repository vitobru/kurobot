#Kuro Bot v0.01 - by Vitobru
import os
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

print('Kuro Bot v0.01 - by Vitobru')

@bot.event
async def on_ready():
    print(f'Kuro is ready!')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hey, {member.name}. Welcome to the server. Sit around and relax or something.'
    )

@bot.command(name='about', help='will show an about dialog, showing info about the bot.')
async def about(ctx):
    response = '``Kuro Bot v0.01 - Written in Python by Vitobru``     URL: https://github.com/vitobru/kurobot'
    await ctx.send(response)

@bot.command(name='test', help='will send the text that follows the command as a test.')
async def test(ctx, *, arg):
    await ctx.send(arg)

@bot.command(name='quotes', help='has kuro give out quotes from F/GO or Kaleid Liner')
async def quotes(ctx):
    kuro_quotes = [
        'Mana supply, pretty please?',
        (
            '...What is that look for? '
            'I get it, everyone else is taking off their clothes and wearing new outfits. '
            'You were looking forward to it, weren’t you? What a pervert.'
        ),
        'I’m a little tired. Mana transfer please, Master',
        'I’m low on energy... Isn’t there a cute girl filled with some to spare around here somewhere? A Caster would be perfect.',
        (
            'I wonder what your magical energy tastes like… '
            'Hey, no need to run away. I was just kidding, silly. '
            'If I was serious, you wouldn’t be able to resist. You wouldn’t want to.'
        ),
        (
            'It’s strange... I feel at ease just being in the same room as you. '
            'You’re the first I’ve felt this way with, outside of my family. '
            'Can I borrow your shoulder . . . just for a minute?'
        ),
    ]
    
    response = random.choice(kuro_quotes)
    await ctx.send(response)

@bot.command(name='kiss', help='[NSFW] gives out a gif of kissing from our one and only succubus.')
@commands.has_role('Cultured')
async def kisses(ctx):
    kuro_kiss = [
        'https://cdn.discordapp.com/attachments/734623501788512258/739787730476859502/kuro-illya-makeout.gif',
        'https://img2.gelbooru.com/images/6a/9e/6a9e51ca1241bc59a9a556e946078cb0.gif',
        'https://i.pinimg.com/originals/f3/e8/e4/f3e8e48b571ea57d0e013fa508346b7b.gif',
        'https://pa1.narvii.com/6202/814df9da373b94a18c76e1e7b4283a8e619f801f_hq.gif',
        'https://img2.gelbooru.com/images/6d/71/6d7117d93a9d99d60a97edc5595b240d.gif',
    ]
    
    response = random.choice(kuro_kiss)
    await ctx.send(response)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')

bot.run(TOKEN)
