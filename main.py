from dotenv import dotenv_values

from interactions import OptionType, slash_option, slash_command, SlashContext, Embed, SlashCommandChoice
import interactions

from interactions import Client, Intents, listen


import asyncio

import random

import sqlite3

bot = Client(intents=Intents.DEFAULT)
TOKEN = dotenv_values(".env")["TOKEN"]
bot = interactions.Client(token=TOKEN)

con = sqlite3.connect("reports.db")

cur = con.cursor()

@slash_command(name="report", description="Report a user/link/profile on a social-network")
@slash_option(
    name="link",
    description="Link to the user profile",
    required=True,
    opt_type=OptionType.STRING
)
@slash_option(
    name="why",
    description="Why did you report this profile ?",
    required=True,
    opt_type=OptionType.STRING
)
async def report(ctx: SlashContext, link, why):
    embed = Embed(
        title="Report",
        description=ctx.locale+" "+link+" "+why,
        color=0xff0000 # RED color
    )
    await ctx.send(embed=embed)

bot.start()