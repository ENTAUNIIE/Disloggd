import discord
from discord import app_commands
from discord.ext import commands
import json
import os
import re
from datetime import datetime

class AddGameSlash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.guilds(discord.Object(id=1354050748962574357))  # ID de ton serveur
    @app_commands.command(name="addgame", description="Ajoute un jeu à ta liste")
    @app_commands.describe(
        title="Nom du jeu",
        time_played="Temps de jeu (ex: 100h)",
        date="Date jouée (YYYY-MM-DD)",
        status="Statut du jeu"
    )
    @app_commands.choices(
        status=[
            app_commands.Choice(name="Completed", value="Completed"),
            app_commands.Choice(name="Played", value="Played"),
            app_commands.Choice(name="Shelved", value="Shelved")
        ]
    )
    async def addgame(
        self,
        interaction: discord.Interaction,
        title: str,
        time_played: str,
        date: str,
        status: app_commands.Choice[str]
    ):
        # ✅ Vérifier le format de la date
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            await interaction.response.send_message(
                "❌ Format de date invalide. Utilise YYYY-MM-DD (ex: 2025-03-25).",
                ephemeral=True
            )
            return

        # ✅ Vérifier et convertir le temps de jeu (ex: 100h, 12.5h)
        match = re.match(r"^(\d+(?:\.\d+)?)h$", time_played.lower())
        if not match:
            await interaction.response.send_message(
                "❌ Format de temps invalide. Utilise un format comme `100h` ou `12.5h`.",
                ephemeral=True
            )
            return

        time_played_float = float(match.group(1))  # Extrait 100 ou 12.5

        user_id = str(interaction.user.id)
        game_data = {
            "title": title,
            "time_played": time_played_float,
            "date": date,
            "status": status.value
        }

        # Charger ou créer games.json
        if os.path.exists("games.json"):
            with open("games.json", "r") as f:
                games = json.load(f)
        else:
            games = {}

        if user_id not in games:
            games[user_id] = []

        games[user_id].append(game_data)

        with open("games.json", "w") as f:
            json.dump(games, f, indent=4)

        await interaction.response.send_message(
            f"✅ Jeu ajouté : **{title}** – {time_played_float}h, {date}, {status.value}",
            ephemeral=False
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(AddGameSlash(bot))
