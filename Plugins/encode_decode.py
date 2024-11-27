import base64

# Alphabet for encoding
a2j = 'abcdefghij'

# Convert integer to string of characters
def Int2Char(x: int) -> str:
    return ''.join([a2j[int(digit)] for digit in str(x)])

# Convert string of characters back to integer
def Char2Int(x: str) -> int:
    return int(''.join([str(a2j.index(char)) for char in x]))

# Encrypt the string using base64 encoding
def encrypt(txt: str) -> str:
    return base64.b64encode(txt.encode('utf-8')).decode('utf-8').rstrip('=')

# Decrypt the string using base64 decoding
def decrypt(txt: str) -> str:
    txt = txt + '=' * (4 - len(txt) % 4)  # Padding the string to ensure it's a multiple of 4
    return base64.b64decode(txt.encode('utf-8')).decode('utf-8')

# Example usage
if __name__ == "__main__":
    original = "hello"
    encrypted = encrypt(original)
    decrypted = decrypt(encrypted)

    print(f"Original: {original}")
    print(f"Encrypted: {encrypted}")
    print(f"Decrypted: {decrypted}")

    # Testing Int2Char and Char2Int
    num = 123
    char = Int2Char(num)
    restored_num = Char2Int(char)

    print(f"Number: {num} -> Char: {char} -> Restored Number: {restored_num}")
