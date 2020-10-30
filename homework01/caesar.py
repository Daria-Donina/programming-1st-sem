import typing as tp


def encrypt_caesar(plaintext: str, shift: int = 3) -> str:
    """
    Encrypts plaintext using a Caesar cipher.

    >>> encrypt_caesar("PYTHON")
    'SBWKRQ'
    >>> encrypt_caesar("python")
    'sbwkrq'
    >>> encrypt_caesar("Python3.6")
    'Sbwkrq3.6'
    >>> encrypt_caesar("")
    ''
    """
    ciphertext = ""

    s_amount = 26
    is_case_changed = False
    for s in plaintext:
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


def decrypt_caesar(ciphertext: str, shift: int = 3) -> str:
    """
    Decrypts a ciphertext using a Caesar cipher.

    >>> decrypt_caesar("SBWKRQ")
    'PYTHON'
    >>> decrypt_caesar("sbwkrq")
    'python'
    >>> decrypt_caesar("Sbwkrq3.6")
    'Python3.6'
    >>> decrypt_caesar("")
    ''
    """
    plaintext = ""

    plaintext = encrypt_caesar(ciphertext, -shift)

    return plaintext


def caesar_breaker_brute_force(ciphertext: str, dictionary: tp.Set[str]) -> int:
    """
    Brute force breaking a Caesar cipher.
    """
    best_shift = 0
    # PUT YOUR CODE HERE
    return best_shift
