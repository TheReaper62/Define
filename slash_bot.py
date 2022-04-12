import discord
from discord.commands import Option

from main import *

client = discord.Bot()

@client.event
async def on_ready():
    print(on_ready_func(client))

@client.slash_command(name="help",guilds=DATA.connected_guilds)
async def help_slash(ctx):
    await ctx.respond(help_cmd(ctx))

@client.slash_command(name="subjects",guilds=DATA.connected_guilds)
async def subjects_slash(ctx,subject:Option(str,description="Choose Subject",choices=DATA.supported_subjects_text.split("\n"),required=False, default=None)):
    await ctx.respond(embed=subjects_cmd(ctx,subject))

@client.slash_command(name="contribute",guilds=DATA.connected_guilds)
async def contribute_slash(ctx):
    await ctx.respond(embed=contribute_cmd(ctx))

@client.slash_command(name="syllabus",guilds=DATA.connected_guilds)
async def syllabus_overview_slash(ctx,subject:Option(str,description="Choose Subject",choices=DATA.supported_subjects_text.split("\n"))):
    await ctx.respond(embed=syllabus_overview_cmd(ctx,subject))

@client.slash_command(name="legal",guilds=DATA.connected_guilds)
async def legal_slash(ctx):
    await ctx.respond(embed=legal_cmd(ctx))

@client.slash_command(name="periodictable",guilds=DATA.connected_guilds)
async def periodictable_slash(ctx,subject:Option(str,description="Choose Subject", choices=["6092 O Levels","9729 A Levels"], default="6092 O Levels", required=False)):
    embed, img_file = periodictable_cmd(ctx,subject)
    await ctx.respond(embed=embed, file=img_file)

@client.slash_command(name="formulasheet",guilds=DATA.connected_guilds)
async def formulasheet_slash(ctx,subject:Option(str,description="Choose Subject", choices=["4048 Mathematics[]","4049 Additional Mathematics"], default="4049 Additional Mathematics", required=False)):
    embed, img_file = formulasheet_cmd(ctx,subject)
    await ctx.respond(embed=embed, file=img_file)

@client.slash_command(name="assessmentobjectives",guilds=DATA.connected_guilds)
async def assessmentobjectives_slash(ctx,subject:Option(str,description="Choose Subject", choices=DATA.supported_subjects_text.split("\n")),ao:Option(int,choices=[1,2,3],required=False,default=None)):
    embed = assessmentobjectives_cmd(ctx,subject,ao)
    await ctx.respond(embed=embed)

@client.slash_command(name="criteria",guilds=DATA.connected_guilds)
async def topicsdetails_slash(ctx,query:Option(str,description="Choose a Topic",choices=DATA.all_topics)):
    embed,file = topicdetails_cmd(ctx,query)
    if file == None:
        await ctx.respond(embed=embed)
    else:
        await ctx.respond(embed=embed,file=file)

@client.slash_command(name="pythonreference",guilds=DATA.connected_guilds)
async def pythonreference_slash(ctx):
    embeds, files = pythonreference_cmd(ctx)
    await ext.create_page(client,ctx,embeds,files=files,respond=False)

client.run("ODA5NDQxNzYxNzMwNDk0NTM0.YCVJYg.R3XDMvaZDP_yryZNHJQpYnDrz3c")
