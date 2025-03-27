import discord
from discord import app_commands
from discord.ext import commands
import json
import os

TRACKING_FILE = "tracking.json"

class TrackCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def set_tracking_status(self, user_id, enabled):
        if not os.path.exists(TRACKING_FILE):
            data = {}
        else:
            with open(TRACKING_FILE, "r") as f:
                data = json.load(f)

        data[str(user_id)] = enabled

        with open(TRACKING_FILE, "w") as f:
            json.dump(data, f, indent=4)

    def is_tracking_enabled(self, user_id):
        if not os.path.exists(TRACKING_FILE):
            return False
        with open(TRACKING_FILE, "r") as f:
            data = json.load(f)
        return data.get(str(user_id), False)

    @app_commands.guilds(discord.Object(id=1354050748962574357))  # ton serveur
    @app_commands.command(name="track", description="Active ou désactive le tracking automatique")
    @app_commands.describe(mode="Activer ou désactiver le tracking auto")
    @app_commands.choices(
        mode=[
            app_commands.Choice(name="on", value="on"),
            app_commands.Choice(name="off", value="off")
        ]
    )
    async def track(self, interaction: discord.Interaction, mode: app_commands.Choice[str]):
        enabled = mode.value == "on"
        user_id = interaction.user.id

        if self.is_tracking_enabled(user_id) == enabled:
            msg = (
                "⚠️ Le tracking est **déjà activé**." if enabled 
                else "⚠️ Le tracking est **déjà désactivé**."
            )
            return await interaction.response.send_message(msg, ephemeral=True)

        self.set_tracking_status(user_id, enabled)

        msg = (
            "🟢 Tracking activé. Tes activités de jeu seront détectées automatiquement." 
            if enabled else 
            "🔴 Tracking désactivé. Tes jeux ne seront plus suivis automatiquement."
        )
        await interaction.response.send_message(msg, ephemeral=True)

async def setup(bot):
    await bot.add_cog(TrackCommand(bot))
