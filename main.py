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

@listen()
async def on_ready():
    print("The bot is now running")
    print(f"This bot is owned by {bot.owner}")

@slash_command(name="report", description="Report a user/link/profile on a social-network")
@slash_option(
    name="link",
    description="Link to the user profile",
    required=True,
    opt_type=OptionType.STRING
)
@slash_option(
    name="source",
    description="Source link to justify your report. Could contains slurs",
    required=True,
    opt_type=OptionType.STRING
)
@slash_option(
    name="why",
    description="Why did you report this profile ?",
    required=False,
    opt_type=OptionType.STRING
)
@slash_option(
    name="pseudo",
    description="Pseudonyme to report",
    required=False,
    opt_type=OptionType.STRING
)
async def report(ctx: SlashContext, link, source, why="", pseudo=""):
    await ctx.send("Adding this user to the report database. Please wait\nhttps://tenor.com/view/m%C3%A9lenchon-bg-jlm-m%C3%A9lanchon-pr%C3%A9sidentielles-gif-23207938", ephemeral=True)
    url = source
    wayback = waybackpy.Url(url)
    archive_url = wayback.save()

    data = [
        link,
        source,
        str(archive_url),
        why,
        pseudo,
        ctx.author.id
    ]
    print(data)

    # ctx.locale

    cur = con.cursor()
    cur.execute("INSERT INTO reports (user_link, source_link, archive_link, description, Pseudo, userID) VALUES(?, ?, ?, ?, ?, ?)", data)
    con.commit()

    embed = Embed(
        title="Your report was added",
        description="link : "+link+"\nDescription : \n"+why,
        color=0xff0000
    )
    await ctx.send(embed=embed)

bot.start()