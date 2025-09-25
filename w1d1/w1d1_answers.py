# %%
import os
import sys
from typing import Generator, List, Tuple, Callable

# Allow imports from parent directory
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from aisb_utils import report


# %%
def lcg_keystream(seed: int) -> Generator[int, None, None]:
    """
    Generate an infinite keystream using a basic LCG.

    Args:
        seed: The starting number for our sequence

    Yields:
        One byte (0-255) at a time from our pseudorandom sequence
    """
    # These are the magic numbers for our LCG formula
    a = 1664525  # multiplier - chosen for good randomness properties
    c = 1013904223  # increment - another carefully chosen constant
    m = 2**32  # modulus - this is 4,294,967,296 (keeps numbers manageable)

    # Start with our seed as the current state
    current_state = seed

    # Generate numbers forever
    while True:
        # Apply the LCG formula: next = (a * current + c) mod m
        current_state = (a * current_state + c) % m

        # We only want the bottom 8 bits (0-255 range)
        # 0xFF in hexadecimal = 255 in decimal = 11111111 in binary
        byte_value = current_state & 0xFF

        # Give back this byte and pause until next request
        yield byte_value


# Test our function
from w1d1_test import test_lcg_keystream

test_lcg_keystream(lcg_keystream)


# %%
# %%
def lcg_encrypt(seed: int, plaintext: bytes) -> bytes:
    """
    Encrypt plaintext using the LCG keystream.

    Args:
        seed: Seed for the keystream generator
        plaintext: The message to encrypt (as bytes)

    Returns:
        Encrypted message (as bytes)
    """
    # Get our keystream generator
    keystream = lcg_keystream(seed)

    # Create a list to hold our encrypted bytes
    encrypted_bytes = []

    # Process each byte of the plaintext
    for plaintext_byte in plaintext:
        # Get the next keystream byte
        keystream_byte = next(keystream)

        # XOR them together
        encrypted_byte = plaintext_byte ^ keystream_byte

        # Add to our result
        encrypted_bytes.append(encrypted_byte)

    # Convert list back to bytes and return
    return bytes(encrypted_bytes)


# Test the encryption function
from w1d1_test import test_encrypt

test_encrypt(lcg_encrypt)


# %%
# %%
def lcg_decrypt(seed: int, ciphertext: bytes) -> bytes:
    """
    Decrypt ciphertext using the same LCG keystream.

    Args:
        seed: Same seed used for encryption
        ciphertext: The encrypted message to decrypt

    Returns:
        Decrypted plaintext (as bytes)
    """
    # Get our keystream generator (same seed as encryption!)
    keystream = lcg_keystream(seed)

    # Create a list to hold our decrypted bytes
    decrypted_bytes = []

    # Process each byte of the ciphertext
    for ciphertext_byte in ciphertext:
        # Get the next keystream byte (same sequence as encryption)
        keystream_byte = next(keystream)

        # XOR them together (this reverses the encryption)
        decrypted_byte = ciphertext_byte ^ keystream_byte

        # Add to our result
        decrypted_bytes.append(decrypted_byte)

    # Convert list back to bytes and return
    return bytes(decrypted_bytes)


# Test the decryption function
from w1d1_test import test_decrypt

test_decrypt(lcg_decrypt)

# Test both functions together
from w1d1_test import test_stream_cipher

test_stream_cipher(lcg_keystream, lcg_encrypt, lcg_decrypt)
