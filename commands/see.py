import discord
from discord import app_commands
from discord.ext import commands
import json
import os
import re

class SeeStats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def convert_time(self, t):
        if isinstance(t, (int, float)):
            return float(t)
        match = re.match(r"^(\d+(?:\.\d+)?)h$", str(t))
        return float(match.group(1)) if match else 0.0

    @app_commands.guilds(discord.Object(id=1354050748962574357))  # Ton serveur
    @app_commands.command(name="see", description="Affiche les stats d'un autre utilisateur")
    @app_commands.describe(user="L'utilisateur à inspecter")
    async def see(self, interaction: discord.Interaction, user: discord.User):
        user_id = str(user.id)

        if not os.path.exists("games.json"):
            await interaction.response.send_message("📂 Aucun fichier trouvé.", ephemeral=True)
            return

        with open("games.json", "r") as f:
            data = json.load(f)

        user_games = data.get(user_id, [])
        if not user_games:
            await interaction.response.send_message(f"ℹ️ {user.name} n’a aucun jeu enregistré.", ephemeral=True)
            return

        total = len(user_games)
        total_hours = sum(self.convert_time(g.get("time_played", 0)) for g in user_games)

        status_counts = {"Completed": 0, "Played": 0, "Shelved": 0}
        for g in user_games:
            status = g.get("status")
            if status in status_counts:
                status_counts[status] += 1

        longest = max(user_games, key=lambda g: self.convert_time(g["time_played"]))
        longest_title = longest["title"]
        longest_time = self.convert_time(longest["time_played"])

        response = (
            f"🔍 **Stats de {user.name}** :\n\n"
            f"🎮 Jeux enregistrés : **{total}**\n"
            f"⏱ Temps total joué : **{round(total_hours, 1)}h**\n\n"
            f"✅ Completed : {status_counts['Completed']}\n"
            f"🕹 Played : {status_counts['Played']}\n"
            f"📦 Shelved : {status_counts['Shelved']}\n\n"
            f"🏆 Jeu le plus long : **{longest_title}** – {longest_time}h"
        )

        await interaction.response.send_message(response, ephemeral=False)

async def setup(bot: commands.Bot):
    await bot.add_cog(SeeStats(bot))
