import os, shutil, sys
from config import STATIC_DIR, PUBLIC_DIR

def clear_public_files(public_dir: str):
    
    if not is_valid_directory(public_dir):
        exit(1)

    # 1. Get abs path for directory
    public_dir_abs = os.path.abspath(public_dir) 

    # 2. Get the current directory permissions
    original_stat = os.stat(public_dir_abs)
    original_mode = original_stat.st_mode 
    original_uid = original_stat.st_uid
    original_gid = original_stat.st_gid

    # 3. Delete the directory
    shutil.rmtree(public_dir_abs)

    # 4. Recreate the directory
    os.mkdir(public_dir_abs)

    # 5. Reset/restore permissions
    os.chmod(public_dir_abs, original_mode)
    os.chown(public_dir_abs, original_uid, original_gid)
    

def copy_static_files(public_dir: str, static_dir: str):

    if not is_valid_directory(public_dir) or not is_valid_directory(static_dir):
        exit(1)

    public_dir_abs = os.path.abspath(public_dir) 
    static_dir_abs = os.path.abspath(static_dir)
    shutil.copytree(static_dir_abs, public_dir_abs, dirs_exist_ok=True)

def is_valid_directory(directory: str = ".") -> bool:
    try:
        working_directory_abs = os.path.abspath(".")
        target_directory = os.path.normpath(os.path.join(working_directory_abs, directory))        
        
        if os.path.commonpath([working_directory_abs, target_directory]) != working_directory_abs:
            print(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
            return False       
        
        if not os.path.isdir(target_directory):
            print(f'Error: "{directory}" is not a directory')
            return False
    
        # if we got this far, directory is valid        
        return True

    
    except Exception as e:
        print(f'Error: Encountered problem with "{directory}": {e}')
        return False