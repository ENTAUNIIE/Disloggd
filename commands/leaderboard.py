import discord
from discord import app_commands
from discord.ext import commands
import json
import os
import re

class Leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def convert_time(self, t):
        if isinstance(t, (int, float)):
            return float(t)
        match = re.match(r"^(\d+(?:\.\d+)?)h$", str(t))
        return float(match.group(1)) if match else 0.0

    @app_commands.guilds(discord.Object(id=1354050748962574357))
    @app_commands.command(name="leaderboard", description="Classement par temps de jeu ou nombre de jeux")
    @app_commands.describe(
        type="Type de classement",
        status="Statut des jeux à inclure (facultatif)"
    )
    @app_commands.choices(
        type=[
            app_commands.Choice(name="Temps", value="time"),
            app_commands.Choice(name="Nombre", value="count")
        ],
        status=[
            app_commands.Choice(name="Tous", value="all"),
            app_commands.Choice(name="Completed", value="Completed"),
            app_commands.Choice(name="Played", value="Played"),
            app_commands.Choice(name="Shelved", value="Shelved"),
        ]
    )
    async def leaderboard(
        self,
        interaction: discord.Interaction,
        type: app_commands.Choice[str],
        status: app_commands.Choice[str] = None
    ):
        if not os.path.exists("games.json"):
            await interaction.response.send_message("📂 Aucun fichier trouvé.", ephemeral=True)
            return

        with open("games.json", "r") as f:
            data = json.load(f)

        results = []
        for user_id, game_list in data.items():
            if status and status.value != "all":
                filtered = [g for g in game_list if g.get("status") == status.value]
            else:
                filtered = game_list

            if type.value == "time":
                total = sum(self.convert_time(g.get("time_played", 0)) for g in filtered)
            else:
                total = len(filtered)

            if total > 0:
                results.append((user_id, total))

        if not results:
            await interaction.response.send_message("ℹ️ Aucun joueur trouvé avec ces critères.", ephemeral=True)
            return

        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)[:5]

        title = "🏆 Leaderboard – "
        title += "Temps total joué" if type.value == "time" else "Nombre de jeux"
        if status and status.value != "all":
            title += f" ({status.value})"

        description = ""
        for rank, (user_id, value) in enumerate(sorted_results, start=1):
            user = await self.bot.fetch_user(int(user_id))
            unit = "h" if type.value == "time" else "jeu(x)"
            description += f"**#{rank}** – {user.name} : {round(value, 1) if type.value == 'time' else value} {unit}\n"

        embed = discord.Embed(
            title=title,
            description=description,
            color=discord.Color.orange()
        )

        await interaction.response.send_message(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(Leaderboard(bot))
