import discord
from discord import app_commands
from discord.ext import commands
import json
import os

class MyGames(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.guilds(discord.Object(id=1354050748962574357))  # Ton serveur
    @app_commands.command(name="mygames", description="Affiche ta liste de jeux")
    @app_commands.describe(status="Filtrer par statut (Completed, Played, Shelved)")
    @app_commands.choices(
        status=[
            app_commands.Choice(name="Completed", value="Completed"),
            app_commands.Choice(name="Played", value="Played"),
            app_commands.Choice(name="Shelved", value="Shelved")
        ]
    )
    async def mygames(
        self,
        interaction: discord.Interaction,
        status: app_commands.Choice[str] = None  # Optionnel
    ):
        user_id = str(interaction.user.id)

        # Vérifie si le fichier existe
        if not os.path.exists("games.json"):
            await interaction.response.send_message("ℹ️ Tu n’as encore aucun jeu enregistré.", ephemeral=True)
            return

        with open("games.json", "r") as f:
            games = json.load(f)

        user_games = games.get(user_id, [])

        if not user_games:
            await interaction.response.send_message("ℹ️ Tu n’as encore aucun jeu enregistré.", ephemeral=True)
            return

        # Si un statut est spécifié, filtrer
        if status:
            user_games = [g for g in user_games if g["status"] == status.value]

        if not user_games:
            await interaction.response.send_message(f"ℹ️ Aucun jeu trouvé avec le statut **{status.value}**.", ephemeral=True)
            return

        response = f"🎮 **Jeux de {interaction.user.name}**"
        if status:
            response += f" – **{status.value}**"
        response += " :\n\n"

        for game in user_games:
            response += f"• **{game['title']}** – {game['time_played']}h – {game['date']} – {game['status']}\n"

        await interaction.response.send_message(response, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(MyGames(bot))
