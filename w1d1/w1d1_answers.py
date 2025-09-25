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
