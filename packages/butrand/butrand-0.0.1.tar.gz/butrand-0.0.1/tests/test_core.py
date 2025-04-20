import pytest
from butrand import BetterRand

def test_random_range():
    rng = BetterRand(seed=2025)
    for _ in range(100):
        val = rng.random()
        assert 0 <= val < 1

def test_randint_range():
    rng = BetterRand(seed=2025)
    for _ in range(100):
        val = rng.randint(10,20)
        assert 10 <= val <= 20