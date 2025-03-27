import discord
from discord import app_commands
from discord.ext import commands
import json
import datetime
import os

class AddGameSlash(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.guilds(discord.Object(id=1354050748962574357))
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
        user_id = str(interaction.user.id)
        game = {
            "title": title,
            "time_played": time_played,
            "date": date,
            "status": status.value,
            "added_at": datetime.datetime.utcnow().strftime("%Y-%m-%d")
        }

        if not os.path.exists("games.json"):
            games = {}
        else:
            with open("games.json", "r") as f:
                games = json.load(f)

        if user_id not in games:
            games[user_id] = []

        games[user_id].append(game)

        with open("games.json", "w") as f:
            json.dump(games, f, indent=4)

        await interaction.response.send_message(
            f"✅ Jeu ajouté : **{title}** – {time_played}, {date}, {status.value}",
            ephemeral=False
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(AddGameSlash(bot))
