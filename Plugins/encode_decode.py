import base64

# Mapping for integer to character conversion
a2j = 'abcdefghij'

def Int2Char(x: int) -> str:
    """
    Convert an integer to a string using the a2j mapping.
    """
    x_str = str(x)
    int_list = [int(char) for char in x_str]
    char_list = [a2j[digit] for digit in int_list]
    return ''.join(char_list)

def Char2Int(x: str) -> int:
    """
    Convert a string back to an integer using the a2j mapping.
    """
    int_list = [a2j.index(char) for char in x]
    int_str = ''.join([str(digit) for digit in int_list])
    return int(int_str)

def encrypt(txt: str) -> str:
    """
    Encrypt a string using base64 encoding.
    """
    return base64.b64encode(txt.encode('utf-8')).decode('utf-8').rstrip('=')

def decrypt(txt: str) -> str:
    """
    Decrypt a base64 encoded string.
    """
    padding = len(txt) % 4
    if padding != 0:
        txt += '=' * padding
    return base64.b64decode(txt.encode('utf-8')).decode('utf-8')