from EnDeCrypt import encryptStringSymmetrical, decryptStringSymmetrical


def recv_length(client, key) -> int:
    return int(decryptStringSymmetrical(client.recv(100), key))


def send_length(text, client, key) -> None:
    text = text.encode() if type(text) != bytes else text
    client.send(encryptStringSymmetrical(str(len(text)).zfill(10), key))
