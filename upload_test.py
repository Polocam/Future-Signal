"""Envoie sur YouTube la vidéo déjà créée (test de publication).

À lancer depuis le dossier du projet :  python upload_test.py
Utilise les mêmes appels que run_now.py (YouTubeUploader + metadata.json).
"""
import json
import logging
from pathlib import Path

from uploaders.youtube import YouTubeUploader

logging.basicConfig(level=logging.INFO)

CHANNEL = "Future Signal"
FOLDER = Path("output") / CHANNEL / "When_The_Global_Internet_Suddenly_Stops" / "final"

videos = sorted(FOLDER.glob("*.mp4"), key=lambda p: p.stat().st_mtime, reverse=True)
if not videos:
    raise SystemExit(f"Aucune vidéo .mp4 trouvée dans {FOLDER}")
video = videos[0]

meta_path = FOLDER / "metadata.json"
if not meta_path.exists():
    raise SystemExit(f"metadata.json introuvable dans {FOLDER}")
meta = json.loads(meta_path.read_text(encoding="utf-8"))

title = meta.get("viral_title", "Future Signal")
description = meta.get("short_description", "")
tags = meta.get("hashtags", ["#shorts"])
hashtags = " ".join(t if t.startswith("#") else f"#{t}" for t in tags)
full_description = f"{description}\n\n{hashtags}"

print(f"Vidéo     : {video.name}")
print(f"Titre     : {title}")
print(f"Hashtags  : {hashtags}")

token = f"youtube_credentials_{CHANNEL.replace(' ', '_')}.json"
YouTubeUploader(token_file=token).upload_video(str(video), title, full_description, tags)
print("Envoi terminé : vérifie YouTube Studio > Contenu.")
