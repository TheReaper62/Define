import typing

import discord
from discord.ext import commands

class Dropdown(discord.ui.Select):
    def __init__(self,raw_options,placeholder=None):

        # Set the options that will be presented inside the dropdown
        options = [discord.SelectOption(**i) for i in raw_options]

        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(
            placeholder=placeholder,
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's favourite colour or choice. The self object refers to the
        # Select object, and the values attribute gets a list of the user's
        # selected options. We only want the first one.
        await interaction.response.send_message(
            f"Your favourite colour is {self.values[0]}"
        )

class DropdownView(discord.ui.View):
    def __init__(self,dropdown_class):
        super().__init__()

        # Adds the dropdown to our view object.
        self.add_item(dropdown_class)

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or("$"))

    async def on_ready(self):
        print(f"Logged in as {self.user} (ID: {self.user.id})")
        print("------")

bot = Bot()
@bot.command()
async def colour(ctx):
    view = DropdownView(Dropdown([
        {
            "label" : "7155 | 1.1.2",
        },
        {
            "label" : "2273 | Theme 1",
        }
    ]))
    await ctx.send("Pick your favourite colour:", view=view)


bot.run("ODA5NDQxNzYxNzMwNDk0NTM0.YCVJYg.N45h21g7rXlI05HNq5v-Nqrmk04")
