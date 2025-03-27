import discord
from discord.ext import commands
import json
import os
import datetime
from tracking_data import active_sessions

CHANNEL_ID = 1354050749398519830  # Ton salon de logs

class PresenceTrack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_presence_update(self, before: discord.Member, after: discord.Member):
        if before.activities == after.activities:
            return  # Aucun changement détecté

        print(f"🎯 PRESENCE UPDATE: {after.name}")
        print("🟡 ACTIVITIES BEFORE :", [type(a).__name__ for a in before.activities])
        print("🟢 ACTIVITIES AFTER  :", [type(a).__name__ for a in after.activities])

        user_id = after.id

        # Vérifie si le tracking est activé
        if not os.path.exists("tracking.json"):
            return

        with open("tracking.json", "r") as f:
            tracking_data = json.load(f)

        if not tracking_data.get(str(user_id), False):
            return

        # 🔍 Détection du jeu via Game ou Activity
        activity = next(
            (a for a in after.activities if isinstance(a, (discord.Game, discord.Activity)) and a.name),
            None
        )
        current_game = activity.name if activity else None
        print("🎮 Jeu détecté :", current_game)

        session = active_sessions.get(user_id)

        # Début de session
        if current_game:
            if not session or session["game"] != current_game:
                active_sessions[user_id] = {
                    "game": current_game,
                    "start_time": datetime.datetime.utcnow()
                }
                print(f"🟢 {after.name} a lancé {current_game}")
                channel = self.bot.get_channel(CHANNEL_ID)
                if channel:
                    await channel.send(f"🎮 {after.mention} a lancé **{current_game}**. Bon jeu ! 🔥")

        # Fin de session
        elif session:
            duration = datetime.datetime.utcnow() - session["start_time"]
            hours_played = round(duration.total_seconds() / 3600, 2)

            game_data = {
                "title": session["game"],
                "time_played": hours_played,
                "date": datetime.datetime.utcnow().strftime("%Y-%m-%d"),
                "status": "Played"
            }

            user_id_str = str(user_id)
            games = {}

            if os.path.exists("games.json"):
                with open("games.json", "r") as f:
                    games = json.load(f)

            if user_id_str not in games:
                games[user_id_str] = []

            existing = next((g for g in games[user_id_str] if g["title"].lower() == session["game"].lower()), None)
            if existing:
                try:
                    existing["time_played"] = round(float(existing["time_played"]) + hours_played, 2)
                except:
                    existing["time_played"] = hours_played
            else:
                games[user_id_str].append(game_data)

            with open("games.json", "w") as f:
                json.dump(games, f, indent=4)

            print(f"🔴 {after.name} a quitté {session['game']} — {hours_played}h enregistrées.")
            channel = self.bot.get_channel(CHANNEL_ID)
            if channel:
                await channel.send(f"🛑 {after.mention} a quitté **{session['game']}** après **{hours_played}h** de jeu.")

            del active_sessions[user_id]

async def setup(bot: commands.Bot):
    await bot.add_cog(PresenceTrack(bot))
