from discord.ext import commands
import discord
import asyncio
import logging

logger = logging.getLogger("Modmail")

from core import checks
from core.models import PermissionLevel

class StickyMessage(commands.Cog):
    """
    Set up a sticky message. Can only handle one sticky in one channel.
    """

    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.plugin_db.get_partition(self)

        print('StickyMessage v1.0.0')

    @commands.Cog.listener()
    async def on_message(self, msg):
        config = await self.db.find_one({"_id": "smconfig"})

        if config is None:
            return

        # If message contains the exact saved message, ignore it
        if msg.content == f'{config["message"]}':
            return

        sticky_channel = await self.bot.fetch_channel(int(config["channel"]))

        logger.debug(config["last_msg_id"] + 'foobar')

        if msg.channel.id == sticky_channel.id and msg.id != int(config["last_msg_id"]):
            try:
                msg_to_delete = await msg.channel.fetch_message(int(config["last_msg_id"]))
                await msg_to_delete.delete()
            except Exception as e:
                logger.error(e)
                pass

            last_msg = await msg.channel.send(config["message"])
            await self.db.find_one_and_update({"_id": "smconfig"}, {"$set": {"last_msg_id": last_msg.id}}, upsert=True)

    @commands.command(aliases=["sm"])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def sticky(self, ctx: commands.Context, channel: discord.TextChannel, message: str):
        """
        Set the sticky message.
        """

        await self.db.find_one_and_update({"_id": "smconfig"}, {"$set": {"channel": channel.id}}, upsert=True)
        await self.db.find_one_and_update({"_id": "smconfig"}, {"$set": {"message": message}}, upsert=True)
        await self.db.find_one_and_update({"_id": "smconfig"}, {"$set": {"last_msg_id": 1405362911827722283}}, upsert=True)

        await ctx.send("Sticky message set!")

    @commands.command(aliases=["unset"])
    @checks.has_permissions(PermissionLevel.MODERATOR)
    async def unsticky(self, ctx: commands.Context):
        """
        Unset the sticky message.
        """

        await self.db.find_one_and_update({"_id": "smconfig"}, {"$set": {"channel": "123"}})

        await ctx.send('Sticky message unset.')

async def setup(bot):
    await bot.add_cog(StickyMessage(bot))
