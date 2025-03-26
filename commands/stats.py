import discord
from discord import app_commands
from discord.ext import commands
import json
import os
import re

class GameStats(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.guilds(discord.Object(id=1354050748962574357))  # Ton ID serveur
    @app_commands.command(name="stats", description="Affiche tes statistiques de jeu")
    async def stats(self, interaction: discord.Interaction):
        try:
            user_id = str(interaction.user.id)

            if not os.path.exists("games.json"):
                await interaction.response.send_message("ℹ️ Tu n’as encore aucun jeu enregistré.", ephemeral=True)
                return

            with open("games.json", "r") as f:
                games = json.load(f)

            user_games = games.get(user_id, [])
            if not user_games:
                await interaction.response.send_message("ℹ️ Tu n’as encore aucun jeu enregistré.", ephemeral=True)
                return

            total_games = len(user_games)
            total_hours = 0.0
            by_status = {
                "Completed": 0,
                "Played": 0,
                "Shelved": 0
            }

            def convert_time(t):
                if isinstance(t, (int, float)):
                    return float(t)
                match = re.match(r"^(\d+(?:\.\d+)?)h$", str(t))
                return float(match.group(1)) if match else 0.0

            for game in user_games:
                time = convert_time(game.get("time_played", 0))
                total_hours += time
                status = game.get("status", "Unknown")
                if status in by_status:
                    by_status[status] += 1

            longest_game = max(user_games, key=lambda g: convert_time(g["time_played"]))

            response = (
                f"📊 **Stats de {interaction.user.name}** :\n\n"
                f"🎮 Total de jeux : **{total_games}**\n"
                f"⏱ Temps total joué : **{round(total_hours, 1)}h**\n\n"
                f"✅ Completed : {by_status['Completed']}\n"
                f"🕹 Played : {by_status['Played']}\n"
                f"📦 Shelved : {by_status['Shelved']}\n\n"
                f"🏆 Jeu le plus long : **{longest_game['title']}** – {convert_time(longest_game['time_played'])}h"
            )

            await interaction.response.send_message(response, ephemeral=True)

        except Exception as e:
            await interaction.response.send_message(f"❌ Erreur : `{e}`", ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(GameStats(bot))
