from discord.ext import commands
import discord
import asyncio

class StickyMessage(commands.Cog):
    """
    Set up a sticky message. Can only handle one sticky in one channel.
    """
    last_msg_id = None

    def __init__(self, bot):
        self.bot = bot
        self.db = self.bot.plugin_db.get_partition(self)

        print('StickyMessage v1.0.0')

    @commands.Cog.listener()
    async def on_message(self, msg):
        config = await self.db.find_one({"_id": "smconfig"})
        print(config)
        sticky_channel = await self.bot.fetch_channel(int(config["channel"]))

        if msg.channel.id == sticky_channel.id and msg.id not last_msg_id:
            last_msg = await msg.channel.send(config["message"])
            last_msg_id = last_msg.id

    @commands.command(aliases=["sm"])
    async def sticky(self, ctx: commands.Context, channel: discord.TextChannel, message: str):
        """
        Set the sticky message.
        """

        await self.db.find_one_and_update({"_id": "smconfig"}, {"$set": {"channel": channel.id}}, upsert=True)
        await self.db.find_one_and_update({"_id": "smconfig"}, {"$set": {"message": message}}, upsert=True)

        await ctx.send("Sticky message set!")

    @commands.command(aliases=["unset"])
    async def unsticky(self, ctx: commands.Context):
        """
        Unset the sticky message.
        """

        await self.db.find_one_and_update({"_id": "smconfig"}, {"$set": {"channel": "123"}})

        await ctx.send('Sticky message unset.')

async def setup(bot):
    await bot.add_cog(StickyMessage(bot))
