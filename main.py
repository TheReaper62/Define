if __name__ == "__main__": #Import Modules
  print("Importing Modules")
  import random,discord,os,asyncio,time,datetime,bs4,requests,json,gspread,pytz,re,string,ast,statistics
  from oauth2client.service_account import ServiceAccountCredentials as sac
  from urllib.request import Request,urlopen
  import urllib.error
  from discord.ext import commands
  from prettytable import PrettyTable
  from datacord import *

  print("Importing Extra Stuff")
  import constant_ping
  from auth import sudo
  from evaluate import *
#Global Variables & Functions
print("Defining & Setting Up Global Variables")
#client = commands.AutoShardedBot(shard_count=10, command_prefix="def ")

CHALLENGE_DETAILS = {}
CHALLENGE_RESPONSE = {}

intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix="def ",intents=intents)
bot_dump = client.fetch_channel(817575042236940318)
client.remove_command('help')

def is_admin():
    async def predicate(ctx):
        return ctx.author.id == 591107669180284928
    return commands.check(predicate)
print("is_admin function Defined")

def is_moderator():
    async def predicate(ctx):
        return ctx.author.id in os.getenv("QUIZ_MODERATORS")
    return commands.check(predicate)
print("is_moderator function Defined")

async def change_p():
    await client.wait_until_ready()
    statuses = [f"{len(client.guilds)} Servers","def help","Always Defined"]
    while not client.is_closed():
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=random.choice(statuses)))
        await asyncio.sleep(5)
print("change_p function Defined")

async def list_bday():
    await client.wait_until_ready()
    channel = client.get_channel(841216084359118868)
    await channel.purge(limit=100)
    x,spreadfile = await connect_spreadsheet("1CFViEMEGkuhBz8ylhgpo6NoRi-QG94p3X8jmAduuaB8")
    values = spreadfile.sheet1.get_all_values()

    focus = None

    for i in values[1:]:
        now = datetime.datetime.now()
        cur_bday = datetime.datetime.strptime(f"{i[1]} {now.strftime('%Y')}", '%d %B %Y')
        if cur_bday>(now+datetime.timedelta(days=14)):
            colour = discord.Colour.green()
        elif cur_bday>now:
            colour = discord.Colour.orange()
        else:
            colour = discord.Colour.red()
        embed = discord.Embed(
            title = f"{i[0]} Birthday!!!",
            description = f"**Date:** {i[1]}",
            colour = colour
        )
        embed.add_field(name="**Relations**",value="\n".join(i[2].split(",")))
        if i[3]!="":
            embed.add_field(name = "**Contact Number**",value=f"`{i[3]}`",inline=False)
        msg = await channel.send(embed=embed)
        if cur_bday > now and focus == None:
                focus = msg.jump_url
    await channel.send(embed=discord.Embed(title = "Legend",description=f"Red => Past\nOrange => Within the Next 2 Weeks\nGreen => Long Way Ahead\n**[Upcoming Birthday]({focus})**",colour=discord.Colour.gold()))
print("list_bday function defined")

async def connect_spreadsheet(sheet_identifier="",method="key"):
  try:
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/drive'
    ]
    sudo("key.json")
    creds = sac.from_json_keyfile_name("key.json", scope)
    google_client = gspread.authorize(creds)
    os.remove("key.json")
    print(f"Connection Successful!!!\n{sheet_identifier}")

    if sheet_identifier != "":

        if method == "name":
            spreadfile = google_client.open_by_key(FromFileSystem("spreadsheet_links")[sheet_identifier])
        elif method == "key":
            spreadfile = google_client.open_by_key(sheet_identifier)
        #print(f"Spreadfile: {spreadfile}")
        details = None
        try:
            details = spreadfile.worksheet("Details")
        except:
            print("Type Not Quiz")
        return details,spreadfile
  except Exception as exception:
        phr = f"An Exception Occured:\n{exception}\nException Details:\n"
        for i in exception.args:
            phr+=f"{i}\n"
        chan = client.get_channel(695118970986168363)
        await chan.send(phr)
        raise exception

