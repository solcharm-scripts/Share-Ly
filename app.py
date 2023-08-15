from flask import Flask
import os
from models import FileManager
# from config import Config

app = Flask(__name__)
            
# app.config.from_object(Config)

# Répertoire où seront stockés les fichiers partagés


app.debug = True


