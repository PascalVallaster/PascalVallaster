# imports
import binascii
import os
import json
import EnDeCrypt
import ListFileStructure

encrypt_info_file = "~tbl.tbl"
data: dict = {}
is_dir = True


def read_encrypt_info_file(path):
    global data
    data = open(path + os.sep + encrypt_info_file, "r").read().replace("'", "\"")
    data = json.loads(data)


# 279
def read_encrypted_info_data(path):
    global data
    global is_dir
    # data = open(path + os.sep + encrypt_info_file, "r").read().replace("'", "\"")
    data = open(path, "rb").read(279).decode().replace("'", "\"")
    data = json.loads(data)
    is_dir = False


# function for decrypting the passed files
def decryptFiles(Files, path, password, progress_max_signal=None, te_todo_signal=None, pb_progress_signal=None):
    if te_todo_signal and pb_progress_signal:
        te_todo_signal.emit(f"Decrypting content of {str(len(Files))} {'files' if len(Files) > 1 or len(Files) == 0 else 'file'}")
        progress_max_signal.emit(len(Files))
        pb_progress_signal.emit(0)
        value = 1
    try:
        Files = Files.remove(encrypt_info_file)
    except:
        pass

    for file in Files:
        file = path + os.sep + os.path.abspath(file).replace(path + os.sep, "")
        EnDeCrypt.decryptFile(password, file, path, False if not is_dir else True)

        if pb_progress_signal:
            pb_progress_signal.emit(value)
            value += 1
    if pb_progress_signal:
        pb_progress_signal.emit(len(Files))


# function for encrypting the passed filenames
def decryptFileNames(Files, path, private_key, progress_max_signal=None, te_todo_signal=None, pb_progress_signal=None):
    global data
    counter = 0
    # path = os.path.abspath(path)

    if te_todo_signal and pb_progress_signal:
        te_todo_signal.emit(f"Decrypting {str(len(Files[1:] if is_dir else Files))} {'filenames' if len(Files[1:] if is_dir else Files) > 1 or len(Files[1:] if is_dir else Files) == 0 else 'filename'}")
        progress_max_signal.emit(len(Files))
        pb_progress_signal.emit(0)
        value = 1

    for file in Files:
        if os.path.normpath(path + os.sep + encrypt_info_file) in os.path.normpath(os.path.abspath(file)):
            continue
        file = os.path.normpath(os.path.abspath(file)).replace(path + os.sep, "")
        old_path = path + os.sep + file
        new_path = path + os.sep + file.replace(os.path.basename(file), "") + str(
            EnDeCrypt.decryptString(binascii.unhexlify(data[os.path.basename(file)]), private_key))
        os.rename(old_path, new_path)

        if pb_progress_signal:
            pb_progress_signal.emit(value)
            value += 1
        counter += 1

    if is_dir:
        os.remove(path + os.sep + encrypt_info_file)
    else:
        return os.path.basename(new_path)


# function for decrypting the passed foldernames
def decryptFolderNames(Folders, private_key, progress_max_signal=None, te_todo_signal=None, pb_progress_signal=None):
    if te_todo_signal and pb_progress_signal:
        te_todo_signal.emit(f"Decrypting {int(len(Folders[:-1]))} {'foldernames' if len(Folders[:-1]) > 1 or len(Folders[:-1]) == 0 else 'foldername'}")
        progress_max_signal.emit(len(Folders[:-1]))
        pb_progress_signal.emit(0)
        value = 1
    Folders = sorted(Folders, key=len)
    Folders = Folders[1:]
    decryptFolders = []
    for folder in Folders:
        folderpath = os.path.abspath(folder)
        basename = os.path.basename(folderpath)
        folderpath = folderpath.replace(basename, "")
        decryptFolders.append(folderpath + EnDeCrypt.decryptString(binascii.unhexlify(data[basename]), private_key))

    counter = len(Folders) - 1
    while counter >= 0:
        os.rename(Folders[counter], decryptFolders[counter])
        if pb_progress_signal:
            pb_progress_signal.emit(value)
            value += 1
        counter -= 1


if __name__ == '__main__':
    """_path = input("File/Folder to decrypt:")
    password = input("Password:")
    _path = _path.replace('"', "")
    _path = os.path.abspath(_path)
    if os.path.isfile(_path):
        _path = _path.replace(os.sep + os.path.basename(_path), "")
    # read_encrypt_info_file(_path)
    return_tuple = ListFileStructure.list_files(_path)
    decryptFileNames(return_tuple[1], _path, EnDeCrypt.load_private_key())
    if return_tuple[0]:
        decryptFolderNames(return_tuple[0], EnDeCrypt.load_private_key())
    return_tuple = ListFileStructure.list_files(_path)
    decryptFiles(return_tuple[1], _path, password)"""
    pass
