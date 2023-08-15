import os
import shutil

class Folder:
    def __init__(self, name, path):
        self.name = name
        self.path = path

class File:
    def __init__(self, name, path):

        self.name = name
        self.path = path

        _, self.file_extension = os.path.splitext(self.name)
        
        # self.types = typess

class FileManager:
    def __init__(self, base_folder):
        self.base_folder = base_folder
        print(f'base folder: {base_folder}')

    def get_folders(self, folder_path):
        folder_full_path = os.path.join(self.base_folder, folder_path)
        print(f'folder path: {folder_path}')
        print(f'folder full  path: {folder_full_path}')
        if not os.path.exists(folder_full_path):
            return None

        folders = [f for f in os.listdir(folder_full_path) if os.path.isdir(os.path.join(folder_full_path, f))]
        return [Folder(name, os.path.join(folder_path, name)) for name in folders]

    def get_files(self, folder_path):
        folder_full_path = os.path.join(self.base_folder, folder_path)
        
        if not os.path.exists(folder_full_path):
            return None

        files = [f for f in os.listdir(folder_full_path) if os.path.isfile(os.path.join(folder_full_path, f))]
        return [File(name, os.path.join(folder_path, name)) for name in files]
    
    def create_folder(self, folder_name, folder_path):
        folder_full_path = os.path.join(self.base_folder, folder_path, folder_name)
        try:
            if  os.path.exists(folder_full_path):
                return '2'
                
            else:
                os.makedirs(folder_full_path)
                return True
                 
        except:
            return False
    
    def del_dir(self, folder_path):
        try:
            del_folder_full_path = os.path.join(self.base_folder, folder_path)
            shutil.rmtree(del_folder_full_path)
            print("Le dossier a été supprimé avec succès.")
            return True
        except OSError as e:
            return False

    def upload_file(self, folder_path, file):
        file = file
        folder_full_path = os.path.join(self.base_folder, folder_path)

        try:

            if not os.path.exists(folder_full_path):
                print ('ooooooooooooooooooooooo')
                print(folder_full_path)
                return '0'
    

            if file.filename == '':
                print('iiiiiiiiiii')
                return "2"

            if file:
                file.save(os.path.join(self.base_folder, folder_path, file.filename))
                return True
            
        except:
            print('yyyyyyyyyyyyyyy')
            return False
            
        

        
        

        



