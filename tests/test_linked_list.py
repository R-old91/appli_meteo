"""
Tests pour la Liste Chaînée (LinkedList) — style pytest
Convention: test_<nom_de_la_fonction_testée>
"""
import pytest

from src.data_structures.linked_list import Node, LinkedList


# ── Tests Node ──────────────────────────────────────────


def test_node_creation():
    """Vérifie qu'un nœud est créé avec ses données et next à None."""
    node = Node("test")

    assert node.data == "test"
    assert node.next is None


def test_node_chainage():
    """Vérifie que deux nœuds peuvent être chaînés."""
    node1 = Node("premier")
    node2 = Node("second")
    node1.next = node2

    assert node1.next is node2
    assert node1.next.data == "second"


# ── Tests LinkedList ────────────────────────────────────


def test_is_empty():
    """Vérifie qu'une liste est vide à la création."""
    linked = LinkedList()

    assert linked.is_empty() is True
    assert linked.size() == 0


def test_append():
    """Vérifie l'ajout d'éléments à la fin de la liste."""
    linked = LinkedList()
    linked.append("A")
    linked.append("B")
    linked.append("C")

    assert linked.size() == 3
    assert linked.is_empty() is False
    assert linked.get(0) == "A"
    assert linked.get(1) == "B"
    assert linked.get(2) == "C"


def test_prepend():
    """Vérifie l'ajout d'éléments au début de la liste."""
    linked = LinkedList()
    linked.append("B")
    linked.prepend("A")

    assert linked.get(0) == "A"
    assert linked.get(1) == "B"


def test_remove_first():
    """Vérifie la suppression du premier élément."""
    linked = LinkedList()
    linked.append("A")
    linked.append("B")

    removed = linked.remove_first()

    assert removed == "A"
    assert linked.size() == 1
    assert linked.get(0) == "B"


def test_iteration():
    """Vérifie qu'on peut itérer sur la liste avec une boucle for."""
    linked = LinkedList()
    linked.append(1)
    linked.append(2)
    linked.append(3)

    result = list(linked)

    assert result == [1, 2, 3]


def test_to_list():
    """Vérifie la conversion en liste Python."""
    linked = LinkedList()
    linked.append("X")
    linked.append("Y")

    assert linked.to_list() == ["X", "Y"]


def test_get_index_hors_limites():
    """Vérifie qu'un IndexError est levé pour un index invalide."""
    linked = LinkedList()
    linked.append("A")

    with pytest.raises(IndexError):
        linked.get(5)


def test_remove_first_liste_vide():
    """Vérifie qu'un ValueError est levé si on supprime d'une liste vide."""
    linked = LinkedList()

    with pytest.raises(ValueError):
        linked.remove_first()
