import discord
from discord import app_commands
from discord.ext import commands
import json
import os
import datetime
from tracking_data import active_sessions



TRACKING_FILE = "tracking.json"

class NowPlaying(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def is_tracking_enabled(self, user_id):
        if not os.path.exists(TRACKING_FILE):
            return False
        with open(TRACKING_FILE, "r") as f:
            data = json.load(f)
        return data.get(str(user_id), False)

    @app_commands.guilds(discord.Object(id=1354050748962574357))
    @app_commands.command(name="nowplaying", description="Affiche ton jeu en cours de tracking")
    async def nowplaying(self, interaction: discord.Interaction):
        user_id = interaction.user.id

        if not self.is_tracking_enabled(user_id):
            return await interaction.response.send_message("🔴 Le tracking automatique est désactivé pour toi.", ephemeral=True)

        session = active_sessions.get(user_id)

        if not session:
            return await interaction.response.send_message("❌ Aucune session de jeu détectée en ce moment.", ephemeral=True)

        game = session["game"]
        start_time = session["start_time"]
        elapsed = datetime.datetime.utcnow() - start_time
        elapsed_hours = round(elapsed.total_seconds() / 3600, 2)

        await interaction.response.send_message(
            f"🎮 Tu joues actuellement à **{game}** depuis **{elapsed_hours}h**.",
            ephemeral=False
        )

async def setup(bot):
    await bot.add_cog(NowPlaying(bot))
