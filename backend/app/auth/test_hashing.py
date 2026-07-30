from security import hash_password, verify_password

password = "Atlas@123"

hashed = hash_password(password)

print(hashed)

print(verify_password(password, hashed))
print(verify_password("wrong-password", hashed))