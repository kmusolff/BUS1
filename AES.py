import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding


class AES:

    def __init__(self):
        self.backend = default_backend()

    def load_key(self, size=32):
        self.key = os.urandom(size)

    def load_iv(self, size=16):
        self.iv = os.urandom(size)

    def load_message(self):
        file = open("message.txt", "r")
        message = file.read()
        file.close()
        return message

    def save_cipher(self, message):
        file = open("cipher.txt", "w")
        file.write(message)
        file.close()

    def load_cipher(self):
        file = open("cipher.txt", "r")
        loadedCipher = file.read()
        file.close()
        return loadedCipher

    def save_message(self, message):
        file = open("decrypted_cipher.txt", "w")
        file.write(message)
        file.close()

    def encrypt(self):
        self.load_key()
        self.load_iv()
        message = self.load_message()
        message = message.encode('utf-8', 'strict')
        padder = padding.PKCS7(128).padder()
        padded_message = padder.update(bytes(message))
        print(len(padded_message))
        self.cipher = Cipher(algorithms.AES(self.key), modes.CBC(self.iv), self.backend)
        encryptor = self.cipher.encryptor()
        self.ct = encryptor.update(bytes(str(padded_message), 'utf-8'))
                  #+ encryptor.finalize()
        encryptedMessage = str(self.ct)
        self.save_cipher(encryptedMessage)

    def decrypt(self):
        decryptor = self.cipher.decryptor()
        decrypted_message = decryptor.update(self.ct)
                            #+ decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(decrypted_message)
        self.save_message(str(data))
