from flask import request, render_template, send_from_directory, flash, redirect, url_for
from models import FileManager
import os
from app import app

# Répertoire de bases où seront stockés les fichiers partagés
UPLOAD_FOLDER = '_shared_files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "le reve haitien 777 / REV'HAITIEN"

file_manager = FileManager(UPLOAD_FOLDER)

# @app.route('/confirm', methods=['GET', 'POST'])
# def confirmation():
#     if request.method == 'POST':
#         user_confirmation = request.form.get('confirmation')
#         if user_confirmation == 'TRUE':
#             # Faites l'action que vous souhaitez ici
#             print('==============true')
#         else:
#             print('==============false')

#         return 'yesss is delete'
    
#     return "no isn't delete"

#=========Home URL's=============
@app.route('/folder/')
def index():
    message_class = request.args.get('message_class', 'message')
    return render_template('index.html', current_path='', folders=file_manager.get_folders(''), message_class=message_class)

#=========Create folder URL's=============
@app.route('/create_folder/', methods=['POST'])
def create_folder():
    folder_name = request.form['folder_name']
    current_path = request.form['current_path']
    

    create_folder = file_manager.create_folder(folder_name, current_path)
    
    if create_folder == True:

        flash(f'Folder "{folder_name}" create succesfully', 'success')
        message_class = 'alert-success'
        
        return redirect(url_for('show_files', folder_path=current_path, message_class=message_class))
    
    if create_folder == '2':
        flash(f'Folder "{folder_name}" is yet exist', 'success')
        message_class = 'alert-warning'
        return redirect(url_for('show_files', folder_path=current_path , message_class=message_class))
    
    else:
        flash(f'Folder "{folder_name}" Not create, Try again', 'success')
        message_class = 'alert-warning'
        return redirect(url_for('show_files', folder_path=current_path, message_class=message_class))
    


@app.route('/rem/<path:folder_path>' )
def remove(folder_path):
  
    folder_path = folder_path
    url = folder_path
    url_elements = url.split("/")
    current_path = "/".join(url_elements[:-1])

    print(f'======{current_path}======')

    
    del_folder = file_manager.del_dir(folder_path)
    if del_folder:
        message_class = 'alert-success'
        flash(f'{url_elements} IS DELETED SUCCESFULLY..!')
        return redirect(url_for('show_files', folder_path= current_path, message_class = message_class))
    else:
        message_class = 'alert-warning'
        flash(f'{url_elements} IS DELETED SUCCESFULLY..!')
        return redirect(url_for('show_files', folder_path= current_path, message_class = message_class)) 

    
       

@app.route('/folder/<path:folder_path>')
def show_files(folder_path):
    folders = file_manager.get_folders(folder_path)
    files = file_manager.get_files(folder_path)
    print(f'fffffffffffffff: {folders}')

    if folders == None:
        return 'bad Url'
    
    message_class = request.args.get('message_class', 'message')
    
    return render_template('folder.html', current_path=folder_path, folders=folders, files=files, message_class= message_class)


@app.route('/upload/<path:folder_path>', methods=['POST'])
def upload(folder_path):
    file = request.files['file']
    folder_path = folder_path   
    upload_files = file_manager.upload_file(folder_path, file)

    if upload_files == True:
        flash(f'Files upload succesfully')
        current_path = folder_path
        return redirect(url_for('show_files', folder_path=current_path))
    
    if upload_files == '2':
        flash(f'Please select a file')
        current_path = folder_path
        return redirect(url_for('show_files', folder_path=current_path))
    
    else:
        return 'fuck-off'

@app.route('/shared/<path:folder_path>/<filename>')
def shared_file(folder_path, filename):
    folder_full_path = os.path.join(UPLOAD_FOLDER, folder_path)
    if not os.path.exists(folder_full_path):
        return f"Dossier '{folder_path}' n'existe pas."

    return send_from_directory(folder_full_path, filename)


