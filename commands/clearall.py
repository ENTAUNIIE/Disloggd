import discord
from discord import app_commands
from discord.ext import commands
import json
import os

class ClearAllView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=30)  # Boutons valables 30 secondes
        self.user_id = user_id

    @discord.ui.button(label="✅ Oui, je le veux", style=discord.ButtonStyle.danger)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ Tu ne peux pas utiliser ce bouton.", ephemeral=True)
            return

        if not os.path.exists("games.json"):
            await interaction.response.send_message("📂 Aucun fichier trouvé.", ephemeral=True)
            return

        with open("games.json", "r") as f:
            data = json.load(f)

        if self.user_id in data:
            del data[self.user_id]
            with open("games.json", "w") as f:
                json.dump(data, f, indent=4)
            await interaction.response.edit_message(content="🧼 Tous tes jeux ont été supprimés !", view=None)
        else:
            await interaction.response.edit_message(content="ℹ️ Tu n’avais aucun jeu enregistré.", view=None)

    @discord.ui.button(label="❌ Annuler", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        if str(interaction.user.id) != self.user_id:
            await interaction.response.send_message("❌ Tu ne peux pas utiliser ce bouton.", ephemeral=True)
            return

        await interaction.response.edit_message(content="❎ Suppression annulée.", view=None)

class ClearAll(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.guilds(discord.Object(id=1354050748962574357))
    @app_commands.command(name="clearall", description="⚠️ Supprime tous tes jeux")
    async def clearall(self, interaction: discord.Interaction):
        view = ClearAllView(str(interaction.user.id))
        await interaction.response.send_message(
            "⚠️ Tu es sur le point de **supprimer tous tes jeux enregistrés**.\n\nSouhaites-tu vraiment continuer ?",
            view=view,
            ephemeral=True
        )

async def setup(bot: commands.Bot):
    await bot.add_cog(ClearAll(bot))
