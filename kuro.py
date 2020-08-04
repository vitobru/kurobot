#Kuro Bot v0.01 - by Vitobru
import os
import random

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

print('Kuro Bot v0.01 - by Vitobru')
print('Kuro is ready!')

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
    ]
    
    response = random.choice(kuro_quotes)
    await ctx.send(response)

@bot.command(name='kiss', help='[NSFW] gives out a gif of kissing from our one and only succubus.')
async def kisses(ctx):
    kuro_kiss = [
        'https://cdn.discordapp.com/attachments/734623501788512258/739787730476859502/kuro-illya-makeout.gif',
        'https://img2.gelbooru.com/images/6a/9e/6a9e51ca1241bc59a9a556e946078cb0.gif',
        'https://i.pinimg.com/originals/f3/e8/e4/f3e8e48b571ea57d0e013fa508346b7b.gif',
    ]
    
    response = random.choice(kuro_kiss)
    await ctx.send(response)

bot.run(TOKEN)
