import discord

import ext

DATA = ext.Handler()

def on_ready_func(client):
    return f"Bot Online, Logged in as {client.user.name}"

def help_cmd(ctx):
    return f"Hi {ctx.author.name}. This bot is under development"

def subjects_cmd(ctx,subject):
    embed = discord.Embed(
        title = f"Subjects that Define will support",
        description = "\n".join([f'`{code}` - **{DATA.supported_subjects_dict[code]}**' for code in DATA.supported_subjects_dict]) + "\n\n**Combined Subjects**\nSince **Combined Humanities** and **Combined Sciences** are a strict subset of its __Pure variation__, content will not be customised for these subjects.\nSyllabus will remain available for each of this subjects\n\nSubjects will be rolled out slowly starting (naturally) with those I have taken",
        colour = discord.Colour.green()
    )
    return embed

def contribute_cmd(ctx):
    embed = discord.Embed(
        title = "About Contribution",
        description = DATA.contribute_message1,
        colour = discord.Colour.teal()
    )
    return embed

def syllabus_overview_cmd(ctx,subject):
    code,name = DATA.fuzzy_search_subject(subject)
    if code == None:
        raise ext.InvalidArguments

    info = eval(f"DATA._{code}_syllabus_overview")

    embed = discord.Embed(
        title = f"**{code} {name}** Syllabus Outline",
        colour = discord.Colour(0xd32ed9)
    )
    for i in info:
        embed.add_field(name=i,value=info[i],inline=False)
    return embed

def legal_cmd(ctx):
    embed = discord.Embed(
        title = "Legal information",
        description = DATA.legal_message1,
        colour = discord.Colour.orange()
    )
    return embed

def periodictable_cmd(ctx,subject):
    if subject == "6092 O Levels":
        img_file = discord.File("images\quickreference\6092 Periodic Table.jpg",filename="table.jpg")
        e = discord.Embed(title="6092 Chemistry Periodic Table")
    elif subject == "9729 A Levels":
        img_file = discord.File("images\quickreference\9729 Periodic Table.jpg",filename="table.jpg")
        e = discord.Embed(title="9729 Chemistry Periodic Table")
    else:
        raise ext.InvalidArguments()
    return e.set_image(url="attachment://table.jpg"), img_file

def formulasheet_cmd(ctx,subject):
    if subject == "4048 Mathematics":
        img_file = discord.File(r"images\quickreference\4048 Formula Sheet.jpg",filename="formula_sheet.jpg")
        e = discord.Embed(title="4048 Mathematics Formula Sheet")
    elif subject == "4049 Additional Mathematics":
        img_file = discord.File(r"images\quickreference\4049 Formula Sheet.jpg",filename="formula_sheet.jpg")
        e = discord.Embed(title="4049 Additonal Mathematics Formula Sheet")
    else:
        raise ext.InvalidArguments()
    return e.set_image(url="attachment://table.jpg"), img_file

def pythonreference_cmd(ctx):
    page_1_file = discord.File(r"images\quickreference\7155 Reference 1.jpg",filename="pythonreference_1.jpg")
    page_2_file = discord.File(r"images\quickreference\7155 Reference 2.jpg",filename="pythonreference_2.jpg")
    page_3_file = discord.File(r"images\quickreference\7155 Reference 3.jpg",filename="pythonreference_3.jpg")
    files = [page_1_file,page_2_file,page_3_file]

    page_1_embed = discord.Embed(title="Python Quick Reference - Page 1")
    page_1_embed.set_footer(text="This document will be provided in ALL GCE O Level 7155 Paper 2 Practical Exam")
    page_1_embed.set_image(url="attachment://pythonreference_1.jpg")

    page_2_embed = discord.Embed(title="Python Quick Reference - Page 2")
    page_2_embed.set_footer(text="This document will be provided in ALL GCE O Level 7155 Paper 2 Practical Exam")
    page_2_embed.set_image(url="attachment://pythonreference_2.jpg")

    page_3_embed = discord.Embed(title="Python Quick Reference - Page 3")
    page_3_embed.set_footer(text="This document will be provided in ALL GCE O Level 7155 Paper 2 Practical Exam")
    page_3_embed.set_image(url="attachment://pythonreference_3.jpg")
    embeds = [page_1_embed,page_2_embed,page_3_embed]
    
    return embeds,files

def assessmentobjectives_cmd(ctx,subject,ao=None):
    if subject == None:
        raise ext.InvalidArguments
    matched,name = DATA.fuzzy_search_subject(subject)
    if matched == None:
        raise ext.InvalidArguments
    if ao == None:
        info = eval(f"DATA._{matched}_ao")
        aos = list(info.keys())
        info = "\n\n".join([f"**AO{i+1} : {aos[i]}**\n{info[aos[i]]}" for i in range(3)])
    elif ao in [1,2,3]:
        info = eval(f"DATA._{matched}_ao")
        info = f"**Assessment Objective {ao}**\n\n **{list(info.keys())[ao-1]}**  \n{info[list(info.keys())[ao-1]]}"
    embed = discord.Embed(
        title = f"Assessment Objectives for {matched} {name}",
        description = info,
        colour = discord.Colour(0x30c762)
    )
    return embed

def topicdetails_cmd(ctx,query):
    subject,sub_topic = query.split(" | ")

    details = DATA.topic_desc[subject][sub_topic]
    details.append({"title":sub_topic})
    details.append({"footer": subject})
    embed,file = ext.Handler.create_embed(details)
    return embed,file
