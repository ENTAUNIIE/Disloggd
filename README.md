# 🎮 Disloggd

**Disloggd** est un bot Discord conçu pour t’aider à suivre ta progression dans les jeux vidéo.  
Ajoute des jeux, track ton temps automatiquement, consulte tes stats et plus encore !

> Développé avec ❤️ par [Entaunie](https://github.com/ENTAUNIIE) – version actuelle : `v1.1`

---

## ✨ Fonctions principales

- `/addgame` – Ajoute manuellement un jeu à ta liste
- `/updategame` – Modifie les infos d’un jeu (statut, temps, etc.)
- `/remove` – Supprime un jeu
- `/clearall` – Supprime tous tes jeux (avec confirmation)
- `/mygames` – Liste tes jeux avec pagination et filtres par statut
- `/stats` – Statistiques globales de ta ludothèque
- `/topgames` – Tes jeux les plus longs
- `/percent` – Pourcentage de complétion
- `/leaderboard` – Comparatif entre utilisateurs
- `/see` – Voir les stats d’un autre utilisateur
- `/export` – Export de ta bibliothèque
- `/help` – Liste des commandes
- `/about` – Infos sur le bot

---

## 🎮 Tracking automatique

Disloggd peut détecter quand tu joues à un jeu et suivre ton temps **automatiquement** :

- `/track on` → Active le tracking automatique
- `/track off` → Le désactive
- `/forcecheck` → Forcer une détection
- `/nowplaying` → Voir le jeu actuellement détecté
- `/presencetrack` (interne) → Détection en temps réel via `on_presence_update`

> 🎯 Nécessite que l'activité soit visible sur Discord + permissions activées

---

## 🧠 Données enregistrées

Chaque jeu inclut :
- Titre
- Temps joué
- Statut (`Completed`, `Played`, `Shelved`)
- 📅 Date d’ajout (`added_at`)
- ✅ Date de fin (`ended_at` si complété)

Toutes les données sont sauvegardées dans `games.json` par utilisateur.

---

## 📦 Installation locale (dev)

### 1. Prérequis
- Python 3.10+
- [discord.py v2.3+](https://pypi.org/project/discord.py/)
- Fichier `.env` avec :
    DISCORD_TOKEN=xxxxxxxxxxxxxxx

### 2. Clonage et lancement

```bash
git clone https://github.com/ENTAUNIIE/Disloggd.git
cd Disloggd
pip install -r requirements.txt
python bot.py


🔒 RGPD & Données
Ce bot est open-source et ne stocke aucune info en ligne.
Tu peux consulter les documents :

📄 Terms of Service

🔒 Politique de confidentialité

🛠️ À venir (roadmap)
Système cloud pour héberger la sauvegarde

Ajout de tags ou notes sur chaque jeu

Import JSON de jeux (depuis HLTB ou Backloggd ?)

Interface web pour consulter ses stats

👤 Crédits
🧠 Développement : Entaunie

📁 Repo GitHub : https://github.com/ENTAUNIIE/Disloggd

Disloggd n'est affilié à aucun service externe type Steam, HLTB ou Backloggd.

yaml
Copier
Modifier

---

## 🛠 Et ensuite ?

