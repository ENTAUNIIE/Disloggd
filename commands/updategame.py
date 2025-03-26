import discord
from discord import app_commands
from discord.ext import commands
import json
import os
import re
from datetime import datetime

class UpdateGame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.guilds(discord.Object(id=1354050748962574357))  # Ton serveur
    @app_commands.command(name="updategame", description="Met à jour un jeu dans ta liste")
    @app_commands.describe(
        title="Nom du jeu à modifier",
        new_title="Nouveau titre (facultatif)",
        time_played="Temps joué (ex: 120h)",
        date="Nouvelle date (YYYY-MM-DD)",
        status="Nouveau statut"
    )
    @app_commands.choices(
        status=[
            app_commands.Choice(name="Completed", value="Completed"),
            app_commands.Choice(name="Played", value="Played"),
            app_commands.Choice(name="Shelved", value="Shelved")
        ]
    )
    async def updategame(
        self,
        interaction: discord.Interaction,
        title: str,
        new_title: str = None,
        time_played: str = None,
        date: str = None,
        status: app_commands.Choice[str] = None
    ):
        user_id = str(interaction.user.id)

        if not os.path.exists("games.json"):
            await interaction.response.send_message("❌ Tu n’as aucun jeu enregistré.", ephemeral=True)
            return

        with open("games.json", "r") as f:
            games = json.load(f)

        user_games = games.get(user_id, [])
        for game in user_games:
            if game["title"].lower() == title.lower():
                if new_title:
                    game["title"] = new_title
                if time_played:
                    match = re.match(r"^(\d+(?:\.\d+)?)h$", time_played.lower())
                    if not match:
                        await interaction.response.send_message("❌ Temps invalide. Format : `150h`", ephemeral=True)
                        return
                    game["time_played"] = float(match.group(1))
                if date:
                    try:
                        datetime.strptime(date, "%Y-%m-%d")
                        game["date"] = date
                    except ValueError:
                        await interaction.response.send_message("❌ Date invalide. Format : YYYY-MM-DD", ephemeral=True)
                        return
                if status:
                    game["status"] = status.value

                games[user_id] = user_games
                with open("games.json", "w") as f:
                    json.dump(games, f, indent=4)

                await interaction.response.send_message(f"✅ Jeu **{title}** mis à jour avec succès !", ephemeral=False)
                return

        await interaction.response.send_message(f"❌ Jeu **{title}** introuvable.", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(UpdateGame(bot))
