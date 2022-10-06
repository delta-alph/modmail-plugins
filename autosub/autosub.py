from discord.ext import commands
import discord
import asyncio

class AutoSub(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print('Autosub v2.1.0')

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        category_id = 719324997461606455 # RMJ
        # category_id = 761620853824815175 # Delpha's
        # role_id = 729298666296180746 # foo
        role_id = 719980372980531201 # RMJ Managers

        # Sub if it's in the MODMAIL Category
        if channel.category.id == category_id:
            await asyncio.sleep(5)
            messages = [message async for message in channel.history()]
            print(messages)
            first_msg = messages[0]
            print('First message: ', first_msg)
            newChannel = self.bot.get_channel(channel.id)
            userID = newChannel.topic.split(': ')[1]
            print('userID:', userID)

            ctx = await self.bot.get_context(first_msg)

            member = self.bot.get_user(int(userID))
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

async def setup(bot):
    await bot.add_cog(AutoSub(bot))
