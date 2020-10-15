def encrypt_vigenere(plaintext: str, keyword: str) -> str:
    """
    Encrypts plaintext using a Vigenere cipher.

    >>> encrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> encrypt_vigenere("python", "a")
    'python'
    >>> encrypt_vigenere("ATTACKATDAWN", "LEMON")
    'LXFOPVEFRNHR'
    """
    ciphertext = ""

    s_amount = 26
    is_case_changed = False

    for s, k in zip(plaintext, extend_keyword(keyword, len(plaintext))):
        shift = ord(k.upper()) - ord('A')
        if ord('A') <= ord(s) <= ord('Z') or ord('a') <= ord(s) <= ord('z'):
            if s.islower():
                s = s.upper()
                is_case_changed = True

            if ord(s) + shift > ord('Z') or ord(s) + shift < ord('A'):
                new_s = chr(ord(s) + shift - s_amount * (shift // abs(shift)))
            else:
                new_s = chr(ord(s) + shift)

            if is_case_changed:
                new_s = new_s.lower()
                is_case_changed = False
            s = new_s
        ciphertext += s

    return ciphertext


def extend_keyword(keyword, length):
    string = keyword * (length // len(keyword)) + keyword[:length % len(keyword)]
    return string


def decrypt_vigenere(ciphertext: str, keyword: str) -> str:
    """
    Decrypts a ciphertext using a Vigenere cipher.

    >>> decrypt_vigenere("PYTHON", "A")
    'PYTHON'
    >>> decrypt_vigenere("python", "a")
    'python'
    >>> decrypt_vigenere("LXFOPVEFRNHR", "LEMON")
    'ATTACKATDAWN'
    """
    plaintext = ""

    s_amount = 26
    is_case_changed = False

    for s, k in zip(ciphertext, extend_keyword(keyword, len(ciphertext))):
        shift = -(ord(k.upper()) - ord('A'))
        if ord('A') <= ord(s) <= ord('Z') or ord('a') <= ord(s) <= ord('z'):
            if s.islower():
                s = s.upper()
                is_case_changed = True

            if ord(s) + shift > ord('Z') or ord(s) + shift < ord('A'):
                new_s = chr(ord(s) + shift - s_amount * (shift // abs(shift)))
            else:
                new_s = chr(ord(s) + shift)

            if is_case_changed:
                new_s = new_s.lower()
                is_case_changed = False
            s = new_s
        plaintext += s

    return plaintext
