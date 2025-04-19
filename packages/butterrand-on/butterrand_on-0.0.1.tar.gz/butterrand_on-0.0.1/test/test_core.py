from butterrand.core import BetterButterflyRandom

def test_random_range():
    rng = BetterButterflyRandom(seed=123)
    for _ in range(100):
        assert 0 <= rng.random() < 1

def test_randint_range():
    rng = BetterButterflyRandom(seed=123)
    for _ in range(100):
        v = rng.randint(10, 20)
        assert 10 <= v <= 20

def test_choice():
    rng = BetterButterflyRandom(seed=123)
    items = ['A', 'B', 'C']
    for _ in range(10):
        assert rng.choice(items) in items

def test_sample():
    rng = BetterButterflyRandom(seed=123)
    result = rng.sample(range(100), 5)
    assert len(result) == 5
    assert len(set(result)) == 5
