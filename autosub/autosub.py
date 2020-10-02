from discord.ext import commands
import discord
import time
from threading import Timer

class AutoSub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def checkMessages(channel, role_id):
        messages = await channel.history().flatten()
        print('Messages: ', messages)
        first_msg = messages[0]
        ctx = await self.bot.get_context(first_msg)
        await ctx.invoke(self.bot.get_command(f'sub <@&{role_id}>'))
        
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        # category_id = 719324997461606455 # RMJ
        category_id = 761620853824815175 # Delpha's
        role_id = 729298666296180746 # foo
        # role_id = 719980372980531201 # RMJ Managers
        
        # Sub if it's in the MODMAIL Category
        if channel.category.id == category_id:
       
            timer = Timer(2.0, checkMessages, args=channel,role_id)
            timer.start()
        else:
            print('Wrong category')
            print(channel.category.name)

    @commands.command()
    async def say(self, ctx, *, message):
        await ctx.send(message)

def setup(bot):
    bot.add_cog(AutoSub(bot))
