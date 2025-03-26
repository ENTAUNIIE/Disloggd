import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from io import BytesIO

class ExportGames(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.guilds(discord.Object(id=1354050748962574357))
    @app_commands.command(name="export", description="Exporte ta liste de jeux en JSON")
    async def export(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)

        if not os.path.exists("games.json"):
            await interaction.response.send_message("❌ Aucun jeu trouvé.", ephemeral=True)
            return

        with open("games.json", "r") as f:
            games = json.load(f)

        user_data = games.get(user_id)
        if not user_data:
            await interaction.response.send_message("❌ Aucun jeu trouvé.", ephemeral=True)
            return

        json_data = json.dumps(user_data, indent=4)
        file = BytesIO(json_data.encode("utf-8"))
        file.seek(0)

        discord_file = discord.File(file, filename="disloggd_export.json")
        await interaction.response.send_message("📦 Voici ton export :", file=discord_file, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(ExportGames(bot))
