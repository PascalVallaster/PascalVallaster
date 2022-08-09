## imports
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from cryptography.fernet import Fernet


chunks = 32 * 1024
base_encoding = "utf-8"
move_number = 2


def generateAsymmetricalKeys(key_len=1024):
    key = RSA.generate(key_len)
    return key, key.publickey()


## This function creates a key for En-/Decrypting the send data (except file-transfer => already encrypted)
def generateSymmetricalKey():
    return Fernet.generate_key()


def import_key(key):
    return RSA.importKey(key)


## encrypts strings that are passed through with the variable private_key
def encryptStringAsymmetrical(string: (str, bytes), public_key):
    encryptObject = PKCS1_OAEP.new(public_key)
    return encryptObject.encrypt(string.encode() if type(string) == str else string)


def decryptStringAsymmetrical(string: bytes, private_key):
    decryptObject = PKCS1_OAEP.new(private_key)
    return decryptObject.decrypt(string).decode()


def encryptStringSymmetrical(string: str, key):
    f = Fernet(key)
    encrypted_string = f.encrypt(string.encode())
    return encrypted_string


def decryptStringSymmetrical(string: bytes, key):
    f = Fernet(key)
    decrypted_string = f.decrypt(string)
    return decrypted_string.decode(base_encoding)


# gets the hashed password for en/decrypting files
def get_key(password) -> bytes:
    hashing = SHA256.new(password.encode(base_encoding))
    return hashing.digest()


if __name__ == '__main__':
    print(encryptStringSymmetrical("0000000000000000", generateSymmetricalKey()))
