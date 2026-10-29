ATMOS — WEATHER INTELLIGENCE
============================

Lancer en local
1. Installer Python 3.10+
2. Dans le dossier du projet :
   py -m pip install -r requirements.txt
3. Lancer :
   py app.py
4. Ouvrir http://127.0.0.1:5000

Déploiement Render
- Root Directory : atmos_simple (si le dépôt contient le dossier parent atmos_simple)
  Si app.py est à la racine du dépôt, laisser Root Directory vide.
- Build Command : pip install -r requirements.txt
- Start Command : gunicorn app:app
- Utiliser le forfait Free si disponible.

Fonctionnalités
- Recherche de villes par géocodage Open-Meteo
- Conditions actuelles
- Graphique de température et ressenti heure par heure
- Prévisions sur 7 jours et probabilités de précipitations
- Carte interactive des températures dans les principales villes françaises
- Humidité, vent, UV, lever/coucher du soleil

La carte et les graphiques utilisent des bibliothèques CDN (Chart.js, Leaflet)
et nécessitent une connexion Internet. Données météo via Open-Meteo.