async def generate_question(message,subject="Random",challenge=False):
    async with message.channel.typing():
        try:
            avail_roles = os.getenv("avail_roles").split(",")
            if subject == "Random" or (subject.lower() == "ignore" and message.author.id==591107669180284928):
                try:
                    target_subject = random.choice(FromDatabase(message.author.id)["roles"].split('|'))
                except IndexError:
                    await message.channel.send("You have no roles!!!")
                    return
            elif subject.title() in avail_roles:
                target_subject = subject.title()
            details,sheet = await connect_spreadsheet(FromFileSystem("spreadsheet_links")[target_subject]["link_id"],method = "key")
            details = details.get_all_values().copy()
            no_qn = int(Acell(details,"B2"))
            if no_qn==0:
                await message.channel.send(embed=discord.Embed(
                    title = "No Questions",
                    description = "The developer has not set any questions for this subject yet.\n*Contact @Fishball_Noodles#7209 to contribute questions*",
                    colour = discord.Colour.red()))
                return
        except Exception as e:
            await bot_dump.send(e)
            await message.channel.send(f"Today's test is `{target_subject}`\n`{no_qn}`**Questions** __Found__", delete_after=3)

        ##Check Spreadsheet
        if False:
            raw_integrity = Acell(details,"D2")
            integrity = False
            for i in FromFileSystem("spreadsheet_links"):
                if FromFileSystem("spreadsheet_links")[i]["integrity"] == raw_integrity:
                    integrity = True
                    break
            if integrity == False:
                await message.channel.send(f"__Spreadsheet__ **Corrupted/Faulty**\nSubject: `{target_subject}`\t\tSubject ID: `{avail_roles.index(target_subject)+1}`")
        ###

        qns = sheet.worksheet("Questions").get_all_values().copy()
        question_index = random.randint(2,1+no_qn)
        question_show = Acell(qns,f"A{question_index}")
        self_question =question_show.split('\n')[0]
        gay = await message.channel.send(f"the Question is {self_question}",tts=True)

        ## Question Templating => Format
        question_show = question_show.replace('?~',"What is ")
        question_show = question_show.replace('?/',"What does ")
        if '?/' in question_show:
            question_show+=" mean?"
        ##
    #End Async ctx.typing()

    question_embed = discord.Embed(
    title = f"Subject: `{target_subject}`",
    description = f"**{question_show}**\n__*You have 30 Seconds to Answer*__",
    colour = discord.Colour.random()
    )
    prompt = await message.channel.send(embed = question_embed)

    #Get Headers - Future

    headers_list = list(map(lambda l:l[0],qns))
    #for i in headers_list:
    #if#
    ###

    model_awnser = str(Acell(qns,f"B{question_index}"))
    model_keywords = str(Acell(qns,f"C{question_index}"))
    if model_keywords == "":
        model_keywords = empty_model_keywords_response(model_awnser)
    banned_words = str(Acell(qns,f"D{question_index}"))
    ###

    #Input for Single Player
    if challenge==False:
        response = ""
        try:
            response = await client.wait_for('message',check=lambda m:m.author==message.author,timeout=60)
        except asyncio.exceptions.TimeoutError:
            await message.channel.send("**Time's Up!!!**")
            return
        score = give_score(
            response = response.content.lower(),
            model_awnser = model_awnser,
            model_keywords = model_keywords,
            banned_words = banned_words
            )
    #End input

    #Input for challenge
    else:
        #Inpt is from on_message

        #Post answering status
        async def get_answering_stats(challenge,answered):
            phr = ""
            ans,total = 0,len(CHALLENGE_DETAILS[challenge]["players"])
            for i in CHALLENGE_DETAILS[challenge]["players"]:
                await client.wait_until_ready()
                username = await client.fetch_user(int(i))
                if i in answered:
                    phr+=f"{username} :white_check_mark:\n"
                    ans+=1
                else:
                    phr+=f"{username} :red_circle:\n"
            print("return")
            print(phr,ans,total)
            return phr,ans,total

        answered = []
        challenge = str(challenge)

        phr,ans,total = await get_answering_stats(challenge,answered)
        await prompt.edit(embed=question_embed)
        # DEBUG: await message.channel.send(f"Challenege Details: {CHALLENGE_DETAILS}\nPointer: {CHALLENGE_DETAILS[challenge]}")

        log_chan = client.get_channel(835542115982639176)
        print("No. Of Players>>>",len(CHALLENGE_DETAILS[challenge]['players']))
        print(CHALLENGE_DETAILS[challenge]['players'])
        list_of_players = ("List of Players>>>","\n".join(map(lambda u:client.get_user(u).name,CHALLENGE_DETAILS[challenge]['players'])))
        await log_chan.send(embed=discord.Embed(
        title = f"Creator: {client.get_user(CHALLENGE_DETAILS[challenge]['creator']).name} `{CHALLENGE_DETAILS[challenge]['creator']}`\nTime: {get_sg_time()}\nServer: {message.guild}|Channel: {message.channel}",
        description = f"{len(CHALLENGE_DETAILS[challenge]['players'])} Players: {list_of_players}"
        ))

        countdown_timer_embed = discord.Embed(title=f"Countdown Timer Starting",colour=discord.Colour.gold())
        countdown_timer = await message.channel.send(embed=countdown_timer_embed)
        for x in range(30):
            if x<10:
                colour = discord.Colour(0x00ff6e)
            elif x<20:
                colour = discord.Colour(0xffa600)
            else:
                colour = discord.Colour(0xff2200)
            countdown_timer_embed = discord.Embed(title=f"Time Left {30-x} Seconds",colour=colour)

            await countdown_timer.edit(embed=countdown_timer_embed)
            await asyncio.sleep(1)
        countdown_timer_embed = discord.Embed(title=f"Time's Up!!!",colour=discord.Colour.random())
        await countdown_timer.edit(embed=countdown_timer_embed,delete_after=2)

        # DEBUG: await message.channel.send(f"Challenge Responses: {CHALLENGE_RESPONSE}")
        respond_count = 0
        local_responses = {}
        #Local Response: author_id=>content
        for i in CHALLENGE_RESPONSE:
            if i in CHALLENGE_DETAILS[challenge]["players"]:
                local_responses[i] = CHALLENGE_RESPONSE[i]
                respond_count+=1
        if respond_count==0:
            question_embed.add_field(name=f"**{ans}** out of **{total}** Players have answered",value="Yes literally No one Answered...Bruh")
        else:
            phr,ans,total = await get_answering_stats(challenge,local_responses.keys())
            question_embed.add_field(name=f"**{ans}** out of **{total}** Players have answered",value=phr)
        await prompt.edit(embed=question_embed)

        print("Evaluating...")
        local_scores = {}
        # local_scores: authorid=>score
        ###Evaluation
        for i in local_responses:
            print(f"Evaluating for {i}")
            score = give_score(
                response = local_responses[i].lower(),
                model_awnser = model_awnser,
                model_keywords = model_keywords,
                banned_words = banned_words
            )
            local_scores[i] = score
        print("Evalua Finsihed>>",local_scores)

    ##End Input
    def return_embed(author,correctness_colour,model_awnser,response,score,encouragement,hide="**"):
        if hide == "challenge":
            hide = "**"
            actual_hide = "challenge"
        actual_hide = ""
        embed=discord.Embed(colour = correctness_colour,
        title = f"Answer Review | `{author}`",
        description = f"Model Answer: {hide}{model_awnser.strip()}{hide}")
        embed.add_field(name = "*Your* __Answer__",value=response,inline=False)
        if actual_hide=="challenge":
            embed.add_field(name = "**Your Score**",value = f"{score}%")
        else:
            embed.add_field(name = "**Your Score**",value = f"{score}%\n\n**React For Next Question**")
        embed.add_field(name = f"**{encouragement}**",value = "Try the Next Question!!!")
        try:
            return embed
        except:
            print("Asyncio.Timeout.Error")

    async def return_evaluation(message,score,model_awnser,response,challenge=False):
        correct_encouragement = ["Good Job!!!","Well Done!!!","Nice One!!!"]
        wrong_encouragement = ["Hmmmm Now you know...","That was close?","There's not limit to how many tries"]

        if score>=50.0:
            correctness_colour = discord.Colour.green()
            encouragement = random.choice(correct_encouragement)
        else:
            correctness_colour = discord.Colour.red()
            encouragement = random.choice(wrong_encouragement)
        async with message.channel.typing():
            embed=discord.Embed(title="Evaluating Response",colour=discord.Colour.green())
            embed.set_thumbnail(url="https://emoji.gg/assets/emoji/loading.gif")
            await message.channel.send(embed=embed,delete_after=1)
        print("Befor Retun EMbed",challenge)
        if challenge==True:
            embed=return_embed(message.author.name,correctness_colour,model_awnser,response,score,encouragement,hide="challenge")
        elif challenge=="hide":
            embed=return_embed(message.author.name,correctness_colour,model_awnser,response,score,encouragement,hide="||")
        else:
            embed=return_embed(message.author.name,correctness_colour,model_awnser,response,score,encouragement)

        return embed

    print("Challenge Status>>>",challenge)
    if challenge!=False:
        #Send & Clear RESPONSES
        for i in local_responses:
            embed = await return_evaluation(message,local_scores[i],model_awnser,local_responses[i],challenge=True)
            await client.get_user(i).send(embed=embed)
            print("Send Eva and Clear Response for >>",str(i))
            #Logging for challenge
            if subject != "ignore" or message.author.id in FromDatabase("ADMIN"):
                log_chan = client.get_channel(835542115982639176)
                await log_chan.send(embed=discord.Embed(
                title = f"User: {message.author.name} `{message.author.id}`\nTime: {get_sg_time()}\nServer: {message.guild}|Channel: {message.channel}",
                description = f"Subject: {target_subject}\nRaw Question: {question_show}\nResponse: {local_responses[i]}\nScore: {local_scores[i]}"
                ))
            del CHALLENGE_RESPONSE[i]

        #Delete Shit
        await gay.delete()

        #Sort by score
        sorted = []
        pre = 0
        for i in local_scores:
            if local_scores[i]<=pre:
                pre = local_scores[i]
                sorted.append([client.get_user(i).name,local_scores[i]])
            else:
                sorted.insert(0,[client.get_user(i).name,local_scores[i]])
        tab = PrettyTable()
        tab.field_names = ["-------Player-------","-------Score-------"]
        tab.add_rows(sorted)
        desc = str(tab)
        if sorted[0][1] != 0.0:
            commentary = f"Well Done {sorted[0][0]} for being the Fastest and getting the Highest Score!!!"
        else:
            commentary = random.choice(["All you peasants...No one got it right","No one Got it Correct... Was it even that hard?"])
        results = discord.Embed(
            title = f"Quiz Results\nSubject: {target_subject}\t|\t**Ended at**: `{get_sg_time()}`",
            description =  f"**{commentary}**\n**{desc}**",
            colour = discord.Colour.teal()
        )
        print(local_scores)
        scores_raw = list(map(lambda i:local_scores[i],local_scores))
        stats = f'''
            ** Non-Zero : **`{len(scores_raw)-scores_raw.count(0)}`
            ** Absoulute Zero : **`{scores_raw.count(0)}`
            ** Correct : **`{scores_raw.count(100.0)}`
            ** Pass (50%): **`{len(list(filter(lambda i:i>=50.0,scores_raw)))}`
            ** Average : **`{sum(scores_raw)/len(scores_raw)}`
            ** Minimum : **`{min(scores_raw)}`
            ** Maximum : **`{max(scores_raw)}`

            ** Mode : **`{statistics.mode(scores_raw)}`
            ** Median : **`{statistics.median(scores_raw)}`
            ** Inter Quartile Range : **`{iqr(scores_raw)}`
        '''
        #** Standard Deviation : **`{statistics.stdev(scores_raw)}`
        #** Variance : **`{statistics.variance(scores_raw)}`

        results.add_field(name="Game Statistics",value=stats)
        await message.channel.send(embed=results)
    else:
        #Logging
        if subject != "ignore" or message.author.id in FromDatabase("ADMIN"):
            log_chan = client.get_channel(835542115982639176)
            await log_chan.send(embed=discord.Embed(
            title = f"User: {message.author.name} `{message.author.id}`\nTime: {get_sg_time()}\nServer: {message.guild}|Channel: {message.channel}",
            description = f"Subject: {target_subject}\nRaw Question: {question_show}\nResponse: {response.content}\nScore: {score}"
            ))
        embed = await return_evaluation(message,score,model_awnser,response.content)
        msg = await message.channel.send(embed=embed)
        await msg.add_reaction('👍')

        def check(reaction, user):
            return user == message.author and str(reaction.emoji) == '👍'

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=20.0, check=check)
        except asyncio.TimeoutError:
            embed = await return_evaluation(message,score,model_awnser,response.content,challenge="hide")
            await msg.edit(embed=embed)
            await msg.remove_reaction('👍', client.user)

        else:
            await generate_question(message,subject=subject)

