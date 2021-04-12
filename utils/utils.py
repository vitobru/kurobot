import asyncio
import datetime
import config.config as config
import discord
from discord.ext import commands

class Embed(discord.Embed):
    """Embed with some prebuilt values."""
    def __init__(self):
        """Creates a new embed."""
        super().__init__()
        self.color = config.EMBED_COLOR
        self.timestamp = datetime.datetime.now()


async def confirm(ctx: commands.Context, *,
                  prompt = "Are you sure?",
                  fields = {},
                  timeout = 15):
    """Confirm box for bot functions.
    **Parameters**
    ctx: Context
    prompt: The description of the embed. 
    fields: Additional fields for the embed. Optional.
      This should be a dict in {name: value} format.
    timeout: Time (in seconds) before the embed closes.
    """
    bot = ctx.bot
    buttons = ['✅', '⛔']
    embed = Embed()
    embed.color = discord.Color(0xff0000)
    embed.set_author(name=ctx.author.display_name,
                     icon_url=ctx.author.avatar_url)
    embed.title = f"Action Required - Answer in {timeout}s"
    embed.description = prompt
    for key in fields:
        embed.add_field(name=key, value=fields[key])
    embed.set_footer(text=f"{buttons[0]} to confirm, {buttons[1]} to deny.")
    dialog = await ctx.reply(embed=embed)
    for react in buttons:
        await dialog.add_reaction(react)

    def _is_valid_reaction(reaction, user) -> bool:
        """Helper check."""
        return (str(reaction) in buttons and 
                user == ctx.author and
                reaction.message == dialog)
    
    try:
        response, _ = await bot.wait_for('reaction_add', timeout = timeout,
                                         check = _is_valid_reaction)
        await dialog.delete()
        if str(response) == buttons[0]:
            return True
        return False
    except asyncio.TimeoutError:
        await dialog.delete()
        return False