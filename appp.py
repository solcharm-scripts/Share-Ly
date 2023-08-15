import os
from flask import Flask, request, render_template, send_from_directory
from models import FileManager

app = Flask(__name__)

# Répertoire où seront stockés les fichiers partagés
UPLOAD_FOLDER = 'shared_files'
file_manager = FileManager(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html', current_path='/', folders=file_manager.get_folders('/'))

@app.route('/create_folder', methods=['POST'])
def create_folder():
    folder_name = request.form['folder_name']
    current_path = request.form['current_path']
    folder_path = os.path.join(current_path, folder_name)
    folder_full_path = os.path.join(UPLOAD_FOLDER, folder_path)
    if not os.path.exists(folder_full_path):
        os.makedirs(folder_full_path)
    return f"Dossier '{folder_name}' créé avec succès."

@app.route('/<path:folder_path>')
def show_files(folder_path):
    folders = file_manager.get_folders(folder_path)
    files = file_manager.get_files(folder_path)
    return render_template('folder.html', current_path=folder_path, folders=folders, files=files)

@app.route('/upload/<path:folder_path>', methods=['POST'])
def upload(folder_path):
    folder_full_path = os.path.join(UPLOAD_FOLDER, folder_path)
    if not os.path.exists(folder_full_path):
        return f"Dossier '{folder_path}' n'existe pas."

    if 'file' not in request.files:
        return "Aucun fichier sélectionné."

    file = request.files['file']
    if file.filename == '':
        return "Aucun fichier sélectionné."

    if file:
        file.save(os.path.join(folder_full_path, file.filename))
        return "Fichier téléchargé avec succès."

@app.route('/shared/<path:folder_path>/<filename>')
def shared_file(folder_path, filename):
    folder_full_path = os.path.join(UPLOAD_FOLDER, folder_path)
    if not os.path.exists(folder_full_path):
        return f"Dossier '{folder_path}' n'existe pas."

    return send_from_directory(folder_full_path, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
