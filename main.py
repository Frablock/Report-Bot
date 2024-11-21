from dotenv import dotenv_values

from interactions import OptionType, slash_option, slash_command, SlashContext, Embed, SlashCommandChoice, BaseContext, Permissions, slash_default_member_permission

from interactions import Client, Intents, listen


import asyncio

import random

import sqlite3

import waybackpy

import csv


TOKEN = dotenv_values(".env")["TOKEN"]
bot = Client(token=TOKEN)

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
    name="pseudo",
    description="Pseudonyme to report",
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
    name="platform",
    description="Platform of the report",
    required=False,
    opt_type=OptionType.STRING
)
async def report(ctx: SlashContext, link, source, pseudo, why="", platform=""):
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
        platform,
        ctx.author.id
    ]
    print(data)

    # ctx.locale

    cur = con.cursor()
    cur.execute("INSERT INTO reports (user_link, source_link, archive_link, description, Pseudo, platform, userID) VALUES(?, ?, ?, ?, ?, ?, ?)", data)
    con.commit()

    embed = Embed(
        title="Your report was added",
        description="link : "+link+"\nDescription : \n"+why,
        color=0xff0000
    )
    await ctx.send(embed=embed)

@slash_command(name="export", description="Export all data")
@slash_default_member_permission(Permissions.MANAGE_EVENTS | Permissions.MANAGE_THREADS)
async def export(ctx: SlashContext):
    #if ctx.author.guild_permissions.administrator:
        cur = con.cursor()
        cur.execute("SELECT * FROM reports")
        data = cur.fetchall()

        with open('reports.csv', 'w', newline='') as f:
            writer = csv.writer(f, delimiter=";")

            for row in data:
                writer.writerow(row)

        await ctx.send("Here is all the data that was saved in the database",files=["./reports.csv"])
    #else:
        #await ctx.send("You do not have permission to use this command.")

@slash_command(name="getprofileinfo", description="Get information about a user")
@slash_option(
    name="pseudo",
    description="Pseudonyme to search for",
    required=True,
    opt_type=OptionType.STRING
)
async def getprofileinfo(ctx: SlashContext, pseudo):
    cur = con.cursor()
    cur.execute("SELECT * FROM reports WHERE Pseudo = ?", (pseudo))
    data = cur.fetchall()

    await ctx.send("Here is all the report that concern the provided user")
    for d in data:
        await ctx.send("> Raison : "+str(d["description"])+"\n> Post problématique : [Post original](<"+str(d["source_link"])+">)  [Lien archive.org](<"+str(d["archive_link"])+">)\n> Statut : à implémenter")



bot.start()