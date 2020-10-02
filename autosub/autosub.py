from discord.ext import commands
import discord

class AutoSub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    '''@commands.Cog.listener()
    async def on_guild_channel_create(self, ctx: commands.Context, channel):
      # category_id = 719324997461606455 # RMJ
      category_id = 761620853824815175 # Delpha's
      role_id = 729298666296180746 # foo
      # role_id = 719980372980531201 # RMJ Managers
      
      # first_msg = self.bot.get_channel(channel.id).fetch_message(payload.message_id)
      # Sub if it's in the MODMAIL Category
      if channel.category.id == category_id:
        print('It should sub')
        # await self.bot.invoke(self.bot.get_command('sub'), user_or_role=ctx.guild.get_role(role_id))
        await discord.ext.commands.Context.invoke(self.bot.get_command('sub'))
      else:
        print('Wrong category')
        print(channel.category.name)'''
        
    @commands.Cog.listener()
    async def on_message(self, message):
        # category_id = 719324997461606455 # RMJ
        category_id = 761620853824815175 # Delpha's
        role_id = 729298666296180746 # foo
        # role_id = 719980372980531201 # RMJ Managers
        # bot_id = 721779303049724017 # RMJ
        bot_id = 761557209791332373 # Delpha's
        # bot_logs = 719324997461606456 # RMJ
        bot_logs = 761620854601285732 # Delpha's
        
        if message.channel.category.id == category_id && message.author.id == bot_id && message.channel.id != bot_logs:
            message.channel.send('<&' + role_id + '>)
        else:
            print('Wrong channel(s)')

    @commands.command()
    async def say(self, ctx, *, message):
        await ctx.send(message)

def setup(bot):
    bot.add_cog(AutoSub(bot))
