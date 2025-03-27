import discord
from discord import app_commands
from discord.ext import commands

class ForceCheck(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="forcecheck", description="Force la vérification du jeu en cours.")
    async def forcecheck(self, interaction: discord.Interaction):
        user = interaction.user

        activity = next(
            (a for a in user.activities if isinstance(a, (discord.Game, discord.Activity)) and a.name),
            None
        )
        current_game = activity.name if activity else None

        if current_game:
            await interaction.response.send_message(
                f"🎮 Jeu actuellement détecté sur ton profil : **{current_game}**",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ Aucune activité détectée sur ton profil Discord.",
                ephemeral=True
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(ForceCheck(bot))
