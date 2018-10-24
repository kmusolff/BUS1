import hashlib

class Integrity:
	def __init__(self):
		pass

	def _hash(self, bytes):
		hash_obj = hashlib.sha3_256()
		hash_obj.update(bytes)
		return hash_obj.digest()

	def hash_file(self, file_from):
		with open(file_from, "rb") as file:
			data = file.read()

		return self._hash(data)

	def hash_to_file(self, file_from, file_to):

		hashed_file = self.hash_file(file_from)

		with open(file_to, "wb") as file:
			file.write(hashed_file)


	def integrity_check(file1, file2):
		return self.hash_file(file1) == self.hash_file(file2)



