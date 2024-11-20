from dotenv import dotenv_values

from interactions import OptionType, slash_option, slash_command, SlashContext, Embed, SlashCommandChoice
import interactions

from interactions import Client, Intents, listen


import asyncio

import random

import sqlite3

import waybackpy


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
    await ctx.send("Adding this user to the report database. Please wait\nhttps://tenor.com/view/m%C3%A9lenchon-bg-jlm-m%C3%A9lanchon-pr%C3%A9sidentielles-gif-23207938", ephemeral=True)
    url = link
    wayback = waybackpy.Url(url)
    archive_url = wayback.save()

    embed = Embed(
        title="Report",
        description=ctx.locale+" "+link+" "+why+" "+str(archive_url),
        color=0xff0000 # RED color
    )
    await ctx.send(embed=embed)

bot.start()