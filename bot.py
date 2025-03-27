import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
load_dotenv(dotenv_path=".env")

print("✅ Chargement .env")
print("TOKEN :", os.getenv("DISCORD_TOKEN"))



# Intents requis (notamment pour message_content dans les commandes texte)
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True


# Création du bot avec préfixe ! pour les commandes classiques
bot = commands.Bot(command_prefix="!", intents=intents)

# Événement lancé quand le bot est connecté
@bot.event
async def on_ready():
    print(f"✅ Disloggd connecté en tant que {bot.user}")
    
    try:
        print("📦 Chargement des membres…")
        for guild in bot.guilds:
            await guild.chunk()  # charge les membres si pas déjà en cache
        print("✅ Membres chargés.")

        GUILD_ID = 1354050748962574357
        guild = discord.Object(id=GUILD_ID)

        synced = await bot.tree.sync(guild=guild)
        print(f"✅ {len(synced)} slash command(s) synchronisée(s) dans la guild.")
        
    except Exception as e:
        print(f"❌ Erreur de synchronisation des slash commands : {e}")
# Chargement des commandes dans le dossier /commands
async def load_extensions():
    files = sorted(f for f in os.listdir("./commands") if f.endswith(".py"))

    print(f"🔍 Commandes détectées ({len(files)}) :")
    for filename in files:
        try:
            await bot.load_extension(f"commands.{filename[:-3]}")
            print(f"✅ Commande chargée : {filename}")
        except Exception as e:
            print(f"❌ Erreur chargement {filename} : {e}")

# Lancement du bot 
async def main():
    async with bot:
        await load_extensions()
        await bot.start(os.getenv("DISCORD_TOKEN"))  

# Exécution principale
asyncio.run(main())
