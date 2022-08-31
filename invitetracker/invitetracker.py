from discord.ext import commands
import discord
import asyncio

class InviteTracker(commands.Cog):
    invites = {}
    tracked_invites = {}
    
    def __init__(self, bot):
        self.bot = bot
        print('v1.0.0')
        
        for guild in bot.guilds:
            # Adding each guild's invites to our dict
            invites[guild.id] = await guild.invites()

    @commands.Cog.listener()
    async def on_member_join(self, member):
        invites_before_join = invites[member.guild.id]
        invites_after_join = await member.guild.invites()
    
        # Loops for each invite we have for the guild
        # the user joined.
        for invite in invites_before_join:
            # Now, we're using the function we created just
            # before to check which invite count is bigger
            # than it was before the user joined.
            
            if invite.uses < find_invite_by_code(invites_after_join, invite.code).uses:
                tracked_invites[member.id] = {
                    'code': invite.code,
                    'inviter': invite.inviter,
                    'uses': invite.uses
                }
                
                # Update the cache
                invites[member.guild.id] = invites_after_join
                
                return

    @commands.Cog.listener()
    async def on_thread_ready(self, thread, creator, category, initial_message):
        user_id = thread.channel.topic.split(': ')[1]
        invite_used = tracked_invites[user_id]
        
        msg = f'Invite used: `{invite_used.code}`. Used {invite_used.uses} times and created by {str(invite_used.inviter)}.'

    @commands.command()
    async def listinvites(self, ctx, *, message):
        """
        List this server's invites and uses.
        """
        
        desc = '**Invites**'
        
        for guildId in invites:
            if guildId == '173554823633829888':
                desc += '\n Real Madrid'
            else:
                desc += f'\n{guildId}'
                
            for invite in invites[guildId]:
                desc += f'\n- `{invite.code}` {invite.uses} uses, created by {str(invite.inviter)}'
        
        await ctx.send(desc)

    def find_invite_by_code(invite_list, code):
        # Simply looping through each invite in an
        # invite list which we will get using guild.invites()
        
        for inv in invite_list:
            # Check if the invite code in this element
            # of the list is the one we're looking for
            
            if inv.code == code:
                # If it is, we return it.
                return inv

def setup(bot):
    bot.add_cog(AutoSub(bot))
