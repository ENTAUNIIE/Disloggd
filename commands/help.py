import discord
from discord.ext import commands
from discord import app_commands

GUILD_ID = 1354050748962574357  # Remplace si besoin

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Affiche toutes les commandes disponibles")
    @app_commands.guilds(discord.Object(id=GUILD_ID))
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="📖 Aide Disloggd",
            description="Voici toutes les commandes disponibles :",
            color=discord.Color.blurple()
        )

        # 🔁 Récupère toutes les commandes dans le serveur
        commands_list = self.bot.tree.get_commands(guild=discord.Object(id=GUILD_ID))
        commands_list.sort(key=lambda c: c.name)

        for command in commands_list:
            desc = command.description or "Aucune description"
            embed.add_field(name=f"/{command.name}", value=desc, inline=False)

        embed.set_footer(text="Disloggd v1.1 • par Entaunie")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(HelpCommand(bot))
