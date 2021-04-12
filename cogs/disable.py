import aiosqlite
from aiosqlite import Error

import discord
import discord.ext.commands as commands
from discord.ext.commands import Cog

class Disabled(commands.CheckFailure):
    pass

async def createtable():
    db = await aiosqlite.connect(r"D:\\Misc\\kurobot\\resources\disabled.db")
    await db.execute("CREATE TABLE IF NOT EXISTS disabled (guild_id integer NOT NULL, command text NOT NULL);")
    await db.commit()
    await db.close() #relatively self-explanatory, but it checks if the table has been created or not and makes it if it isn't

class Disable(Cog):

    def is_disabled():
        async def predicate(ctx):
            await createtable()
            db = await aiosqlite.connect(r"D:\\Misc\\kurobot\\resources\disabled.db")
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
    
    @commands.command(name='disable', help='hopefully disables the specified command.')
    @commands.has_guild_permissions(manage_guild=True)
    async def disable(self, ctx, arg):
        await createtable() #makes sure that the table is created, and ensures its creation if not
        db = await aiosqlite.connect(r'resources/disabled.db')
        try:
            arg = str(arg)
            insert = """INSERT INTO disabled
            VALUES ("""+str(ctx.guild.id)+""", '"""+arg+"""');"""
            await db.execute(insert)
            await db.commit()
            await db.close()
            await ctx.send("Success.")
        except: #remnant error handling from when i was trying to troubleshoot this goddamn system -lillie
            insert = """INSERT INTO disabled
            VALUES ("""+str(ctx.guild.id)+""", '"""+arg+"""');"""
            await ctx.send("Couldn't perform operation.")
            await ctx.send("The attempted query was: `"+insert+"`")
            await db.close()

    @disable.error
    async def disable_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You must have Manage Server permissions enabled. Sorry.")
    #yes, error handling would technically be overwritten by this, but since the database works, i don't fucking care :)

    @commands.command(name='enable', help='hopefully re-enables the specified command.')
    @commands.has_guild_permissions(manage_guild=True)
    async def enable(self, ctx, arg):
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
    async def enable_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("You must have Manage Server permissions enabled. Sorry.")

def setup(bot: commands.Bot):
    bot.add_cog(Disable())