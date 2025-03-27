import discord
from discord.ext import commands
from discord import app_commands

class About(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="about", description="À propos du projet Disloggd")
    async def about(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📌 À propos de Disloggd",
            description="Un bot Discord pour suivre et archiver tes sessions de jeu 🎮",
            color=discord.Color.green()
        )
        embed.add_field(name="👨‍💻 Développeur", value="`Entaunie#0001`", inline=True)
        embed.add_field(name="📁 GitHub", value="[Voir le projet](https://github.com/ENTAUNIIE/Disloggd)", inline=True)
        embed.add_field(name="📦 Version", value="`1.1`", inline=True)
        embed.set_footer(text="Merci d'utiliser Disloggd ❤️")

        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(About(bot))
