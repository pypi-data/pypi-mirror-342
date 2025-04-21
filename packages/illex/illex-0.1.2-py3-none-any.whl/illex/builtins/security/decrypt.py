from cryptography.fernet import Fernet

from illex.decorators.function import function
from illex.decorators.multi_param import multi_param_function


@function("decrypt")
@multi_param_function
def handle_decrypt(text: str, key: str, cipher_type: str = "fernet"):
    def fernet_decrypt(text, key):
        if key is None:
            raise ValueError("A key must be provided for Fernet decryption.")
        try:
            fernet = Fernet(key.encode())
        except Exception as e:
            raise ValueError(
                "Invalid key. The key must be 32 url-safe base64-encoded bytes.") from e

        decrypted_text = fernet.decrypt(text.encode())
        return {"decrypted_text": decrypted_text.decode()}

    def caesar_decrypt(text, key):
        if key is None or not key.isdigit():
            raise ValueError(
                "For Caesar cipher, a numeric key must be provided.")
        shift = int(key)
        return ''.join(
            chr((ord(char) - 65 - shift) % 26 + 65) if char.isupper() else
            chr((ord(char) - 97 - shift) % 26 + 97) if char.islower() else char
            for char in text
        )

    def vigenere_decrypt(text, key):
        if key is None or not key.isalpha():
            raise ValueError(
                "For Vigenère cipher, an alphabetic key must be provided.")
        key = key.lower()
        key_iter = [-(ord(k) - 97) for k in key]
        key_len = len(key_iter)
        decrypted_text = ''.join(
            chr((ord(char) - 65 + key_iter[i % key_len]) % 26 + 65) if char.isupper() else
            chr((ord(char) - 97 + key_iter[i % key_len]) %
                26 + 97) if char.islower() else char
            for i, char in enumerate(text)
        )
        return decrypted_text

    cipher_functions = {
        "fernet": fernet_decrypt,
        "caesar": caesar_decrypt,
        "vigenere": vigenere_decrypt,
    }

    if cipher_type not in cipher_functions:
        raise ValueError(f"Unsupported cipher type: {cipher_type}")

    return cipher_functions[cipher_type](text, key)
