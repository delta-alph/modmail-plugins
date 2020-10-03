from discord.ext import commands
import discord
import asyncio

class AutoSub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('v0.0.064')
    
    def find_member(self, name, guild):
        members = guild.fetch_members(limit=None)
        
        for member in members:
            if member.name.lower().startswith(name.lower()):
                return member
                break
        
    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        category_id = 719324997461606455 # RMJ
        # category_id = 761620853824815175 # Delpha's
        # role_id = 729298666296180746 # foo
        role_id = 719980372980531201 # RMJ Managers
        
        # Sub if it's in the MODMAIL Category
        if channel.category.id == category_id:
            await asyncio.sleep(10)
            messages = await channel.history().flatten()
            first_msg = messages[0]
            print(first_msg)
            parts = channel.name.split('-')
            del parts[-1]
            joined = " ".join(parts)
            print(joined)
            
            ctx = await self.bot.get_context(first_msg)
            
            member = self.find_member(joined, channel.guild)
            print("Member: ", member)
            thr = await self.bot.threads.find_or_create(member)
            ctx.thread = thr
            
            await ctx.invoke(self.bot.get_command('subscribe'), user_or_role=ctx.guild.get_role(role_id))
        else:
            print('Wrong category')
            print(channel.category.name)

    @commands.command()
    async def say(self, ctx, *, message):
        await ctx.send(message)

def setup(bot):
    bot.add_cog(AutoSub(bot))