# Events
@client.event
async def on_ready():
  #FromDatabase("restarts") = 0

  #await channel.send(f'Bot Up & Waiting for Requests (**{FromDatabase("restarts")}**)')
  print("Bot Online and Waiting for Requests")
  await connect_spreadsheet()

@client.event
async def on_command_error(ctx,error):
  raise error
  await ctx.send(f"`{ctx.message.content[4:]}` was **invoked __incorrectly__**.\n||{error}||")

@client.event
async def on_message(message):
    print(f"{message.guild} | {message.author.name}")
    if message.guild is None and message.author != client.user:
        print("received DM")
        if len(CHALLENGE_DETAILS) == 0:
            bot_dms = client.get_channel(842676492084576276)
            embed = discord.Embed(
            title = 'Bot has recieved a DM',
            description = f"From: {message.author}",
            colour = discord.Colour.dark_theme()
            )
            embed.add_field(name = 'Message Content',value = message.content)
            await bot_dms.send(embed=embed)
        else:
            await message.channel.send(":white_check_mark:Response Received!!!")
            for i in CHALLENGE_DETAILS:
                print("Challenge plaeyrs>>?",CHALLENGE_DETAILS[i]["players"])
                if message.author.id in CHALLENGE_DETAILS[i]["players"]:
                    print("Found SPecific Challenge")
                    CHALLENGE_RESPONSE[message.author.id] = message.content

    elif re.search("^def-|^Def-|^Drf-|^drf-|^D4f-|^d4f-",message.content):
        subject = message.content.split("-")[1]
        await generate_question(message,subject)
    elif message.content in ["def","Def","drf","Drf","d4f","D4f"]:
        await generate_question(message)
    if "<@809441761730494534>" in message.content:
        await message.channel.send("Do `def help`")
    #await help_command(message,command_specific)
    await client.process_commands(message)

