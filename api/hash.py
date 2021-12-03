import hashlib

m = hashlib.sha256()
m.update(b"testpassword")
value = m.hexdigest()
print(value)
