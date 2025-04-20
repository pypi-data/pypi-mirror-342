import logging
from monsterlib import add, subtract

# Config du logger
logging.basicConfig(level=logging.DEBUG, format="🔍 %(message)s")


# 1. Test de base - addition positive
def test_add_simple():
    logging.debug("Test : add(2, 3)")
    result = add(2, 3)
    logging.debug(f"Résultat : {result}")
    assert result == 5


# 2. Test de base - soustraction positive
def test_subtract_simple():
    logging.debug("Test : subtract(10, 4)")
    result = subtract(10, 4)
    logging.debug(f"Résultat : {result}")
    assert result == 6


# 3. Test avec zéro
def test_add_zero():
    logging.debug("Test : add(0, 5)")
    assert add(0, 5) == 5
    logging.debug("Test : subtract(0, 5)")
    assert subtract(0, 5) == -5


# 4. Test avec nombres négatifs
def test_with_negatives():
    logging.debug("Test : add(-2, -3)")
    assert add(-2, -3) == -5
    logging.debug("Test : subtract(-2, -3)")
    assert subtract(-2, -3) == 1


# 5. Test avec des floats
def test_with_floats():
    logging.debug("Test : add(1.5, 2.5)")
    assert add(1.5, 2.5) == 4.0
    logging.debug("Test : subtract(5.5, 2.2)")
    assert subtract(5.5, 2.2) == 3.3


# 6. Bonus : test avec de très grands nombres
def test_large_numbers():
    logging.debug("Test : add(1_000_000_000, 2_000_000_000)")
    assert add(1_000_000_000, 2_000_000_000) == 3_000_000_000
