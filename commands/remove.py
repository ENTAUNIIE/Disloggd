import discord
from discord import app_commands
from discord.ext import commands
import json
import os

class RemoveGame(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.guilds(discord.Object(id=1354050748962574357))  # Ton serveur
    @app_commands.command(name="removegame", description="Supprime un jeu de ta liste")
    @app_commands.describe(title="Titre exact du jeu à supprimer")
    async def removegame(self, interaction: discord.Interaction, title: str):
        user_id = str(interaction.user.id)

        if not os.path.exists("games.json"):
            await interaction.response.send_message("❌ Aucun jeu trouvé.", ephemeral=True)
            return

        with open("games.json", "r") as f:
            games = json.load(f)

        user_games = games.get(user_id, [])

        new_list = [game for game in user_games if game["title"].lower() != title.lower()]
        removed = len(user_games) - len(new_list)

        if removed == 0:
            await interaction.response.send_message(f"❌ Aucun jeu nommé **{title}** trouvé.", ephemeral=True)
            return

        games[user_id] = new_list

        with open("games.json", "w") as f:
            json.dump(games, f, indent=4)

        await interaction.response.send_message(f"🗑️ Jeu **{title}** supprimé avec succès !", ephemeral=False)

async def setup(bot: commands.Bot):
    await bot.add_cog(RemoveGame(bot))
