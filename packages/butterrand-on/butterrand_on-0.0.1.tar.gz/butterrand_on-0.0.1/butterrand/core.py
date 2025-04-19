import time
import hashlib
from typing import Any, Sequence, List

class BetterButterflyRandom:
    """PRNG dựa trên logistic map với hashing nhẹ."""

    def __init__(self, seed: int = None, r: float = 3.99):
        if seed is None:
            seed = int(time.time() * 1000) & 0xFFFFFFFF
        self.x = ((seed & 0xFFFFFFF) / float(0xFFFFFFF)) * 0.999998 + 1e-6
        self.y = (((seed >> 5) & 0xFFFFFFF) / float(0xFFFFFFF)) * 0.999998 + 1e-6
        self.r = r
        self.counter = 0

    def _logistic_step(self, val: float) -> float:
        return self.r * val * (1 - val)

    def random(self) -> float:
        self.x = self._logistic_step(self.x)
        self.y = self._logistic_step(self.y)
        mixed = (self.x + self.y + self.x * self.y) % 1.0
        self.counter += 1
        digest = hashlib.sha256(f"{mixed:.16f}{self.counter}".encode()).hexdigest()
        int_val = int(digest[:16], 16)
        return int_val / float(0xFFFFFFFFFFFFFFFF)

    def randint(self, a: int, b: int) -> int:
        return a + int(self.random() * (b - a + 1))

    def choice(self, seq: Sequence[Any]) -> Any:
        if not seq:
            raise IndexError("Cannot choose from an empty sequence")
        return seq[self.randint(0, len(seq) - 1)]

    def shuffle(self, seq: List[Any]) -> None:
        for i in reversed(range(1, len(seq))):
            j = self.randint(0, i)
            seq[i], seq[j] = seq[j], seq[i]

    def sample(self, population: Sequence[Any], k: int) -> List[Any]:
        if k > len(population):
            raise ValueError("Sample larger than population")
        pool = list(population)
        self.shuffle(pool)
        return pool[:k]
