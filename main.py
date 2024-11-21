from dotenv import dotenv_values

from interactions import Modal, ModalContext, ParagraphText, ShortText, OptionType, slash_option, slash_command, SlashContext, Embed, SlashCommandChoice, BaseContext, Permissions, slash_default_member_permission

from interactions import Client, Intents, listen, AllowedMentions


import asyncio

import random

import sqlite3

import waybackpy

import csv

import re


TOKEN = dotenv_values(".env")["TOKEN"]
bot = Client(token=TOKEN, intents=Intents.DEFAULT | Intents.MESSAGE_CONTENT)

con = sqlite3.connect("reports.db")

@listen()
async def on_ready():
    print("The bot is now running")
    print(f"This bot is owned by {bot.owner}")

@slash_command(name="report", description="Signaler un utilisateur/lien")
async def report(ctx: SlashContext):
    my_modal = Modal(
        ShortText(label="Lien vers le profil", custom_id="link", required=True),
        ShortText(label="Sources", custom_id="source", required=True),
        ShortText(label="Pseudo à signaler", custom_id="pseudo", required=True),
        ShortText(label="Plateforme", custom_id="platform", required=True),
        ParagraphText(label="Pourquoi ?", custom_id="why", required=False),
        title="Signaler un utilisateur",
        custom_id="report_modal",
    )
    await ctx.send_modal(modal=my_modal)
    modal_ctx: ModalContext = await ctx.bot.wait_for_modal(my_modal)

    # Extract the answers from the responses dictionary
    link = modal_ctx.responses["link"]
    source = modal_ctx.responses["source"]
    pseudo = modal_ctx.responses["pseudo"]
    platform = modal_ctx.responses["platform"]
    why = modal_ctx.responses.get("why", "")

    valid_platforms = ["BlueSky", "YouTube", "X (Twitter)", "Instagram", "TikTok"]
    if platform not in valid_platforms:
        await modal_ctx.send(f"Invalid platform selected. Please choose one of the following: {', '.join(valid_platforms)}", ephemeral=True)
        return

    await modal_ctx.send("Ajout de l'utilisateur dans la base de données des signalements, veuillez patienter\nhttps://tenor.com/view/m%C3%A9lenchon-bg-jlm-m%C3%A9lanchon-pr%C3%A9sidentielles-gif-23207938", ephemeral=True)
    url = source
    try:
        wayback = waybackpy.Url(url)
        archive_url = wayback.save()
    except:
        archive_url = source

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
    await ctx.send(embed=embed, ephemeral=True)

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
    data = [
        "%"+pseudo+"%"
    ]
    cur.execute("SELECT * FROM reports WHERE Pseudo LIKE ?", data)
    data = cur.fetchall()

    await ctx.send("Here is all the report that concern the provided user")
    for d in data:
        await ctx.send("## "+str(d[5])+"\n> plateforme : "+str(d[6])+"\n> Raison : "+str(d[4])+"\n> Post problématique : [Post original](<"+str(d[2])+">)  [Lien archive.org](<"+str(d[3])+">)\n> Statut : à implémenter")

"""
Réponse si des liens sont envoyés
"""
import re

@listen()
async def on_message_create(event):
    if event.message.author.bot:
        return
    ret_message = "-# "+random.choice([
                    "⚠️ - Ce compte à été signalé comme étant une source d'extrême droite",
                    "Ce post provient d’un compte signalé F",
                    "C'est un compte cancel ça, faites mieux"
                    ])
    print("message : "+event.message.content)
    # Vérifie si le message contient un lien vers "bsky.social/"
    if "bsky.app/" in event.message.content:
        # Extrait le pseudonyme à partir du lien

        match = re.search(r"bsky\.app/profile/([^/]+)/post/", event.message.content)
        print(match)
        if match:
            url_username = match.group(1)

            # Connexion à la base de données et vérification du pseudonyme
            cur = con.cursor()
            cur.execute("SELECT Pseudo FROM reports WHERE platform = \"BlueSky\"")
            data = cur.fetchall()

            # Vérifie si le pseudonyme est dans la base de données
            if (url_username,) in data:
                await event.message.reply(ret_message, allowed_mentions=AllowedMentions(replied_user=False))
                
   

bot.start()