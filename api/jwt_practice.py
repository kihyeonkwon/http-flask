import jwt


payload = input()
data_to_encode = {'some':payload}
encryption_secret = 'secrete'
algorithm = 'HS256'
encoded = jwt.encode(data_to_encode, encryption_secret, algorithm=algorithm)
print('encoded : ', encoded)


decoded = jwt.decode(encoded, encryption_secret, algorithms=[algorithm])
print('decoded : ', decoded)
