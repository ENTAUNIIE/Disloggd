import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
load_dotenv()


# Intents requis (notamment pour message_content dans les commandes texte)
intents = discord.Intents.default()
intents.message_content = True

# Création du bot avec préfixe ! pour les commandes classiques
bot = commands.Bot(command_prefix="!", intents=intents)

# Événement lancé quand le bot est connecté
@bot.event
async def on_ready():
    print(f"✅ Disloggd connecté en tant que {bot.user}")

    try:
        GUILD_ID = 1354050748962574357  # Ton serveur
        guild = discord.Object(id=GUILD_ID)

        synced = await bot.tree.sync(guild=guild)
        print(f"✅ {len(synced)} slash command(s) synchronisée(s) dans la guild.")
    except Exception as e:
        print(f"❌ Erreur de synchronisation des slash commands : {e}")

# Chargement des commandes dans le dossier /commands
async def load_extensions():
    for filename in os.listdir("./commands"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f"commands.{filename[:-3]}")
                print(f"✅ Commande chargée : {filename}")
            except Exception as e:
                print(f"❌ Erreur chargement {filename} : {e}")

# Lancement du bot (nouveau système recommandé pour async)
async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv("DISCORD_TOKEN"))  

# Exécution principale
asyncio.run(main())
