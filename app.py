import os
import requests, time

import discord

client = discord.Client()
# BASE_URL = "https://datacordapp.herokuapp.com"
# BASE_URL = "http://127.0.0.1:5000/"
BASE_URL = "http://datacord.vercel.app"

def attempt_connection():
    auth_params = {"name": "Define_Client", "intent": "DefineApp/Database"}
    r = requests.post(BASE_URL+"/auth", json=auth_params)
    if r.ok:
        connection_key = {"identifier": r.json()["success"]}
        return connection_key
    else:
        print(r.text)
        
DB_KEY = attempt_connection()

def get_user(userid):
    while True:
        try:
            value = requests.get(BASE_URL+"/get", headers=DB_KEY,json={"method": "value", "query": str(userid)})
            value = value.json()["content"]
            break
        except KeyError:
            print("Trying Again")
            continue
    return value


def user_exist(userid):
    while True:
        try:
            value = requests.get(BASE_URL+"/get", headers=DB_KEY,json={"method": "keys", "query": ''})
            value = value.json()["content"]
            break
        except KeyError:
            print("Trying Again")
            continue
    value = [i.replace('"',"") for i in value]
    print("List",value)
    return str(userid) in value

def get_def(word):
    start = time.time()
    API_URL = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    r = requests.get(API_URL)
    raw = r.json()[0]
    print(raw)
    dura = time.time()-start
    data = {
        "dura" : dura,
        "phonetic": raw['phonetic'],
        "phonetic_audio": raw['phonetics'][0]['audio'][2:],
        'definitions': [
            {
                'speech_part' : var['partOfSpeech'],
                'meaning' : var['definitions'][0]['definition'],
                'example': var['definitions'][0]['example'],
                'synonyms': var['definitions'][0]['synonyms'][:4]
            } for var in raw["meanings"]
        ]
    }
    return data
        
@client.event
async def on_ready():
    print("Client Ready!!!")


@client.event
async def on_message(message):
    if message.content.startswith("def "):
        if message.content.endswith("review"):
            if not user_exist(message.author.id):
                return
            data = get_user(message.author.id)
            embed = discord.Embed(
                title = f"{message.author.name}'s Profile",
                colour = discord.Colour.random()
            ).set_footer(text=f'User ID: {message.author.id}')

            place = []
            count = 0
            for i in data['history']:
                if len(embed)>5800:
                    return
                embed.add_field(
                    name=f"~\n**{i.title()}**",
                    value=f"Last Searched on <t:{data['history'][i]['last']}>\nSearched **{data['history'][i]['rep']}** time(s)",
                    inline = False
                )

            
            await message.channel.send(embed=embed)
    else:
        if "<@809441761730494534>" in message.content:
            embed = discord.Embed(
                title="Hi I'm Define",
                description="I only work in DMs. Send me a work and I will give you the definition.",
                colour=discord.Colour.teal()
            ).set_footer(text=f"Requested by {message.author}")
            await message.channel.send(embed=embed)
        if message.guild == None:
            if len(message.content.split()) != 1:
                return
            else:
                data = get_def(message.content)
                if data == None:
                    embed=discord.Embed(title="Word Not Found",colour=discord.Colour.red())
                else:
                    embed = discord.Embed(
                        title=f"Definition for {message.content.title()}",
                        description = f"Phonetic: [{data['phonetic']}]({data['phonetic_audio']})",
                        colour = discord.Colour.teal()
                    ).set_footer(text=f"Generated in {round(data['dura'],4)} seconds")
                    for i in data["definitions"]:
                        embed.add_field(name=f"----------\n{i['speech_part']}",value=f"Meaning: **{i['meaning']}**\n**Example**: *{i['example']}*\nSynonyms: {' | '.join([f'`{n}`' for n in i['synonyms']])}")
                    if user_exist(message.author.id):
                        data = get_user(message.author.id)
                    else:
                        data = {'joined':int(time.time()),'history':{}}
                    if message.content.lower() in data['history']:
                        rep = data['history'][message.content.lower()]['rep']+1
                    else:
                        rep = 1
                    
                    data['history'][message.content.lower()] = {
                        'last' : int(time.time()),
                        'rep' : rep
                    }
                    requests.patch(BASE_URL+"/change", headers=DB_KEY,json={"query": str(message.author.id), "data" : data})
    
                    
                await message.channel.send(embed=embed)

client.run(os.getenv('token'))
