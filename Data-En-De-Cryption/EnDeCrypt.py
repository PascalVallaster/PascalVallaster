## imports
import os
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


chunks = 32 * 1024
base_encoding = "utf-8"
move_number = 2


def generateKeys(base_path="keys/", key_len=1024):
    if not os.path.isdir(base_path):
        os.mkdir(base_path)
    key = RSA.generate(key_len)
    open(base_path + "private_key.key", "wb").write(key.exportKey())
    open(base_path + "public_key.key", "wb").write(key.publickey().exportKey())


def load_private_key(base_path="keys/"):
    return RSA.importKey(open(base_path + "private_key.key", "rb").read())


def load_public_key(base_path="keys/"):
    return RSA.importKey(open(base_path + "public_key.key", "rb").read())


## encrypts strings that are passed through with the variable private_key
def encryptString(string: str, public_key):
    encryptObject = PKCS1_OAEP.new(public_key)
    return encryptObject.encrypt(string.encode())


def decryptString(string: bytes, private_key):
    decryptObject = PKCS1_OAEP.new(private_key)
    return decryptObject.decrypt(string).decode()


# encrypts a file <filename> with the <key> that is passed through and saves it as files/encrypted-<filename>
def encryptFile(key, filename, path, encryptedFileNames=None):
    if encryptedFileNames:
        encryptedFileNames = str(encryptedFileNames).encode(base_encoding)
    key = get_key(key)
    out_file_name = path + os.sep + "encrypted-" + os.path.basename(filename)
    file_size = str(os.path.getsize(filename)).zfill(16)
    IV = Random.new().read(16)
    encryptor = AES.new(key, AES.MODE_CFB, IV)
    with open(filename, 'rb') as f_input:
        with open(out_file_name, 'wb') as f_output:
            if encryptedFileNames:
                f_output.write(encryptedFileNames)
            f_output.write(file_size.encode(base_encoding))
            f_output.write(IV)
            while True:
                chunk = f_input.read(chunks)
                if len(chunk) == 0:
                    break
                if len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - (len(chunk) % 16))
                f_output.write(encryptor.encrypt(chunk))
    try:
        os.remove(filename)
    except IOError:
        print(f"No permission to delete File: {filename}")


# decrypts a file <filename> with the <key> that is passed through
def decryptFile(key, filename, path, is_dir=True):
    key = get_key(key)
    out_file_name = path + os.sep + os.path.basename(filename).replace("encrypted-", "")
    with open(filename, 'rb') as f_input:
        if not is_dir:
            f_input.seek(279)
        filesize = int(f_input.read(16))
        IV = f_input.read(16)
        decryptor = AES.new(key, AES.MODE_CFB, IV)
        with open(out_file_name, 'wb') as f_output:
            while True:
                chunk = f_input.read(chunks)
                if len(chunk) == 0:
                    break
                f_output.write(decryptor.decrypt(chunk))
                f_output.truncate(filesize)
        f_input.close()
        f_input.close()
    try:
        os.remove(filename)
    except IOError:
        pass
    # return out_file_name


# gets the hashed password for en/decrypting files
def get_key(password) -> bytes:
    hashing = SHA256.new(password.encode(base_encoding))
    return hashing.digest()


if __name__ == '__main__':
    # encryptFile("pass", r"path", r"path")
    print(encryptString("a" * 86, load_public_key()))
    input()
