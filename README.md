# Habit Tracker - Flask API

MySQL as database 


Initial file setup:
$python3 -m venv env

command + shift + P (python sele3ct interpreter, if not automatic, will be the current version that starts iwth ./env or .\env)

ctrl + shift + ` (create new integrated terminal in virtual environment)
pip3 install flask

create new .py file

save

$export FLASK_APP = api.py

$python3 -m flask fun



To connect to react:

$pip3 install -U flask-cors

inside api.py:

from flask_cors import CORS

CORS(app)



see requirements.txt for installed packages...
