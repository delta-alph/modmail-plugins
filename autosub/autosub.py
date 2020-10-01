from discord.ext import commands
import discord

class AutoSub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_create(channel):
      # Sub if it's in the MODMAIL Category
      if channel.category.name == "MODMAIL":
        await ctx.invoke(bot.get_command('sub'), user_or_role=ctx.guild.get_role(719980372980531201))

    @commands.command()
    async def say(self, ctx, *, message):
        await ctx.send(message)

def setup(bot):
    bot.add_cog(AutoSub(bot))
