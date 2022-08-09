# imports
import os
import sys
import string
import EnDeCrypt
import Data_Encrypter
import Data_Decrypter
import ListFileStructure
from secrets import choice
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from traceback import format_exc
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtWidgets import QDialog, QApplication, QInputDialog


# method for catching and printing out errors
def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


# method for checking the existence of the passed path
def check_existence(path) -> (bool, (bool, bool), bool):
    path_bool = False
    keys_bool = (False, False)
    is_dir = False

    if os.path.isdir(path):
        path_bool, is_dir = True, True
    elif os.path.isfile(path):
        path_bool = True

    if os.path.isfile(key_paths[0]):
        keys_bool = (True, False)
    else:
        keys_bool = (False, False)
    if os.path.isfile(key_paths[1]):
        keys_bool = (keys_bool[0], True)
    else:
        keys_bool = (keys_bool[0], False)

    return path_bool, keys_bool, is_dir


# method for formatting and preparing the raw passed path
def format_path(_path) -> str:
    _path = _path.replace('"', "")
    _path = os.path.abspath(_path)
    return _path


# method for displaying the messagebox for creating new keys
def start_input_dialog_window(self):
    length, _bool = QInputDialog.getInt(self, "Key Length", "Enter length of private key:",
                                        value=1024, min=1024, max=2024, flags=Qt.CustomizeWindowHint)
    if _bool:
        EnDeCrypt.generateKeys(key_len=int(length))


# method for clearing the fields of the En- and Decrypt Window
def clearGuiWindow(input_path, input_password, ):
    input_path.clear()
    input_password.clear()


# class for building and handling the windows of the application
class Windows:
    encrypt_window = None
    decrypt_window = None
    help_window = None
    info_window = None
    error_help_window = None

    def build_main_window(self):
        main_instance.main_window = Main_Window()

    def build_encrypt_window(self):
        self.encrypt_window = Encrypt_Window()

    def build_decrypt_window(self):
        self.decrypt_window = Decrypt_Window()

    def build_help_window(self):
        self.help_window = Help_Window()

    def build_info_window(self):
        self.info_window = Info_Window()

    def build_error_help_window(self):
        self.error_help_window = Error_Help_Window()


# class for encrypting the passed path in a separate thread
class EncryptWorker(QThread):
    progress_max_signal = pyqtSignal(int)
    progressbar_signal = pyqtSignal(int)
    textedit_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int)

    def __init__(self, path, password, is_dir):
        super(EncryptWorker, self).__init__()
        self.path = path
        self.password = password
        self.is_dir = is_dir

    def run(self):
        self.textedit_signal.emit(f"-Encrypting \"{os.path.basename(os.path.abspath(self.path))}\"-")
        try:
            return_tuple = ListFileStructure.list_files(self.path)
            Data_Encrypter.encryptFiles(return_tuple[1], self.path, self.password, self.progress_max_signal,
                                        self.textedit_signal, self.progressbar_signal)
            return_tuple = ListFileStructure.list_files(self.path)
            try:
                Data_Encrypter.encryptFileNames(return_tuple[1], self.path if self.is_dir else os.path.split(os.path.normpath(self.path))[0], EnDeCrypt.load_public_key(),
                                                self.progress_max_signal, self.textedit_signal, self.progressbar_signal)
                if len(return_tuple[0]) > 1:
                    Data_Encrypter.encryptFolderNames(return_tuple[0], EnDeCrypt.load_public_key(),
                                                      self.progress_max_signal, self.textedit_signal,
                                                      self.progressbar_signal)
            except AttributeError:
                self.textedit_signal.emit("<span style=\"color:#aa0000;\">Wrong public-key!</span>")
            except ValueError:
                self.textedit_signal.emit("<span style=\"color:#aa0000;\">Name isn't 128 chars long!</span>")
            else:
                if self.is_dir:
                    Data_Encrypter.write_tbl_file(self.path)
                self.textedit_signal.emit("-Process finished successfully-")
                self.finished_signal.emit(1)
        except:
            with open("error-log.txt", "w") as f:
                f.write(format_exc())
            self.textedit_signal.emit("<span style=\"color:#aa0000;\">!A unknown error occurred and was "
                                      "logged to error-log.txt!</span>")