@client.event
async def on_guild_join(guild):
  channel = client.get_channel(817575042236940318)
  await channel.send(embed=discord.Embed(
    title = "New Guild Join",
    description = f"**{guild.name}**\nServer Owner: {guild.owner}\nGuild Count: {len(guild.members)}\nJoin Time: {get_sg_time()}"))

# Commands
@client.command()
async def ping(ctx):
  await ctx.send(embed=discord.Embed(
    title=f"Client Latency\n{round(client.latency*1000,2)}ms",
    description = f"Client Shards:\n**Coming Soon!!!**",colour=discord.Colour.green()))

#Help Command changed to Cog
client.load_extension("cogs.help")

@client.command(aliases=["eval"])
async def evaluate(ctx,*,expression):
  try:
    await ctx.send(embed=discord.Embed(title=f"{ctx.author.name}\n\nEvaluation of: `{expression}`\n`{ast.literal_eval(expression=expression)}`",colour=discord.Colour.teal()))
  except:
    await ctx.send(":warning:Invalid Expression!!!")
@evaluate.error
async def mssing_args(ctx,error):
  if isinstance(error,commands.MissingRequiredArgument):
    await ctx.send(embed=discord.Embed(title="Missing arguments",description="Please Enter in a valid Operator",colour=discord.Colour.red()))

