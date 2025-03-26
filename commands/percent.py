import discord
from discord import app_commands
from discord.ext import commands
import json
import os

class GamePercent(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.guilds(discord.Object(id=1354050748962574357))
    @app_commands.command(name="percent", description="Affiche ton pourcentage de jeux complétés")
    async def percent(self, interaction: discord.Interaction):
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

        total = len(user_games)
        completed = sum(1 for g in user_games if g["status"] == "Completed")
        percent = (completed / total) * 100

        await interaction.response.send_message(
            f"📈 Tu as complété **{completed}** jeu(x) sur **{total}** → **{round(percent, 1)}%** ✅",
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(GamePercent(bot))
