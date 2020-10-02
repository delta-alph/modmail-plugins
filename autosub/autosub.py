from discord.ext import commands
import discord

class AutoSub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('Plugin print line 7')

    @commands.Cog.listener()
    async def on_guild_channel_create(self, ctx):
      # category_id = 719324997461606455 # RMJ
      category_id = 761620853824815175 # Delpha's
      category = discord.utils.get(self.bot.guild.categories, id=category_id)
      # Sub if it's in the MODMAIL Category
      print('ctx.category.id: ', ctx.category.id)
      print('category_id: ', category_id)
      if ctx.category.id == category_id:
        print('It should sub')
        await self.bot.invoke(bot.get_command('sub'), user_or_role=ctx.guild.get_role(719980372980531201))
      else:
        print('Wrong category')
        print(ctx.category.name)

    @commands.command()
    async def say(self, ctx, *, message):
        await ctx.send(message)

def setup(bot):
    bot.add_cog(AutoSub(bot))
