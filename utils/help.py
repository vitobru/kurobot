import math

import discord
from discord.ext import commands

import utils.utils as util

COMMANDS_PER_PAGE = 10

class HelpCommand(commands.DefaultHelpCommand):
    def __init__(self, **options):
        super().__init__(**options)
        # self.command_attrs = {"usage" : "[command]",
        #                       "description" : "Sends this message.",
        #                       "aliases" : ["halp"],
        #                       "name" : "help"}
        self.command_attrs['usage'] = "[command]"
        self.verify_checks = True

    async def send_command_help(self, command: commands.Command):
        try:
            if await command.can_run(ctx=self.context):
                embed = util.Embed()
                embed.title = self.clean_prefix + command.qualified_name
                embed.description = command.help
                if command.cog_name:
                    embed.add_field(name="Category", value=command.cog_name, 
                                    inline=False)
                if command.usage:
                    embed.add_field(name="Usage",
                                    value=self.clean_prefix +
                                          command.qualified_name + ' ' +
                                          command.usage,
                                    inline=False)
                else:
                    embed.add_field(name="Usage",
                                    value=self.clean_prefix +
                                          command.qualified_name)
                if command.aliases:
                    embed.add_field(name="Aliases", value=", ".join(command.aliases),
                                    inline=False)
                if command.description:
                    embed.set_footer(text = command.description)
                await self.get_destination().send(embed=embed)
            else:
                await self.get_destination().send("You can't run this command here.\n",
                                        "If this is in error, try running this" +
                                        " from a place where you can use it.")
        except commands.NotOwner:
            await self.get_destination().send(self.command_not_found(command.name))
        except commands.CheckFailure:
            await self.get_destination().send("You can't run this command here.")

    async def send_group_help(self, group):
        embed = util.Embed()
        embed.title = self.clean_prefix + group.qualified_name
        embed.description = group.help + "\n\n" + self.get_ending_note()
        group_commands = await self.filter_commands(group.commands, sort=True)
        pagify = False if len(group_commands) <= 10 else True
        if pagify:
            pages = math.ceil(len(group_commands) / COMMANDS_PER_PAGE)
            page_on = 1
        for index, command in enumerate(group_commands):
            embed.add_field(name=command.name,
                            value=command.help,
                            inline=False)
            if (len(embed.fields) == COMMANDS_PER_PAGE and
                index != len(group_commands) - 1):
                # If there's enough subcommands to get here, pagify is True.
                embed.set_footer(text="Page " + str(page_on) +
                                      " of " + str(pages))
                await self.get_destination().send(embed = embed)
                embed.title = self.clean_prefix + group.qualified_name + " (cont.)"
                page_on += 1
                embed.clear_fields()
        if pagify:
            embed.set_footer(text="Page " + str(page_on) + " of " + str(pages))
        await self.get_destination().send(embed=embed)
        await self.context.message.add_reaction("👌")

    async def send_cog_help(self, cog: commands.Cog):
        """Sends the help message for all commands in the cog."""
        embed = util.Embed()
        embed.title = cog.qualified_name + " Commands"
        embed.description = self.get_ending_note()
        cog_commands = await self.filter_commands(cog.get_commands(),
                                                    sort=True)
        pages = math.ceil(len(cog_commands) / COMMANDS_PER_PAGE)
        page_on = 1
        for index, command in enumerate(cog_commands):
            embed.add_field(name=self.clean_prefix + command.name,
                            value=command.help,
                            inline=False)
            if len(embed.fields) == COMMANDS_PER_PAGE and index != len(cog_commands) - 1:
                embed.set_footer(text="Page " + str(page_on) +
                                      " of " + str(pages))
                await self.get_destination().send(embed = embed)
                embed.title = cog.qualified_name + " Commands (cont.)"
                page_on += 1
                embed.clear_fields()
        embed.set_footer(text="Page " + str(page_on) + " of " + str(pages))
        await self.get_destination().send(embed = embed)
        await self.context.message.add_reaction("👌")

    async def send_bot_help(self, mapping):
        """Sends the help message for all available commands."""
        all_commands = []
        for cog in mapping:
            all_commands.extend(mapping[cog])
        all_commands = await self.filter_commands(all_commands, sort=True)
        embed = util.Embed()
        embed.title = f"Commands for {self.context.bot.user.name}"
        embed.description = self.get_ending_note()
        pages = math.ceil(len(all_commands) / COMMANDS_PER_PAGE)
        page_on = 1
        for index, command in enumerate(all_commands):
            embed.add_field(name=self.clean_prefix + command.name,
                            value=command.help,
                            inline=False)
            if len(embed.fields) == COMMANDS_PER_PAGE and index != len(all_commands) - 1:
                embed.set_footer(text="Page " + str(page_on) +
                                      " of " + str(pages))
                await self.get_destination().send(embed = embed)
                embed.title = f"Commands for {self.context.bot.user.name} (cont.)"
                page_on += 1
                embed.clear_fields()
        embed.set_footer(text="Page " + str(page_on) + " of " + str(pages))
        await self.context.message.add_reaction("👌")
        await self.get_destination().send(embed = embed)

    def get_destination(self):
        return self.context

    def get_ending_note(self):
        return ("You have access to the following commands here.\n" +
                super().get_ending_note())