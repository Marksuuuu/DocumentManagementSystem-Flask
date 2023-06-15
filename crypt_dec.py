from cryptography.fernet import Fernet

# Generate a random encryption key
key = Fernet.generate_key()

# Create an instance of the Fernet cipher using the key
cipher = Fernet(key)

# Encrypt a message
message = "W7R25RZqn/UJg".encode()
encrypted_message = cipher.encrypt(message)

# Decrypt the encrypted message
decrypted_message = cipher.decrypt(encrypted_message)

# Print the original and decrypted messages
print("Original Message:", message.decode())
print("Decrypted Message:", decrypted_message.decode())
