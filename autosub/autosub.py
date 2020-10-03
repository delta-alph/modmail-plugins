from discord.ext import commands
# from core.thread import Thread
import discord
import asyncio
from pprint import pprint

class AutoSub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('v0.0.060')
        # pprint(vars(self.bot))
        
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        # category_id = 719324997461606455 # RMJ
        category_id = 761620853824815175 # Delpha's
        role_id = 729298666296180746 # foo
        # role_id = 719980372980531201 # RMJ Managers
        
        # Sub if it's in the MODMAIL Category
        if channel.category.id == category_id:
            await asyncio.sleep(5)
            messages = await channel.history().flatten()
            # print('Messages: ', messages)
            first_msg = messages[0]
            # topic = channel.topic
            # recipient_id = str(topic).split(':')[1].strip()
            # print(channel.topic)
            ctx = await self.bot.get_context(first_msg)
            ctx.foo = True
            # thread = Thread(self, int(recipient_id), channel)
            member = await channel.guild.fetch_member(685320437265203252)
            thr = await self.bot.threads.find_or_create(member)
            ctx.thread = thr
            pprint(vars(ctx))
            
            # role = ctx.guild.get_role(role_id)
            # await ctx.invoke(self.bot.get_command('sub'))
            await ctx.invoke(self.bot.get_command('subscribe'), user_or_role=ctx.guild.get_role(role_id))
        else:
            print('Wrong category')
            print(channel.category.name)

    @commands.command()
    async def say(self, ctx, *, message):
        await ctx.send(message)

def setup(bot):
    bot.add_cog(AutoSub(bot))
