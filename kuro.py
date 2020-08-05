import discord
import pickledb
import random

# put your token into the "token" file.

TOKEN=str(open("token","r").read())

client = discord.Client()

@client.event
async def on_ready():
    print('Kuro Bot v0.1.1 - by Vitobru and armeabi')
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == ('$about'):
        embed = discord.Embed(title="KuroBot v0.1.1", description="A bot written in discord.py by\nvito#1072 and armeabi#3621.")
        embed.set_thumbnail(url="https://media.discordapp.net/attachments/740369729188921345/740404293718245376/smug-upscale.png?width=529&height=482")
        embed.set_footer(text="KuroBot")
        embed.add_field(name="GitHub", value="https://github.com/vitobru/kurobot")
        await message.channel.send(embed=embed)

    if message.content == ('$fuckoff'):
        if(not message.author.id == 437748282731659271):
            return
        else:
            await message.channel.send("Okay, master... ;-;")
            await client.logout()
            quit()
    
    if message.content == ('$kiss'):
        if(not message.channel.is_nsfw()):
            await message.channel.send("B-baka, this channel isn't NSFW! Go somewhere else! o////o")
            return

        kuro_kiss = [
        'https://cdn.discordapp.com/attachments/734623501788512258/739787730476859502/kuro-illya-makeout.gif',
        'https://img2.gelbooru.com/images/6a/9e/6a9e51ca1241bc59a9a556e946078cb0.gif',
        'https://i.pinimg.com/originals/f3/e8/e4/f3e8e48b571ea57d0e013fa508346b7b.gif',
        'https://pa1.narvii.com/6202/814df9da373b94a18c76e1e7b4283a8e619f801f_hq.gif',
        'https://img2.gelbooru.com/images/6d/71/6d7117d93a9d99d60a97edc5595b240d.gif',
        ]

        response = random.choice(kuro_kiss)
        await message.channel.send(response)

    if message.content == ('$help'):
        embed = discord.Embed()
        embed.set_footer(text="KuroBot")
        embed.add_field(name="about", value="will show an about dialog,\nshowing info about the bot.", inline=True)
        embed.add_field(name="google", value="lemme google that for ya. \nreturns a google URL for \nwhatever you typed in.", inline=True)
        embed.add_field(name="quote", value="returns a Kuro quote from\nF/GO or Kaleid Liner.", inline=True)
        embed.add_field(name="kiss", value="[NSFW] gives out a gif of\nkissing from our one and\nonly succubus.", inline=True)
        embed.add_field(name="more to be added soon", value="please check back for\nmore commands!", inline=True)

        await message.channel.send(embed=embed)
        
    if message.content == ('$quote'):
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
            ),
        ]

        response = random.choice(kuro_quotes)
        await message.channel.send(response)
    
    if message.content.startswith('$google'):
        query = "+".join(message.content.split(" ")[1:])
        embed = discord.Embed(description="https://www.google.com/search?hl=en_US&q="+query)
        embed.set_author(name="Google Search")
        embed.set_footer(text="KuroBot")
        await message.channel.send(embed=embed)

client.run(TOKEN)
