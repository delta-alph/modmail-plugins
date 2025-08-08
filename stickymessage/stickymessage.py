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
        sticky_channel = await self.bot.fetch_channel(int(config["channel"]))

        if msg.channel.id == sticky_channel.id:
            await msg.channel.send(config["message"])

    @commands.command(aliases=["sm"])
    async def sticky(self, ctx: Commands.Context, channel: discord.TextChannel, message: str):
        """
        Set the sticky message.
        """

        await self.db.find_one_and_update({"_id": "smconfig"}, {"$set": {"channel": channel.id}})
        await self.db.find_one_and_update({"_id": "smconfig"}, {"$set": {"message": message}})

        await ctx.send("Sticky message set!")

    @commands.command(aliases=["unset"])
    async def unsticky(self, ctx: Commands.Context):
        """
        Unset the sticky message.
        """
        
        await self.db.find_one_and_update({"_id": "smconfig"}, {"$set": {"channel": "123"}})

        await ctx.send('Sticky message unset.')

async def setup(bot):
    await bot.add_cog(InviteTracker(bot))
