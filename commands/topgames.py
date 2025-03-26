import discord
from discord import app_commands
from discord.ext import commands
import json
import os
import re

class TopGames(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def convert_time(self, t):
        if isinstance(t, (int, float)):
            return float(t)
        match = re.match(r"^(\d+(?:\.\d+)?)h$", str(t))
        return float(match.group(1)) if match else 0.0

    @app_commands.guilds(discord.Object(id=1354050748962574357))
    @app_commands.command(name="topgames", description="Affiche tes 3 jeux les plus longs")
    async def topgames(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)

        if not os.path.exists("games.json"):
            await interaction.response.send_message("❌ Aucun jeu trouvé.", ephemeral=True)
            return

        with open("games.json", "r") as f:
            games = json.load(f)

        user_games = games.get(user_id, [])
        if not user_games:
            await interaction.response.send_message("❌ Aucun jeu trouvé.", ephemeral=True)
            return

        sorted_games = sorted(user_games, key=lambda g: self.convert_time(g["time_played"]), reverse=True)[:3]

        response = "🏆 **Top 3 jeux les plus longs** :\n\n"
        for i, game in enumerate(sorted_games, 1):
            response += f"{i}. **{game['title']}** – {self.convert_time(game['time_played'])}h\n"

        await interaction.response.send_message(response, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(TopGames(bot))
