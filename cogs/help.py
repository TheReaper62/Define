import discord
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self,client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def help(self,ctx):
        embed = discord.Embed(
          title = "Help Menu",
          description = "*New here?* __Read the Instructions__ and set up your account in under **__30 Seconds__!!!**",
          colour = discord.Colour.green()
        )
        placeholder =  '''
        1) Create an account by doing `def profile`
        2) Get your relevant subject roles by doing `def roles`
        3) To Remove Roles, do `def rroles`
        4) Now you can start doing questions!!!
        *Follow the Steps below*
        '''
        embed.add_field(name = "**__Setting Up a NEW Account__**",value = placeholder,inline=False)
        placeholder = '''
        You can do a question by doing `def`.
        Type your awnser normally to respond.
        There is a 60 Seconds Timeout.

        If you want to do a specific topic you can:
        **EITHER**
        Remove the other roles temporarily
        **OR**
        Do `def-subject name`
        Example
        `def-computing`

        After finshing the question you may choose to, generate another question by pressing the thumbs up reaction instead of typing `def` again.
        '''
        embed.add_field(name = "**__Doing Questions__**",value = placeholder,inline=False)
        placeholder = '''
        Challenges allow you to compete with other players REAL TIME, be the first to answer the question amongst your friends.
        Challenges require minimally 2 Players to Start. Anyone can start by doing `def challenge`
        Add a thumbs up Reaction to join.
        The bot will proceed to ask a Question based on the roles the creator of the challenge has.
        Instead of Typing it in the chat (where everyone can see your answer and copy), you will need to DM the bot.
        A DM is a direct message or private message, yes the bot can see. If there's a active challenge the bot will reply to your answer with the message 'Response Received'
        That message means you have successfully responded to the question. THe bot will proceed to evaluate your answer after the 30 Seconds TImer Ends.

        Apart from that, do not join more than 1 challenge at a time. This will result in you getting both questions immediately wrong (99.9%).
        '''
        embed.add_field(name = "**Challenges**",value=placeholder)
        embed.set_author(name = "Fishball_Noodles#7209")
        embed.set_footer(text='You may contact Fishball_Noodles#7209 if any problems arises')
        await self.ctx.send(embed=embed)

    @help.error
    async def command_error(ctx, error):
        if isinstance(error, dc.CommandOnCooldown):
            em = discord.Embed(title=f"Slow it down !",description=f"Try again in {error.retry_after:.2f}s.", color=discord.Colour.red())
            await ctx.send(embed=em)
def setup(client):
    client.add_cog(Help(client))