@client.command(name = "return")
@is_admin()
async def return_db(ctx,selector=None):
  if selector == None:
    db = ReturnDatabase()
    for i in db:
      await ctx.send(f'{i}\t->\t{db[i]}')
  else:
    embed = discord.Embed(
      title = "Define Database",
      description = f"Selector: **{selector}**",
      colour = discord.Colour.orange()
    )
    embed.set_footer(text = f"Returned at {datetime.datetime.now()}")
    embed.set_author(name = "Fishball_Noodles#7209")
    for i in db[selector]:
      embed.add_field(name =i ,value = db[selector][i])
    await ctx.send(embed=embed)

@client.command(aliases = ["script","sudo"])
@is_admin()
async def run(ctx,*,code):
  if "while True:" in code:
    await ctx.send(embed=discord.Embed(title=":warning: Take Note An Infinite Loop will not produce any result",colour=discord.Colour.red()))
  if "input" in code:
    await ctx.send(embed=discord.Embed(title=":warning: Take Note No inputs will/can be entered in.\nTherefore, no results will be given.",colour=discord.Colour.red()))
  async with ctx.typing():
    place = open("placeholder.py","w")
    place.write(f"from discord.ext import commands\nclient = commands.Bot('def ')\nfrom datacord import *\n{code}\nimport os\nclient.run(os.getenv('bot-token'))")
    place.close()
    import subprocess

    subprocess = subprocess.Popen("python placeholder.py", shell=True, stdout=subprocess.PIPE)
    output, error = subprocess.communicate()
    subprocess_return = output.decode('utf-8')

    embed = discord.Embed(
      title = ctx.author.name,
      description = f"Code Input:\n```{code}```",
      colour = discord.Colour.purple()
    )
    embed.set_footer(text="Another Discord Bot by @Fishball_Noodles#7209")
    embed.add_field(name="Code Output",value=f"```\n{subprocess_return}\n```")
    if error!=None:
      embed.add_field(name = "Error:",value=f"```{error}```")
  await ctx.send(embed=embed)

@client.command(aliases = ['q'])
async def quiz(ctx):
  await generate_question(ctx.message)

@client.command()
@commands.has_permissions(administrator=True)
async def guild(ctx,method,*args):
  try:
    pass
  except:
    pass

