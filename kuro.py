#client
import os
import random

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hey, {member.name}. Welcome to the server. Sit down and relax or something. The lolis are here.'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    kuro_quotes = [
        'Mana supply, pretty please?',
        (
            '...What is that look for? '
            'I get it, everyone else is taking off their clothes and wearing new outfits. '
            'You were looking forward to it, weren’t you? What a pervert.'
        ),
        'I’m a little tired. Mana transfer please, Master',
    ]
    
    if message.content == '!quotes':
        response = random.choice(kuro_quotes)
        await message.channel.send(response)

client.run(TOKEN)
