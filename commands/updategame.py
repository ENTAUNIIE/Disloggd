import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from datetime import datetime

class UpdateGame(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(discord.Object(id=1354050748962574357))
    @app_commands.command(name="updategame", description="Met à jour un jeu")
    @app_commands.describe(
        title="Nom du jeu à modifier",
        time_played="Nouveau temps de jeu (optionnel)",
        date="Nouvelle date (optionnel)",
        status="Nouveau statut (optionnel)"
    )
    @app_commands.choices(status=[
        app_commands.Choice(name="Completed", value="Completed"),
        app_commands.Choice(name="Played", value="Played"),
        app_commands.Choice(name="Shelved", value="Shelved")
    ])
    async def updategame(
        self,
        interaction: discord.Interaction,
        title: str,
        time_played: str = None,
        date: str = None,
        status: app_commands.Choice[str] = None
    ):
        user_id = str(interaction.user.id)

        if not os.path.exists("games.json"):
            return await interaction.response.send_message("Aucune donnée trouvée.", ephemeral=True)

        with open("games.json", "r") as f:
            games = json.load(f)

        user_games = games.get(user_id, [])
        game = next((g for g in user_games if g["title"].lower() == title.lower()), None)

        if not game:
            return await interaction.response.send_message("❌ Jeu non trouvé.", ephemeral=True)

        if time_played:
            try:
                game["time_played"] = float(time_played.replace("h", "").strip())
            except ValueError:
                return await interaction.response.send_message("⛔ Format de temps invalide.", ephemeral=True)

        if date:
            try:
                datetime.strptime(date, "%Y-%m-%d")
                game["date"] = date
            except ValueError:
                return await interaction.response.send_message("⛔ Format de date invalide. (YYYY-MM-DD)", ephemeral=True)

        if status:
            game["status"] = status.value
            if status.value == "Completed":
                game["completed_at"] = datetime.utcnow().strftime("%Y-%m-%d")

        with open("games.json", "w") as f:
            json.dump(games, f, indent=4)

        await interaction.response.send_message(f"✅ Jeu mis à jour : **{title}**", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(UpdateGame(bot))
