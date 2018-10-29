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

    def integrity_check(self, file1, file2):
        with open(file1, "rb") as file:
            data1 = file.read()

        hash1 = self._hash(data1)
        print(hash1)

        with open(file2, "rb") as file:
            hash2 = file.read()
        print(hash2)

        if hash1 == hash2:
            print("Funkcja skrótu odpowiada podanej wartości")
        else:
            print("Funkcja skrótu nie odpowiada podanej wartości")


