import random
import string
from Crypto.Cipher import AES, Blowfish
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import Twofish
from Crypto.Random import get_random_bytes
from hashlib import sha256

class AESY:
    def __init__(self):
        # Sabit şifreyi burada tanımlıyoruz
        self.password = "eutybsiniriosetbytiornioebtyerteurcbieurtytieyersioesnutseiersnbuotriesvyortotvvvvvvvvvvvvvvvvvvvvvvvvvvvvvrsdknrkyxvrtkxtzvybbbbbbbbbzryjtzjykrbvzrtyrbytzbgvrbryuzyncucnunutvnudt"
        
        # Şifreyi SHA256 ile hash'liyoruz ve AES için anahtar olarak kullanıyoruz
        self.key = sha256(self.password.encode()).digest()
        self.rsa_key = RSA.generate(2048)
        self.rsa_cipher = PKCS1_OAEP.new(self.rsa_key)

    def encrypt_aes(self, data: bytes) -> bytes:
        cipher = AES.new(self.key, AES.MODE_EAX)
        ciphertext, tag = cipher.encrypt_and_digest(data)
        return cipher.nonce + tag + ciphertext

    def decrypt_aes(self, data: bytes) -> bytes:
        nonce = data[:16]
        tag = data[16:32]
        ciphertext = data[32:]
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag)

    def encrypt_blowfish(self, data: bytes) -> bytes:
        cipher = Blowfish.new(self.key, Blowfish.MODE_ECB)
        plen = 8 - len(data) % 8
        padding = bytes([plen]) * plen
        return cipher.encrypt(data + padding)

    def decrypt_blowfish(self, data: bytes) -> bytes:
        cipher = Blowfish.new(self.key, Blowfish.MODE_ECB)
        decrypted = cipher.decrypt(data)
        plen = decrypted[-1]
        return decrypted[:-plen]

    def encrypt_twofish(self, data: bytes) -> bytes:
        cipher = Twofish.new(self.key)
        plen = 16 - len(data) % 16
        padding = bytes([plen]) * plen
        return cipher.encrypt(data + padding)

    def decrypt_twofish(self, data: bytes) -> bytes:
        cipher = Twofish.new(self.key)
        decrypted = cipher.decrypt(data)
        plen = decrypted[-1]
        return decrypted[:-plen]

    def encrypt_rsa(self, data: bytes) -> bytes:
        return self.rsa_cipher.encrypt(data)

    def decrypt_rsa(self, data: bytes) -> bytes:
        return self.rsa_cipher.decrypt(data)

    def caesar_cipher(self, data: str, shift: int = 7) -> str:
        result = []
        for char in data:
            if char.isalpha():
                shift_base = 65 if char.isupper() else 97
                result.append(chr((ord(char) - shift_base + shift) % 26 + shift_base))
            else:
                result.append(char)
        return ''.join(result)

    def to_lower_case(self, data: str) -> str:
        return data.lower()

    def replace_numbers(self, data: str) -> str:
        symbols = ['#', '$', '%', '&']
        result = []
        for char in data:
            if char.isdigit():
                num = int(char)
                symbol = symbols[num % len(symbols)]
                result.append(symbol * num)
            else:
                result.append(char)
        return ''.join(result)

    def generate_seed(self, seed_length: int) -> str:
        # Generate a random seed of the requested length
        seed = ''.join(random.choices(string.ascii_letters + string.digits, k=seed_length))
        return seed

    def encrypt(self, message: str, seed_length: int = 128) -> str:
        # Encrypt the message with AESY encryption algorithm

        # Ensure seed_length is provided, otherwise set it to 128 by default
        if not seed_length:
            seed_length = 128

        # Convert message to bytes
        data = message.encode()

        # Apply AES, RSA, Blowfish, Twofish encryption
        aes_encrypted = self.encrypt_aes(data)
        rsa_encrypted = self.encrypt_rsa(aes_encrypted)
        blowfish_encrypted = self.encrypt_blowfish(rsa_encrypted)
        twofish_encrypted = self.encrypt_twofish(blowfish_encrypted)

        # Apply Caesar Cipher
        shifted = self.caesar_cipher(twofish_encrypted.decode('latin-1', errors='ignore'))

        # Convert the text to lowercase
        lowered = self.to_lower_case(shifted)

        # Replace numbers with symbols
        final = self.replace_numbers(lowered)

        # Generate the seed and append it to the encrypted message
        seed = self.generate_seed(seed_length)

        # Return the final encrypted message with seed
        return final + "%&&%" + seed

    def decrypt(self, encrypted_message: str) -> str:
        # Decrypt the message with AESY decryption algorithm

        # Separate the encrypted message and seed
        encrypted_data, seed = encrypted_message.split("%&&%")

        # Reverse the transformations
        replaced = self.replace_numbers(encrypted_data)
        original_case = self.to_lower_case(replaced)
        reverted = self.caesar_cipher(original_case.upper(), -7)

        # Convert back to bytes
        ciphertext_bytes = reverted.encode('latin-1')

        # Apply layered decryption: Twofish, Blowfish, RSA, AES
        decrypted_twofish = self.decrypt_twofish(ciphertext_bytes)
        decrypted_blowfish = self.decrypt_blowfish(decrypted_twofish)
        decrypted_rsa = self.decrypt_rsa(decrypted_blowfish)
        decrypted_aes = self.decrypt_aes(decrypted_rsa)

        return decrypted_aes.decode()
