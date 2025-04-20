import time
import hashlib
from typing import Optional

class BetterRand:
    """
    Chaotic random number generator based on butterfly effect and hashing.
    """

    def __init__(self, seed: Optional[int] = None, r: float = 3.99):
        if seed is None:
            seed = int(time.time() * 1000) & 0xFFFFFFFF
        self.x = ((seed & 0xFFFFFFF) / float(0xFFFFFFF)) * 0.999998 + 1e-6
        self.y = (((seed >> 5) & 0xFFFFFFF) / float(0xFFFFFFF)) * 0.999998 + 1e-6
        self.r = r
        self.counter = 0

    def _logistic_step(self, val: float) -> float:
        return self.r * val * (1 - val)

    def random(self) -> float:
        """
        Return a float random number in [0,1).
        """
        self.x = self._logistic_step(self.x)
        self.y = self._logistic_step(self.y)
        mixed = (self.x + self.y + self.x * self.y) % 1.0
        digest = hashlib.sha256(f"{mixed:.16f}{self.counter}".encode()).hexdigest()
        self.counter += 1
        int_val = int(digest[:16], 16)
        return int_val / float(0xFFFFFFFFFFFFFFFF)

    def randint(self, a: int, b: int) -> int:
        """
        Return a random integer in [a,b].
        """
        return a + int(self.random() * (b - a + 1))