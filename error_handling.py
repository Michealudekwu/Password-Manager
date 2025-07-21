from cryptography.fernet import Fernet
import json

# key = Fernet.generate_key()
# with open("secret.key", "wb") as enc_file:
#     enc_file.write(key)

with open("secret.key", "rb") as enc_key:
    key = enc_key.read()

fernet = Fernet(key)
#
# with open("data.json", "rb") as file:
#     original_data = file.read()
#
# encrypt = fernet.encrypt(original_data)
#
# with open("Encrypted_data", "wb") as enc_data:
#     enc_data.write(encrypt)

with open("Encrypted_data","rb") as enc_data:
    data = enc_data.read()

dec = fernet.decrypt(data)

