import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from datetime import datetime

MAX_PER_PAGE = 5

class MyGamesView(discord.ui.View):
    def __init__(self, interaction: discord.Interaction, games, filter_status="All", page=0):
        super().__init__(timeout=None)
        self.interaction = interaction
        self.all_games = games
        self.filter_status = filter_status
        self.page = page
        self.update_buttons()

    def filtered_games(self):
        if self.filter_status == "All":
            return self.all_games
        return [g for g in self.all_games if g["status"] == self.filter_status]

    def paginated_games(self):
        filtered = self.filtered_games()
        start = self.page * MAX_PER_PAGE
        end = start + MAX_PER_PAGE
        return filtered[start:end]

    def update_buttons(self):
        total_pages = max(1, (len(self.filtered_games()) - 1) // MAX_PER_PAGE + 1)
        self.children[4].disabled = self.page <= 0
        self.children[5].disabled = self.page >= total_pages - 1

    def get_embed(self):
        embed = discord.Embed(
            title="🎮 Mes jeux",
            description=f"Filtre : **{self.filter_status}**",
            color=discord.Color.blurple()
        )

        page_games = self.paginated_games()
        if not page_games:
            embed.description = f"Aucun jeu avec le filtre **{self.filter_status}**."
            return embed

        for game in page_games:
            added = game.get("added_at", "❓")
            completed = game.get("completed_at", None)
            value = f"🕒 {game['time_played']}h\n📅 Ajouté : {added}"
            if completed:
                value += f"\n✅ Terminé : {completed}"
            value += f"\n🏷️ Statut : {game['status']}"
            embed.add_field(name=f"🎮 {game['title']}", value=value, inline=False)

        total = len(self.filtered_games())
        total_pages = max(1, (total - 1) // MAX_PER_PAGE + 1)
        embed.set_footer(text=f"Page {self.page + 1}/{total_pages} • {total} jeu(x) total")

        return embed

    # Boutons de filtre
    @discord.ui.button(label="Tous", style=discord.ButtonStyle.secondary, row=0)
    async def all(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.filter_status = "All"
        self.page = 0
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Completed", style=discord.ButtonStyle.success, row=0)
    async def completed(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.filter_status = "Completed"
        self.page = 0
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Played", style=discord.ButtonStyle.primary, row=0)
    async def played(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.filter_status = "Played"
        self.page = 0
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="Shelved", style=discord.ButtonStyle.danger, row=0)
    async def shelved(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.filter_status = "Shelved"
        self.page = 0
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    # Pagination
    @discord.ui.button(label="◀️", style=discord.ButtonStyle.secondary, row=1)
    async def previous(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 0:
            self.page -= 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @discord.ui.button(label="▶️", style=discord.ButtonStyle.secondary, row=1)
    async def next(self, interaction: discord.Interaction, button: discord.ui.Button):
        total_pages = max(1, (len(self.filtered_games()) - 1) // MAX_PER_PAGE + 1)
        if self.page < total_pages - 1:
            self.page += 1
            self.update_buttons()
            await interaction.response.edit_message(embed=self.get_embed(), view=self)


class MyGames(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.guilds(discord.Object(id=1354050748962574357))
    @app_commands.command(name="mygames", description="Affiche tes jeux enregistrés avec filtrage")
    async def mygames(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)

        if not os.path.exists("games.json"):
            return await interaction.response.send_message("Aucune donnée trouvée.", ephemeral=True)

        with open("games.json", "r") as f:
            data = json.load(f)

        games = data.get(user_id, [])
        if not games:
            return await interaction.response.send_message("Tu n’as encore aucun jeu enregistré.", ephemeral=True)

        view = MyGamesView(interaction, games)
        await interaction.response.send_message(embed=view.get_embed(), view=view, ephemeral=True)


async def setup(bot):
    print("📥 Chargement du cog : MyGames")  # Debug
    await bot.add_cog(MyGames(bot))