@client.command()
async def kattis(ctx,*,task_id=None):
  if task_id==None or len(task_id)>50:
    await ctx.send(embed=discord.Embed(
      title = ":warning: Task Not Found",
      description = "`ERR 404` **Cannot find Task**,Check Spelling",
      colour = discord.Colour.red()
    ))
    return
  else:
    f_task_id = ""
    for i in task_id.lower():
      if i.isspace():
        f_task_id+="+"
      elif i.isalpha() or i.isdigit():
        f_task_id+=i
    itemurl = f"https://open.kattis.com/search?q={f_task_id}"
    req = Request(itemurl, headers={'User-Agent': 'Mozilla/5.0'})
    async with ctx.typing():
      try:
        sauce = urlopen(req).read()
      except urllib.error.URLError:
        await ctx.send(embed=discord.Embed(
          title = ":warning: Task Not Found",
          description = "`ERR 404` **Cannot find Task**,Check Spelling",
          colour = discord.Colour.red()
        ))
        return
      soup = bs4.BeautifulSoup(sauce, features="html.parser")
      try:
        task_name = soup.find("div", {"class": "headline-wrapper"}).text
        picture = "open.kattis.com"+soup.find("div", {"class": "figure"})["src"]
        print(f"Image Link: {picture}")
      except:
        await ctx.send(embed=discord.Embed(
          title = ":warning: Task Not Found",
          description = "`ERR 404` **Cannot find Task**,Check Spelling",
          colour = discord.Colour.red()
        ))
        return
      text = soup.find("div", {"class": "problembody"})
      childs = text.findChildren("p",recursive=True)
      cur_len = 0
      visible = "\n\n**Task Description**\n"
      for i in childs:
        if cur_len<800:
          visible += i.text
          visible += '\n\n'
          cur_len+=len(i.text)
        else:
          visible+=f"[*Click to continue reading*]({itemurl})"
          break

      display = discord.Embed(
        title = f"{task_name.title()}\n||{itemurl}||",
        description = visible,
        type = "rich",
        colour = discord.Colour.green()
      )
      display.set_thumbnail(picture)
      await ctx.send(embed=display)

@client.command()
async def define(ctx,phrase=""):
  response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en_US/{phrase.replace(" ","%20")}')
  model = discord.Embed(
    title = f'**Definition** for `{phrase.replace("%20"," ").title()}`',
    description = f"By Google Dictionary API (Unofficial)\n__Response Code__:`{response.status_code}`",
    colour = discord.Colour.green()
  )
  await ctx.send(response)
  content = json.loads(response.text)[0]["meanings"]
  await ctx.send(content)
  for i in content:
    embed = model
    embed.add_field(name = "Part Of Speech",value = i["partOfSpeech"])
    embed.add_field(name = "Definitions",value = i["definitions"])
    await ctx.send(embed=embed)

@client.command(aliases=["stats", "create","profile","p"])
async def mystatistics(ctx):
  new=False
  author_id = str(ctx.author.id)
  while True:
    await ctx.send("*Finding Player Data...*", delete_after=2)
    try:
        place = FromDatabase(author_id)
        print("Play",type(place),place)
        tokens = place["TrueTokens"]
        roles = place["roles"].split("|")
        prompt = await ctx.send("Player Data Found!!!")
        break
    except KeyError:
      prompt = await ctx.send(
			    f"**Player Data for the name ({ctx.author.name}) Not Found**!!!\n__*Attempting* To Create New Profile__"
			)
      joined_in = pytz.timezone("Asia/Singapore").localize(
			    datetime.datetime.now() +
			    datetime.timedelta(hours=8)).strftime("%c")
      ToDatabase(author_id ,{"name":ctx.author.name,"joined_in": str(joined_in), "roles": "", "TrueTokens":10})
      new=True
    await prompt.delete()
  display = discord.Embed(
	    title=f"Your Profile - {ctx.author.name}",
	    description=
	    f"**Player ID:** `{ctx.author.id}`\n",
	    color=discord.Colour.green())
  display.add_field(name="*Joined In*",value=place["joined_in"],inline=False)
  display.add_field(name="**Your TrueTokens™**", value=tokens)
  if roles!=[""]:
    printable_roles = str(" | ".join(roles))
  else:
    printable_roles = 'No Roles Here'
  print(f"Values to Add: {place['joined_in']} | {tokens} | {printable_roles}")
  display.add_field(name="**Your Roles**", value=printable_roles,inline=False)
  await ctx.send(embed=display)
  if new==True:
    bot_dump = client.get_channel(817575042236940318)
    await bot_dump.send(f"**New User Joined **in {ctx.guild.name}#{ctx.channel.name}",embed=display)

