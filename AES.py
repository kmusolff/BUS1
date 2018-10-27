import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from PIL import Image
from cryptography.hazmat.primitives import padding

class AES:

	def __init__(self):
		self._key = None
		self._backend = None
		self._mode = None
		self._iv = None		
		self._cipher = None
		
	def prepare_encrypt(self, mode):
		self._key = os.urandom(32)
		self._backend = default_backend()
		self._mode = mode
		if mode == 'CBC':
			self._iv = os.urandom(16)
			print(self._iv)
			self._cipher = Cipher(algorithms.AES(self._key), modes.CBC(self._iv), backend=self._backend)
			print("encrypting CBC...")
		else:
			self._cipher = Cipher(algorithms.AES(self._key), modes.ECB(), backend=self._backend)
			print("encrypting ECB...")

	def prepare_decrypt(self, mode = 'mode', key = 'key', iv = 'iv'):

		#read key from supplied file
		with open(key, 'rb') as file:
			self._key = file.read()

		self._backend = default_backend()
		self._mode = mode
		if mode == 'CBC':
			#read IV from supplied file
			with open(iv, "rb") as file:
				self._iv = file.read()
			print(self._iv)
			self._cipher = Cipher(algorithms.AES(self._key), modes.CBC(self._iv), backend=self._backend)
			print("decrypting CBC...")
		else:
			self._cipher = Cipher(algorithms.AES(self._key), modes.ECB(), backend=self._backend)
			print("decrypting ECB...")

	def _pad(self,message):
		padder = padding.PKCS7(128).padder()
		padded_data = padder.update(message)
		padded_data += padder.finalize()

		return padded_data

	def _unpad(self, message):
		unpadder = padding.PKCS7(128).unpadder()
		unpadded_data = unpadder.update(message) + unpadder.finalize()

		return unpadded_data

	def _encrypt(self, message):
		encryptor = self._cipher.encryptor()
		message = self._pad(message)
		message = encryptor.update(message) + encryptor.finalize()
		return message
		
	#decrypt bytes
	def _decrypt(self, message):
		decryptor = self._cipher.decryptor()
		message = decryptor.update(message) + decryptor.finalize()
		message = self._unpad(message)
		return message

	# prepare encrypted data for Image class
	def _convert_to_RGB(self, data):
		r, g, b = tuple(map(lambda d: [data[i] for i in range(0,len(data)) if i % 3 == d], [0, 1, 2]))
		pixels = tuple(zip(r,g,b))
		return pixels

	def encrypt_image(self, file_in, file_out, data_out = 'data_out', key_out = 'key', iv_out = 'iv'):
		im = Image.open(file_in)
		width, height = im.size
		data = im.convert('RGB').tobytes()

		encrypted_data = self._encrypt(data)

		# write image data for later decryption
		with open(data_out, "wb") as file:
			file.write(encrypted_data)

		wh_out = data_out + '_wh'
		with open(wh_out, 'w') as file:
			file.write(str(width) + ' ' + str(height))
		# edit data for visualisation purposes
		original = len(data)
		encrypted_image = self._convert_to_RGB(encrypted_data[:original])
		
		# save visualisation
		im2 = Image.new(im.mode, im.size)
		im2.putdata(encrypted_image)
		im2.save(file_out)

		#save IV and key
		with open(key_out, 'wb') as file:
			file.write(self._key)
			print("saving key")

		if self._mode == 'CBC':
			with open(iv_out, 'wb') as file:
				file.write(self._iv)


	# decrypt image from saved data
	def decrypt_image(self, data_in, file_out):

		#read encrypted data
		with open(data_in, 'rb') as file:
			encrypted_data = file.read()

		#data decrypted back to Image 
		data = self._decrypt(encrypted_data)

		#read width and height to restore image
		with open(data_in + '_wh', 'r') as file:
			wh = file.read()
			width, height = wh.split(" ")

		im = Image.frombytes('RGB', (int(width), int(height)), data)
		im.save(file_out)


	def encrypt_txt(self, file_in, file_out, key_out='key', iv_out='iv'):
		# load text from file_in
		with open(file_in, 'r') as file:
			text = file.read()

		text = text.encode('utf-8')
		encrypted_text = self._encrypt(text)

		# save encrypted_text to file_out
		with open(file_out, 'wb') as file:
			file.write(encrypted_text)

		# save currently used key to key_out
		with open(key_out, 'wb') as file:
			file.write(self._key)

		# save currently used IV if working as CBC
		if self._mode == 'CBC':
			with open(iv_out, 'wb') as file:
				file.write(self._iv)	

	def decrypt_txt(self, file_in, file_out):
		
		#read encrypted text and decrypt
		with open(file_in, 'rb') as file:
			encrypted_text = file.read()

		text = self._decrypt(encrypted_text).decode('utf-8')

		# write decrypted text to file
		with open(file_out, 'w') as file:
			file.write(text)