import base64

a2j = 'abcdefghij'

def Int2Char(x: int) -> str:
    """
    Converts an integer to a string using a custom alphabet.
    """
    int_str = str(x)
    int_list = [int(char) for char in int_str]
    char_list = [a2j[num] for num in int_list]
    return ''.join(char_list)

def Char2Int(x: str) -> int:
    """
    Converts a string using a custom alphabet back to an integer.
    """
    int_list = [a2j.index(char) for char in x]
    int_str = ''.join([str(num) for num in int_list])
    return int(int_str)

def encrypt(txt: str) -> str:
    """
    Encrypts a string using base64 encoding.
    """
    encoded_bytes = base64.b64encode(txt.encode('utf-8'))
    encoded_str = encoded_bytes.decode('utf-8').rstrip('=')
    return encoded_str

def decrypt(txt: str) -> str:
    """
    Decrypts a base64 encoded string.
    """
    padding_needed = len(txt) % 4
    if padding_needed != 0:
        txt += '=' * padding_needed
    decoded_bytes = base64.b64decode(txt.encode('utf-8'))
    decoded_str = decoded_bytes.decode('utf-8')
    return decoded_str