# class for decrypting the passed path in a separate thread
class DecryptWorker(QThread):
    progress_max_signal = pyqtSignal(int)
    progressbar_signal = pyqtSignal(int)
    textedit_signal = pyqtSignal(str)
    finished_signal = pyqtSignal(int)

    def __init__(self, path, password, is_dir):
        super(DecryptWorker, self).__init__()
        self.path = path
        self.password = password
        self.is_dir = is_dir
        self.new_name = ""

    def run(self):
        self.textedit_signal.emit(f"-Decrypting \"{os.path.basename(os.path.abspath(self.path))}\"-")
        try:
            try:
                if self.is_dir:
                    Data_Decrypter.read_encrypt_info_file(self.path)
                else:
                    Data_Decrypter.read_encrypted_info_data(self.path)
            except FileNotFoundError:
                self.textedit_signal.emit('<span style="color:#aa0000;">File "~tbl.tbl" is missing!</span>')
            else:
                return_tuple = ListFileStructure.list_files(self.path)
                try:
                    self.new_name = Data_Decrypter.decryptFileNames(return_tuple[1],
                                                    self.path if self.is_dir else os.path.split(os.path.normpath(
                                                        self.path))[0], EnDeCrypt.load_private_key(),
                                                    self.progress_max_signal, self.textedit_signal,
                                                    self.progressbar_signal)
                    if len(return_tuple[0]) > 1:
                        Data_Decrypter.decryptFolderNames(return_tuple[0], EnDeCrypt.load_private_key(),
                                                          self.progress_max_signal, self.textedit_signal,
                                                          self.progressbar_signal)
                except AttributeError:
                    self.textedit_signal.emit("<span style=\"color:#aa0000;\">Wrong private-key!</span>")
                except ValueError:
                    self.textedit_signal.emit("<span style=\"color:#aa0000;\">Name isn't 128 chars long!</span>")
                else:
                    return_tuple = ListFileStructure.list_files(self.path if self.is_dir else os.path.split(
                                                                os.path.normpath(self.path))[0] + os.sep + self.new_name)
                    Data_Decrypter.decryptFiles(return_tuple[1],
                                                self.path if self.is_dir else os.path.split(
                                                    os.path.normpath(self.path))[0],
                                                self.password, self.progress_max_signal,
                                                self.textedit_signal, self.progressbar_signal)
                    self.textedit_signal.emit("-Process finished successfully-")
                    self.finished_signal.emit(1)
        except:
            with open("error-log.txt", "w") as f:
                f.write(format_exc())
            self.textedit_signal.emit("<span style=\"color:#aa0000;\">!A unknown error occurred and was "
                                      "written to error-log.txt!</span>")


