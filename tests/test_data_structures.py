"""
Tests pour Queue et WeatherDict — style pytest
Convention: test_<nom_de_la_fonction_testée>
"""
import pytest

from src.data_structures.queue import Queue
from src.data_structures.weather_dict import WeatherDict


# ── Tests Queue ─────────────────────────────────────────


def test_queue_is_empty():
    """Vérifie qu'une file est vide à la création."""
    queue = Queue()

    assert queue.is_empty() is True
    assert queue.size() == 0


def test_enqueue_dequeue():
    """Vérifie le comportement FIFO : premier entré, premier sorti."""
    queue = Queue()
    queue.enqueue("A")
    queue.enqueue("B")
    queue.enqueue("C")

    assert queue.size() == 3
    assert queue.dequeue() == "A"
    assert queue.dequeue() == "B"
    assert queue.dequeue() == "C"
    assert queue.is_empty() is True


def test_peek():
    """Vérifie que peek retourne le premier élément sans le retirer."""
    queue = Queue()
    queue.enqueue("X")
    queue.enqueue("Y")

    assert queue.peek() == "X"
    assert queue.size() == 2


def test_dequeue_file_vide():
    """Vérifie qu'une erreur est levée si on retire d'une file vide."""
    queue = Queue()

    with pytest.raises(ValueError):
        queue.dequeue()


def test_peek_file_vide():
    """Vérifie qu'une erreur est levée si on consulte une file vide."""
    queue = Queue()

    with pytest.raises(ValueError):
        queue.peek()


def test_queue_iteration():
    """Vérifie qu'on peut itérer sur la file."""
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.enqueue(3)

    assert list(queue) == [1, 2, 3]


# ── Tests WeatherDict ──────────────────────────────────


def test_weather_dict_is_empty():
    """Vérifie qu'un dictionnaire est vide à la création."""
    wd = WeatherDict()

    assert wd.is_empty() is True
    assert wd.size() == 0


def test_put_get():
    """Vérifie l'ajout et la récupération de paires clé-valeur."""
    wd = WeatherDict()
    wd.put("station_42", "données_compans")
    wd.put("station_2", "données_marengo")

    assert wd.get("station_42") == "données_compans"
    assert wd.get("station_2") == "données_marengo"
    assert wd.size() == 2


def test_put_mise_a_jour():
    """Vérifie que put met à jour la valeur si la clé existe déjà."""
    wd = WeatherDict()
    wd.put("station_42", "ancien")
    wd.put("station_42", "nouveau")

    assert wd.get("station_42") == "nouveau"
    assert wd.size() == 1


def test_get_valeur_par_defaut():
    """Vérifie que get retourne la valeur par défaut si clé absente."""
    wd = WeatherDict()

    assert wd.get("inexistant", "défaut") == "défaut"


def test_remove():
    """Vérifie la suppression d'une paire clé-valeur."""
    wd = WeatherDict()
    wd.put("clé", "valeur")

    removed = wd.remove("clé")

    assert removed == "valeur"
    assert wd.is_empty() is True


def test_remove_cle_inexistante():
    """Vérifie qu'une KeyError est levée pour une clé inexistante."""
    wd = WeatherDict()

    with pytest.raises(KeyError):
        wd.remove("inexistant")


def test_contains():
    """Vérifie la recherche de clé."""
    wd = WeatherDict()
    wd.put("présent", True)

    assert wd.contains("présent") is True
    assert wd.contains("absent") is False


def test_keys_values_items():
    """Vérifie les méthodes keys(), values() et items()."""
    wd = WeatherDict()
    wd.put("a", 1)
    wd.put("b", 2)

    assert "a" in wd.keys()
    assert 1 in wd.values()
    assert ("a", 1) in wd.items()


def test_clear():
    """Vérifie que clear vide le dictionnaire."""
    wd = WeatherDict()
    wd.put("a", 1)
    wd.put("b", 2)
    wd.clear()

    assert wd.is_empty() is True
    assert wd.size() == 0
