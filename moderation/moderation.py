import datetime
import logging

logger = logging.getLogger("Modmail")

import discord
import typing
from discord.ext import commands

from core import checks
from core.models import PermissionLevel


class ModerationPlugin(commands.Cog):
    """
    Moderate ya server using modmail pog
    """

    def __init__(self, bot):
        self.bot = bot
        self.db = bot.plugin_db.get_partition(self)
        self.mod_ids = ['812426821010194463', '305446998658646020', '387594598182027264', '721761521755095160']
        print('Moderation by Donnie v1.2.0')

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def moderation(self, ctx: commands.Context):
        """
        Moderation by Donnie v1.2.0
        """
        await ctx.send_help(ctx.command)
        return

    @commands.command()
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def channel(self, ctx: commands.Context, channel: discord.TextChannel):
        """
        Set the log channel for moderation actions.
        """

        await self.db.find_one_and_update(
            {"_id": "config"}, {"$set": {"channel": channel.id}}, upsert=True
        )

        await ctx.send("Done!")
        return

    def isModmailThread(self, topic):
        if topic is None:
            print('Not modmail thread')
            return False

        components = topic.split(':')

        if components[1] is None:
            print('Not modmail thread')
            return False

        userID = components[1].strip()

        if len(userID) < 17 or len(userID) > 20:
            print('Not modmail thread')
            return False
        else:
            print('Is modmail thread')
            return True

    def getUserId(self, topic):
        if topic is None:
            print('No userID found')
            return None

        components = topic.split(':')

        if components[1] is None:
            print('No userID found')
            return None

        userID = components[1].strip()

        if len(userID) < 17 or len(userID) > 20:
            print('No userID found')
            return None
        else:
            print('UserID found')
            print('UserID:', userID)
            return userID

    # Do not EVER ban another mod
    def hasModRole(self, roles):
        for role in roles:
            if f"{role.id}" in self.mod_ids:
                return False

        return True

    @commands.command(aliases=["banhammer"])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def ban(
        self,
        ctx: commands.Context,
        member: typing.Union[typing.Optional[discord.User], typing.Optional[str]] = None,
        days: typing.Optional[int] = 0,
        *,
        reason: str = None,
    ):
        """Ban one or more users.
        Usage:
        {prefix}ban @member 10 Advertising their own products
        {prefix}ban Spamming (inside modmail thread)
        """

        config = await self.db.find_one({"_id": "config"})

        if config is None:
            return await ctx.send("There's no configured log channel.")
        else:
            channel = ctx.guild.get_channel(int(config["channel"]))

        if channel is None:
            await ctx.send("There is no configured log channel.")
            return

        print('Member Outer:', member)
        if member is None and self.isModmailThread(f"{ctx.channel.topic}"):
            userID = self.getUserId(ctx.channel.topic)

            try:
                rmds = await self.bot.fetch_guild(int("173554823633829888"))

                member = rmds.get_member(int(userID))

                if member is None:
                    member = await self.bot.fetch_user(int(member))

                print('Member:', member)

                if type(member) is discord.Member:
                    if hasModRole(member.roles):
                        ctx.send("Never again.")
                        return

                await ctx.guild.ban(member, delete_message_days=days, reason=f"{reason if reason else None}")

                embed = discord.Embed(
                    color=discord.Color.red(),
                    title=f"{member} was banned!",
                    timestamp=datetime.datetime.utcnow(),
                )

                embed.add_field(
                    name="Moderator",
                    value=f"{ctx.author}",
                    inline=False,
                )

                if reason:
                    embed.add_field(name="Reason", value=reason, inline=False)

                await ctx.send(f"🚫 | {member} is banned!")
                await channel.send(embed=embed)
            except discord.Forbidden:
                await ctx.send("I don't have the proper permissions to ban people.")

            except Exception as e:
                await ctx.send(
                    "An unexpected error occurred, please check the logs for more details."
                )
                logger.error(e)
                return
        elif member != None and type(member) is str:
            try:
                rmds = await self.bot.fetch_guild(int("173554823633829888"))

                member = rmds.get_member(int(member))

                if member is None:
                    member = await self.bot.fetch_user(int(member))

                print('Member:', member)

                if type(member) is discord.Member:
                    if hasModRole(member.roles):
                        ctx.send("Never again.")
                        return

                await ctx.guild.ban(member, delete_message_days=days, reason=f"{reason if reason else None}")

                embed = discord.Embed(
                    color=discord.Color.red(),
                    title=f"{member} was banned!",
                    timestamp=datetime.datetime.utcnow(),
                )

                embed.add_field(
                    name="Moderator",
                    value=f"{ctx.author}",
                    inline=False,
                )

                if reason:
                    embed.add_field(name="Reason", value=reason, inline=False)

                await ctx.send(f"🚫 | {member} is banned!")
                await channel.send(embed=embed)
            except discord.Forbidden:
                await ctx.send("I don't have the proper permissions to ban people.")

            except Exception as e:
                await ctx.send(
                    "An unexpected error occurred, please check the logs for more details."
                )
                logger.error(e)
                return
        elif member != None and type(member) is discord.User:
            try:
                rmds = await self.bot.fetch_guild(int("173554823633829888"))

                member = rmds.get_member(member.id)

                if member is None:
                    member = await self.bot.fetch_user(int(member))

                print('Member:', member)

                if type(member) is discord.Member:
                    if hasModRole(member.roles):
                        ctx.send("Never again.")
                        return
                
                await ctx.guild.ban(member, delete_message_days=days, reason=f"{reason if reason else None}")

                embed = discord.Embed(
                    color=discord.Color.red(),
                    title=f"{member} was banned!",
                    timestamp=datetime.datetime.utcnow(),
                )

                embed.add_field(
                    name="Moderator",
                    value=f"{ctx.author}",
                    inline=False,
                )

                if reason:
                    embed.add_field(name="Reason", value=reason, inline=False)

                await ctx.send(f"🚫 | {member} is banned!")
                await channel.send(embed=embed)
            except discord.Forbidden:
                await ctx.send("I don't have the proper permissions to ban people.")

            except Exception as e:
                await ctx.send(
                    "An unexpected error occurred, please check the logs for more details."
                )
                logger.error(e)
                return
        else:
            await ctx.send("This is not a modmail thread and you have not mentioned anyone.")

    @commands.command(aliases=["getout"])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def kick(
        self, ctx, member: typing.Union[typing.Optional[discord.Member], typing.Optional[int]], *, reason: str = None
    ):
        """Kick one or more users.
        Usage:
        {prefix}kick @member Being rude
        {prefix}kick Advertising (inside a modmail thread)
        """

        config = await self.db.find_one({"_id": "config"})

        if config is None:
            return await ctx.send("There's no configured log channel.")
        else:
            channel = ctx.guild.get_channel(int(config["channel"]))

        if channel is None:
            await ctx.send("There is no configured log channel.")
            return

        print('Member Outer:', member)
        if member is None and self.isModmailThread(f"{ctx.channel.topic}"):
            userID = self.getUserId(ctx.channel.topic)

            try:
                rmds = await self.bot.fetch_guild(int("173554823633829888"))

                member = rmds.get_member(int(userID))

                if member is None:
                    member = await self.bot.fetch_user(int(member))

                print('Member:', member)

                if type(member) is discord.Member:
                    if hasModRole(member.roles):
                        ctx.send("Never again.")
                        return

                await ctx.guild.kick(member, reason=f"{reason if reason else None}")

                embed = discord.Embed(
                    color=discord.Color.red(),
                    title=f"{member} was kicked!",
                    timestamp=datetime.datetime.utcnow(),
                )

                embed.add_field(
                    name="Moderator",
                    value=f"{ctx.author}",
                    inline=False,
                )

                if reason is not None:
                    embed.add_field(name="Reason", value=reason, inline=False)

                await ctx.send(f"🦶 | {member} is kicked!")
                await channel.send(embed=embed)

            except discord.Forbidden:
                await ctx.send("I don't have the proper permissions to kick people.")

            except Exception as e:
                await ctx.send(
                    "An unexpected error occurred, please check the Heroku logs for more details."
                )
                logger.error(e)
                return
        elif member != None and type(member) is str:
            try:
                rmds = await self.bot.fetch_guild(int("173554823633829888"))

                member = rmds.get_member(int(member))

                if member is None:
                    member = await self.bot.fetch_user(int(member))

                print('Member:', member)

                if type(member) is discord.Member:
                    if hasModRole(member.roles):
                        ctx.send("Never again.")
                        return

                await ctx.guild.kick(member, reason=f"{reason if reason else None}")
                embed = discord.Embed(
                    color=discord.Color.red(),
                    title=f"{member} was kicked!",
                    timestamp=datetime.datetime.utcnow(),
                )

                embed.add_field(
                    name="Moderator",
                    value=f"{ctx.author}",
                    inline=False,
                )

                if reason is not None:
                    embed.add_field(name="Reason", value=reason, inline=False)

                await ctx.send(f"🦶 | {member} is kicked!")
                await channel.send(embed=embed)

            except discord.Forbidden:
                await ctx.send("I don't have the proper permissions to kick people.")

            except Exception as e:
                await ctx.send(
                    "An unexpected error occurred, please check the Heroku logs for more details."
                )
                logger.error(e)
                return
        elif member != None and type(member) is discord.Member:
            try:
                if hasModRole(member.roles):
                    ctx.send("Never again.")
                    return
                
                await member.kick(reason=f"{reason if reason else None}")
                embed = discord.Embed(
                    color=discord.Color.red(),
                    title=f"{member} was kicked!",
                    timestamp=datetime.datetime.utcnow(),
                )

                embed.add_field(
                    name="Moderator",
                    value=f"{ctx.author}",
                    inline=False,
                )

                if reason is not None:
                    embed.add_field(name="Reason", value=reason, inline=False)

                await ctx.send(f"🦶 | {member} is kicked!")
                await channel.send(embed=embed)

            except discord.Forbidden:
                await ctx.send("I don't have the proper permissions to kick people.")

            except Exception as e:
                await ctx.send(
                    "An unexpected error occurred, please check the Heroku logs for more details."
                )
                logger.error(e)
                return
        else:
            await ctx.send("This is not a modmail thread and you have not mentioned anyone.")

async def setup(bot):
    await bot.add_cog(ModerationPlugin(bot))