# class that represents the Main window
class Main_Window(QDialog):
    def __init__(self):
        super(Main_Window, self).__init__()
        loadUi("GUI/main_window.ui", self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.btn_encrypt.clicked.connect(self.start_encrypt_window)
        self.btn_decrypt.clicked.connect(self.start_decrypt_window)
        self.btn_help.clicked.connect(self.start_help_window)
        self.btn_info.clicked.connect(self.start_info_window)
        self.btn_error.clicked.connect(self.start_error_help_window)
        self.btn_generate.clicked.connect(lambda: start_input_dialog_window(self))

    def start_encrypt_window(self):
        window_instance.build_encrypt_window()
        window_instance.encrypt_window.show()
        main_instance.main_window.close()
        window_instance.encrypt_window.exec_()

    def start_decrypt_window(self):
        window_instance.build_decrypt_window()
        window_instance.decrypt_window.show()
        main_instance.main_window.close()
        window_instance.decrypt_window.exec_()

    def start_help_window(self):
        window_instance.build_help_window()
        window_instance.help_window.show()
        main_instance.main_window.close()
        window_instance.help_window.exec_()

    def start_info_window(self):
        window_instance.build_info_window()
        window_instance.info_window.show()
        main_instance.main_window.close()
        window_instance.info_window.exec_()

    def start_error_help_window(self):
        window_instance.build_error_help_window()
        window_instance.error_help_window.show()
        main_instance.main_window.close()
        window_instance.error_help_window.exec_()


# class that represents the Encrypt window
class Encrypt_Window(QDialog):
    def __init__(self):
        super(Encrypt_Window, self).__init__()
        loadUi("GUI/encrypt_window.ui", self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.btn_create_password.setIcon(QIcon("GUI/refresh.png"))
        self.btn_create_password.setIconSize(QSize(25, 27))
        self.btn_back.clicked.connect(self.back)
        self.btn_encrypt.clicked.connect(self.encrypt)
        self.btn_create_password.clicked.connect(self.create_password)
        self.worker = None

    def back(self):
        window_instance.build_main_window()
        main_instance.main_window.show()
        self.close()
        main_instance.main_window.exec_()

    def encrypt(self):
        path = self.input_path.text().replace("\"", "")
        password = self.input_password.text()
        path_exist, keys_exist, is_dir = check_existence(path)
        if not is_dir:
            Data_Encrypter.is_dir = False
        # self.te_todo.append(f"-Encrypting \"{os.path.basename(os.path.abspath(path))}\"-")
        if path_exist and keys_exist[0] and keys_exist[1] and password:
            self.btn_encrypt.setEnabled(False)
            self.btn_back.setEnabled(False)
            path = format_path(path)
            self.te_todo.clear()
            self.worker = EncryptWorker(path, password, is_dir)
            self.worker.start()
            self.worker.finished.connect(lambda: self.btn_encrypt.setEnabled(True))
            self.worker.finished.connect(lambda:self.btn_back.setEnabled(True))
            self.worker.progress_max_signal.connect(lambda value: self.pb_progress.setMaximum(value))
            self.worker.progressbar_signal.connect(lambda value: self.pb_progress.setValue(value))
            self.worker.textedit_signal.connect(lambda value: self.te_todo.append(value))
            self.worker.finished_signal.connect(lambda: clearGuiWindow(self.input_path, self.input_password))
        else:
            if not path_exist:
                self.te_todo.append("<span style=\"color:#aa0000;\">Path is invalid or doesn't exist!</span>")
            elif not keys_exist[0]:
                self.te_todo.append("<span style=\"color:#aa0000;\">\"private_key.key\" not found!</span>")
            elif not keys_exist[1]:
                self.te_todo.append("<span style=\"color:#aa0000;\">\"public_key.key\" not found!</span>")
            else:
                self.te_todo.append("<span style=\"color:#aa0000;\">Field \"Password\" is empty!</span>")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.input_path.setText(file_path)

    def create_password(self):
        chars = string.ascii_letters + string.digits + string.punctuation
        password = ""
        for i in range(0, 11):
            password += choice(chars)
        self.input_password.setText(password)


# class that represents the Decrypt window
class Decrypt_Window(QDialog):
    def __init__(self):
        super(Decrypt_Window, self).__init__()
        loadUi("GUI/decrypt_window.ui", self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.btn_back.clicked.connect(self.back)
        self.btn_decrypt.clicked.connect(self.decrypt)
        self.worker = None

    def back(self):
        window_instance.build_main_window()
        main_instance.main_window.show()
        self.close()
        main_instance.main_window.exec_()

    def decrypt(self):
        path = self.input_path.text().replace("\"", "")
        password = self.input_password.text()
        path_exist, keys_exist, is_dir = check_existence(path)
        # self.te_todo.append(f"-Encrypting {os.path.basename(os.path.abspath(path))}-")
        if path_exist and keys_exist[0] and keys_exist[1] and password:
            self.btn_decrypt.setEnabled(False)
            self.btn_back.setEnabled(False)
            path = format_path(path)
            self.te_todo.clear()
            self.worker = DecryptWorker(path, password, is_dir)
            self.worker.start()
            self.worker.finished.connect(lambda: self.btn_decrypt.setEnabled(True))
            self.worker.finished.connect(lambda: self.btn_back.setEnabled(True))
            self.worker.progress_max_signal.connect(lambda val: self.pb_progress.setMaximum(val))
            self.worker.progressbar_signal.connect(lambda val: self.pb_progress.setValue(val))
            self.worker.textedit_signal.connect(lambda val: self.te_todo.append(val))
            self.worker.finished_signal.connect(lambda: clearGuiWindow(self.input_path, self.input_password))
        else:
            if not path_exist:
                self.te_todo.append("<span style=\"color:#aa0000;\">Path is invalid or doesn't exist!</span>")
            elif not keys_exist[0]:
                self.te_todo.append("<span style=\"color:#aa0000;\">\"private_key.key\" not found!</span>")
            elif not keys_exist[1]:
                self.te_todo.append("<span style=\"color:#aa0000;\">\"public_key.key\" not found!</span>")
            else:
                self.te_todo.append("<span style=\"color:#aa0000;\">Field \"Password\" is empty!</span>")

    def dragEnterEvent(self, event):

        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.input_path.setText(file_path)


# class that represents the Help window
class Help_Window(QDialog):
    def __init__(self):
        super(Help_Window, self).__init__()
        loadUi("GUI/help_window.ui", self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.btn_back.clicked.connect(self.back)

    def back(self):
        window_instance.build_main_window()
        main_instance.main_window.show()
        self.close()
        main_instance.main_window.exec_()


# class that represents the Info window
class Info_Window(QDialog):
    def __init__(self):
        super(Info_Window, self).__init__()
        loadUi("GUI/info_window.ui", self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.btn_back.clicked.connect(self.back)

    def back(self):
        window_instance.build_main_window()
        main_instance.main_window.show()
        self.close()
        main_instance.main_window.exec_()


# class that represents the Error Help window
class Error_Help_Window(QDialog):
    def __init__(self):
        super(Error_Help_Window, self).__init__()
        loadUi("GUI/error_help_window.ui", self)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setWindowFlag(Qt.WindowMinimizeButtonHint, True)
        self.btn_back.clicked.connect(self.back)

    def back(self):
        window_instance.build_main_window()
        main_instance.main_window.show()
        self.close()
        main_instance.main_window.exec_()


# class for starting and initialising the whole application and the Main window
class Main:
    def __init__components__(self):
        global window_instance
        sys.excepthook = except_hook
        window_instance = Windows()
        app = QApplication(sys.argv)
        app.setWindowIcon(QIcon("GUI/icon.png"))
        self.main_window = Main_Window()
        self.main_window.show()
        app.exec_()


# <__name__ == "__main__"> will be executed if the application was started
if __name__ == '__main__':
    key_paths = ["keys/private_key.key", "keys/public_key.key"]
    main_instance = Main()
    main_instance.__init__components__()
