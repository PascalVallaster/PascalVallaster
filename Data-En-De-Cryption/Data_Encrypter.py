# imports
import os
import binascii
import EnDeCrypt
import ListFileStructure
from secrets import choice

encrypt_info_file = "~tbl.tbl"
encryptedFileNames = {}
FileNames = []
numbers = "0123456789"
is_dir = True
create_dictionary = False
encrypted_string = ""


def write_tbl_file(path):
    open(path + os.sep + encrypt_info_file, "w").write(str(encryptedFileNames))


# function for encrypting the passed files
def encryptFiles(Files, path, password, progress_max_signal=None, te_todo_signal=None, pb_progress_signal=None):
    global create_dictionary
    if te_todo_signal and pb_progress_signal:
        te_todo_signal.emit(f"Encrypting content of {str(len(Files))} {'files' if len(Files) > 1 or len(Files) == 0 else 'file'}")
        progress_max_signal.emit(len(Files))
        pb_progress_signal.emit(0)
        value = 1
    for file in Files:
        if is_dir:
            file = path + os.sep + os.path.abspath(file).replace(path + os.sep, "")
        if not is_dir:
            create_dictionary = True
            new_Files = Files[0]
            p, f = os.path.split(new_Files)
            new_Files = [p + os.sep + "encrypted-" + f]
            encryptFileNames(new_Files,os.path.split(os.path.normpath(path))[0], EnDeCrypt.load_public_key())
        EnDeCrypt.encryptFile(password, file, path if is_dir else os.path.split(os.path.normpath(path))[0],
                              encryptedFileNames if not is_dir else None)

        if pb_progress_signal:
            pb_progress_signal.emit(value)
            value += 1


# function for encrypting the passed filenames
def encryptFileNames(Files, path, public_key, progress_max_signal=None, te_todo_signal=None, pb_progress_signal=None):
    global encryptedFileNames
    global FileNames
    global create_dictionary
    global encrypted_string
    path = os.path.abspath(path)

    if te_todo_signal and pb_progress_signal:
        te_todo_signal.emit(f"Encrypting {str(len(Files))} {'filenames' if len(Files) > 1 or len(Files) == 0 else 'filename'}")
        progress_max_signal.emit(len(Files))
        pb_progress_signal.emit(0)
        value = 1

    for file in Files:
        if os.path.normpath(path + os.sep + encrypt_info_file) in os.path.normpath(os.path.abspath(file)):
            continue
        file = os.path.normpath(os.path.abspath(file)).replace(path + os.sep, "")
        old_path = path + os.sep + file
        if create_dictionary or is_dir:
            while True:
                encrypted_string = ""
                for i in range(1, 16):
                    encrypted_string += choice(numbers)
                if encrypted_string not in FileNames:
                    FileNames.append(encrypted_string)
                    break
        encryptedFileNames[FileNames[-1]] = binascii.hexlify(
            EnDeCrypt.encryptString(os.path.basename(file), public_key)).decode()
        new_path = path + os.sep + file.replace(os.path.basename(file), "") + FileNames[-1]
        if not create_dictionary:
            os.rename(old_path, new_path)
        else:
            create_dictionary = False

        if pb_progress_signal:
            pb_progress_signal.emit(value)
            value += 1


# function for encrypting the passed foldernames
def encryptFolderNames(folders, public_key, progress_max_signal=None, te_todo_signal=None, pb_progress_signal=None):
    global encryptedFileNames
    local_FileNames = []

    if te_todo_signal and pb_progress_signal:
        te_todo_signal.emit(f"Encrypting {int(len(folders[:-1]))} {'foldernames' if len(folders[:-1]) > 1 or len(folders[:-1]) == 0 else 'foldername'}")
        progress_max_signal.emit(len(folders[:-1]))
        pb_progress_signal.emit(0)
        value = 1
    folders = sorted(folders, key=len)
    folders = folders[1:]
    encryptFolders = []
    for folder in folders:
        folderpath = os.path.abspath(folder)
        basename = os.path.basename(folderpath)
        folderpath = folderpath.replace(basename, "")
        while True:
            encrypted_string = ""
            for i in range(1, 16):
                encrypted_string += choice(numbers)
            if encrypted_string not in FileNames:
                local_FileNames.append(encrypted_string)
                break
        encryptedFileNames[local_FileNames[-1]] = binascii.hexlify(
            EnDeCrypt.encryptString(basename, public_key)).decode()
        encryptFolders.append(folderpath + local_FileNames[-1])

    counter = len(folders) - 1
    while counter >= 0:
        os.rename(folders[counter], encryptFolders[counter])
        if pb_progress_signal:
            pb_progress_signal.emit(value)
            value += 1
        counter -= 1

    if pb_progress_signal:
        pb_progress_signal.emit(len(folders))


# open(path + os.sep + encrypt_info_file, "w").write(str(encryptedFileNames))
if __name__ == '__main__':
    """_path = input("File/Folder to encrypt:")
    password = input("Password:")
    _path = _path.replace('"', "")
    _path = os.path.abspath(_path)
    if os.path.isfile(_path):
        _path = _path.replace(os.sep + os.path.basename(_path), "")
    return_tuple = ListFileStructure.list_files(_path)
    encryptFiles(return_tuple[1], _path, password)
    return_tuple = ListFileStructure.list_files(_path)
    encryptFileNames(return_tuple[1], _path, EnDeCrypt.load_public_key())
    if return_tuple[0]:
        encryptFolderNames(return_tuple[0], EnDeCrypt.load_public_key())
    open(path + os.sep + encrypt_info_file, "w").write(str(encryptedFileNames))"""
    pass
