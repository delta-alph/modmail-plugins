from discord.ext import commands
import discord
import asyncio

class DeleteTMZ(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    print('DeleteTMZ v1.0.0')
    
  @commands.Cog.listener()
  async def on_message(self, msg):
    if (msg.content.lower().contains('twitter.com/themadridzone')):
      warn_msg = await msg.channel.send(f'🚫 {msg.author.mention} tweets from The Madrid Zone are banned!')
      
      await msg.delete()
      await warn_msg.delete(delay=5.0)

def setup(bot):
  bot.add_cog(DeleteTMZ(bot))
