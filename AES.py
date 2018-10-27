import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

from cryptography.hazmat.primitives import padding

class AES:

	def __init__(self, mode='CBC'):
		self._key = os.urandom(32)
		self._backend = default_backend()
		if mode == 'CBC':
			self._iv = os.urandom(16)
			self._cipher = Cipher(algorithms.AES(self._key), modes.CBC(self._iv), backend=self._backend)
		else:
			self._cipher = Cipher(algorithms.AES(self._key), modes.ECB(), backend=self._backend)
		

	def _pad(self,message):
		padder = padding.PKCS7(128).padder()
		padded_data = padder.update(message.encode('utf-8'))
		padded_data += padder.finalize()

		return padded_data

	def _unpad(self, message):
		unpadder = padding.PKCS7(128).unpadder()
		unpadded_data = unpadder.update(message) + unpadder.finalize()

		return unpadded_data.decode('utf-8')

	def encrypt(self):
		encryptor = self._cipher.encryptor()
		self._message = self._pad(self._message)
		self._message = encryptor.update(self._message) + encryptor.finalize()
		self.writeCipher(self._message)
		

	def decrypt(self):
		decryptor = self._cipher.decryptor()
		self._message = decryptor.update(self._message) + decryptor.finalize()
		self._message = self._unpad(self._message)
		self.writeDecryptedMessage()
		return self._message

	def readMessage(self):
		with open("message.txt", "r") as file:
	  		self._message = file.read()		

	def writeCipher(self, msg):
		with open("cipher.txt", "wb") as file:
	  		file.write(msg)

	def writeDecryptedMessage(self):
		with open("decrypted_message.txt", "w") as file:
			file.write(self._message)	







