import discord
from discord import app_commands
from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.guilds(discord.Object(id=1354050748962574357))  # Ton serveur
    @app_commands.command(name="help", description="Affiche toutes les commandes de Disloggd")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📘 Aide Disloggd",
            description="Voici la liste des commandes disponibles :",
            color=discord.Color.blurple()
        )

        embed.add_field(
            name="➕ /addgame",
            value="Ajoute un jeu à ta liste.\n**Format requis :**\n• `Temps` → `100h`\n• `Date` → `YYYY-MM-DD`\n• `Status` → Completed / Played / Shelved",
            inline=False
        )

        embed.add_field(
            name="🎮 /mygames [status]",
            value="Affiche tous tes jeux, ou filtre par statut (optionnel).",
            inline=False
        )

        embed.add_field(
            name="📊 /stats",
            value="Affiche tes stats : total de jeux, heures, par statut, et ton jeu le plus long.",
            inline=False
        )

        embed.add_field(
            name="❓ /help",
            value="Affiche ce message d’aide.",
            inline=False
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCommand(bot))
