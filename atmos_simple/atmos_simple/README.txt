ATMOS — SITE MÉTÉO SIMPLE EN PYTHON
====================================

Fichiers :
- app.py : serveur Python Flask et appels à l'API météo
- templates/index.html : contenu HTML
- static/style.css : design du site
- requirements.txt : bibliothèques nécessaires

LANCEMENT
1. Installe Python si nécessaire.
2. Ouvre le dossier atmos_simple dans Visual Studio Code.
3. Dans le terminal, exécute :
   python -m pip install -r requirements.txt
4. Puis :
   python app.py
5. Ouvre http://127.0.0.1:5000 dans ton navigateur.

Le site utilise l'API Open-Meteo, sans clé API pour commencer. Une connexion Internet est nécessaire.
Modifie librement les fichiers pour apprendre. Le mode debug Flask est destiné au développement local, pas à un serveur public.
