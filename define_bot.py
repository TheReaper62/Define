import os
import discord
import requests, time

client = discord.Client()


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
    print(message.content)
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
            embed = discord.Embed(
                title=f"Definition for {message.content.title()}",
                description = f"Phonetic: [{data['phonetic']}]({data['phonetic_audio']})",
                colour = discord.Colour.teal()
            ).set_footer(text=f"Generated in {round(data['dura'],4)} seconds")
            for i in data["definitions"]:
                embed.add_field(name=f"----------\n{i['speech_part']}",value=f"Meaning: **{i['meaning']}**\n**Example**: *{i['example']}*\nSynonyms: {' | '.join([f'`{n}`' for n in i['synonyms']])}")
            await message.channel.send(embed=embed)

client.run(os.getenv('token'))
