import aiosqlite
import requests
from aiosqlite import Error

import discord
import discord.ext.commands as commands
from discord.ext.commands import Cog

class NSFW(Cog):
    headers = {
        'User-Agent': 'KuroBot / Contact cl6ver#1312, alatartheblue42#1891, or vito#1072 if this is misbehaving!'
    }

    def __init__(self):
        self._last_member = None

    @commands.command(name='fetch_e621', help='fetches NSFW from e621')
    @commands.is_nsfw()
    async def fetch_e621(self, ctx):
        """Fetches NSFW from e621."""
        response = requests.get("http://e621.net/tags.json", headers=self.headers)
        print(response)

def setup(bot: commands.Bot):
    bot.add_cog(NSFW())