@client.command(aliases = ["roles"])
async def getroles(ctx):
  db = ReturnDatabase()
  print(type(db),db)
  if f"Define-{ctx.author.id}" in db:
    embed=discord.Embed(
      title = "**Currently Available Roles**",
      description = "Key in Subject ID (not Subject name)\n*Input Format: `1 3`*\n> This gives the roles __Computing__ and __Normal Chinese__",
      colour = discord.Colour.teal()
    )
    phrase,counter = "",1
    avail_roles = os.getenv("avail_roles").split(",")
    for i in avail_roles:
      phrase+=f"`{counter}`\t**{i}**\n"
      counter+=1
    embed.add_field(name = "Currently Available Subjects:",value=phrase)
    await ctx.send(embed=embed)
    try:
      response = await client.wait_for("message",check=lambda m:m.author == ctx.author,timeout=60)
    except asyncio.TimeoutError:
      await ctx.send("Ran out of Time, try again.",delete_after=5)
      return
    response = list(map(int,response.content.split()))
    role_print = ""
    no_roles_given = 0
    for i in response:
      print("FromDatabase",type(FromDatabase(ctx.author.id)),FromDatabase(ctx.author.id))
      obj = FromDatabase(ctx.author.id)
      print("This is obj>>",type(obj),obj)
      try:
        avail_roles[i-1]
      except:
        await ctx.send(embed=discord.Embed(title=f"Invalid Subject ID `{i}`",colour=discord.Colour.red()))
        continue
      if avail_roles[i-1].replace('"',"") in obj["roles"]:
        await ctx.send(embed=discord.Embed(title="You already have the role `{}`".format(avail_roles[i-1].replace('"',"")),colour=discord.Colour.red()))
        continue
      else:
        role_print+=f" `{avail_roles[i-1]}`"
        place = obj["roles"].split("|")
        if place == ['']:
            place = []
        print("Place before assign>>",place)
        place.append(avail_roles[i-1].replace('"',""))
        obj["roles"] = "|".join(place)
        ToDatabase(ctx.author.id,str(obj))
        no_roles_given+=1
    if no_roles_given==0:
      return
    await ctx.send(embed=discord.Embed(title=":white_check_mark: Roles Given!!!",description=f'Roles Given:{role_print}',colour=discord.Colour.teal()))
  else:
    await ctx.send(embed=discord.Embed(
      title = ":warning:Account Not Created",
      description = "Do `def create` before trying this command again.",
      colour = discord.Colour.red()))

@client.command(aliases = ["rroles"])
async def removeroles(ctx):
  db = ReturnDatabase()
  print(db)
  if f"Define-{ctx.author.id}" in db:
    embed=discord.Embed(
      title = "**Your Current Roles**",
      description = "Key in Subject ID (not Subject name)\n*Input Format: `1 3`*\n> This gives removes roles __Computing__ and __Normal Chinese__\n*Type `cancel` to exit*",
      colour = discord.Colour.teal()
    )
    phrase,counter = "",1
    avail_roles = FromDatabase(ctx.author.id)["roles"].split("|")
    for i in avail_roles:
      phrase+=f"`{counter}`\t**{i}**\n"
      counter+=1
    if phrase=="":
      phrase=None
    embed.add_field(name = "Your Current Roles:",value=phrase)
    await ctx.send(embed=embed)
    try:
      response = await client.wait_for("message",check=lambda m:m.author == ctx.author,timeout=60)
    except asyncio.TimeoutError:
      await ctx.send("Ran out of Time, try again.",delete_after=5)
      return
    response = list(map(int,response.content.split()))
    role_print = ""
    no_roles_rem = 0
    for i in response:
      obj = FromDatabase(ctx.author.id)
      try:
        avail_roles[i-1]
      except:
        await ctx.send(embed=discord.Embed(title=f"Invalid Subject ID `{i}`",colour=discord.Colour.red()))
        continue
      if avail_roles[i-1].replace('"',"") not in obj["roles"].split("|"):
        await ctx.send(embed=discord.Embed(title=f"You don't have the role `{avail_roles[i-1]}`",colour=discord.Colour.red()))
        continue
      else:
        print("Obj Brfore::",obj)
        role_print+=f" `{avail_roles[i-1]}`"
        place = obj["roles"].split("|")
        print("Removing Role>>>",avail_roles[i-1])
        place.remove(avail_roles[i-1])
        obj["roles"] = "|".join(place)
        print("Obj After::",obj)
        ToDatabase(ctx.author.id,obj)
        no_roles_rem+=1
    if no_roles_rem==0:
      return
    await ctx.send(embed=discord.Embed(title=":white_check_mark: Roles Removes!!!",description=f'Roles Removed:{role_print}',colour=discord.Colour.teal()))
  else:
    await ctx.send(embed=discord.Embed(
      title = ":warning:Account Not Created",
      description = "Do `def create` before trying this command again.",
      colour = discord.Colour.red()))

@client.command()
async def bot_stat(ctx):
  await ctx.send(client.guilds)

@client.command()
async def invite(ctx):
  await ctx.send("You can invite the bot to your server (no requirements) - https://discord.com/api/oauth2/authorize?client_id=809441761730494534&permissions=2148006992&scope=bot")

@client.command()
async def status(ctx):
  await ctx.send(embed=discord.Embed(
    title = 'Status Page',
    description = "https://stats.uptimerobot.com/v94L3CWZ1Q",
    colour = discord.Colour.green()
  ))

@client.command()
async def report(ctx,description=""):
  if description=="":
    embed=discord.Embed(colour=discord.Colour.green(),
    title = "Report Vulnerability|Bug",
    description = "Type in the details of the report\n**Include:** *Command that has a bug*\n*Explain what is expected to happen and what actually happened*")
    await ctx.send(embed=embed)
    description = await client.wait_for('message',check=lambda m:m.author==ctx.author)
    description = description.content
    await embed.delete()
    await bot_dump.send(embed=discord.Embed(
        title = "Bug Report",
        description = f"Username: {ctx.author.name}|{ctx.author.id}\nTime: {get_sg_time()}\n\nReport Description: {description}",
        colour = discord.Colour.orange()
    ))

@client.command(aliases=['sb'])
async def superbroadcast(ctx):
    if ctx.author.id == 591107669180284928:

        def check(message):
            return message.author.id == ctx.author.id

        await ctx.send(
            "Type in What You want to broadcast\n`Type cancel to force end`")
        msg = await client.wait_for('message', check=check)
        if msg.content != "" and msg.content != "cancel":
            for i in client.guilds:
              channel = i.system_channel
              await channel.send(
                        f"**Super Broadcast**\n{msg.content}\n\n*By my creator __@Fishball Noodles__*"
                    )
            await ctx.send("Broadcast Successfully Sent!")
        else:
            await ctx.send("`Super Broadcast Cancelled.`")

@client.command()
@is_admin()
async def talk(ctx,guild_id,*,text):
	guild = None
	for i in client.guilds:
		if i.id == int(guild_id):
			guild = i
			break
	for i in guild.channels:
		if i.name=="general":
			await i.send(text)
	await ctx.send("Message Sent Awaiting Response")
	while True:
		msg=await client.wait_for("message",check= lambda m:m.author!=client.user)
		if msg.author==ctx.author and msg.content=="--END--":
			break
		await ctx.send(f"{msg.author.name}: {msg.content}")

@client.command()
@commands.guild_only()
async def challenge(ctx,subject="Random"):
    for i in CHALLENGE_DETAILS:
        if ctx.author in CHALLENGE_DETAILS[i]["players"]:
            await ctx.send(embed=discord.Embed(
    			title = ":warning:Forbidden",
    			description = f"**Reason**: You are already in another game started by {CHALLENGE_DETAILS[i]['creator']} in {client.get_channel(CHALLENGE_DETAILS[i]).name}.\nWait for that game to end or **Directly message the bot** `leave game`",
    			colour = discord.Colour.red()
    		))
            return
        elif ctx.channel.id == CHALLENGE_DETAILS[i]:
            await ctx.send(embed=discord.Embed(
    			title = ":warning:Forbidden",
    			description = f"**Reason**: There's already another game running here started by {CHALLENGE_DETAILS[i]['creator']} in {client.get_channel(CHALLENGE_DETAILS[i]).name}.",
    			colour = discord.Colour.red()
    		))
            return
    embed=discord.Embed(title="Challenge",colour=discord.Colour.green())
    embed.set_thumbnail(url="https://emoji.gg/assets/emoji/loading.gif")
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('👍')
    starts_in = 5
    for i in range(starts_in,-1,-1):
        await msg.edit(embed=discord.Embed(title="Challenge Starting",
              description = f"Challenge for subject `{subject}` has been started by `{ctx.author.name}`\nReact Below to Join!!!\nTime Left to Join **{i}**",
              colour = discord.Colour.random())
              )
        await asyncio.sleep(1)

    #Get reactions from cached msg
    cache_msg = discord.utils.get(client.cached_messages, id=msg.id)
    n_players = await cache_msg.reactions[0].users().flatten()
    n_players = n_players[1:]

    if len(n_players)>0:
        embed.add_field(name = f"{len(n_players)} Players Joined:",value="\n".join(map(str,n_players))+"\n\n")
        await msg.delete()
        starter = await ctx.send(embed=embed)
    else:
        await ctx.send(embed=discord.Embed(
        title = ":warning:Game Cancelled",
        description = "**Reason**: Not enough players Minimum 2 players",
        colour = discord.Colour.red()
        ))
        return

    	#Add action to global challenges
    players = []
    for i in n_players:
        players.append(i.id)
    CHALLENGE_DETAILS[str(ctx.channel.id)] = {"creator":ctx.author.id,"players":players}
    # DEBUG: await ctx.send(CHALLENGE_DETAILS)
    embed=discord.Embed(title="Starting Game!!!",colour=discord.Colour.green())
    embed.set_thumbnail(url="https://emoji.gg/assets/emoji/loading.gif")
    if subject=="Random":
        subject = random.choice(FromDatabase(ctx.author.id)["roles"].split("|"))
    await generate_question(ctx.message,subject=subject,challenge=ctx.channel.id)


if __name__ == "__main__":
  client.loop.create_task(change_p())
  client.loop.create_task(list_bday())
  constant_ping.keep_alive()
  from dotenv import load_dotenv
  print(load_dotenv())
  client.run(os.getenv("bot-token"))
