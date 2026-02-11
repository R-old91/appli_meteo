"""
Queue (File d'attente) - Structure de données FIFO
Responsabilité unique: Gérer une collection FIFO (First In, First Out)

Utilisation dans l'application: Gestion des requêtes API en file d'attente
pour traiter les demandes de mise à jour dans l'ordre d'arrivée.
"""
from typing import Any, Optional, Iterator

from .linked_list import Node


class Queue:
    """
    File d'attente (FIFO) implémentée avec des nœuds chaînés.

    Responsabilité unique: Gérer une collection ordonnée où le premier
    élément ajouté est le premier retiré (First In, First Out).

    Complexité:
        - enqueue (ajout): O(1) grâce au pointeur tail
        - dequeue (retrait): O(1) grâce au pointeur head
        - peek (consultation): O(1)

    Attributes:
        _head: Premier nœud de la file (celui qui sera retiré en premier)
        _tail: Dernier nœud de la file (le plus récemment ajouté)
        _size: Nombre d'éléments dans la file
    """

    def __init__(self):
        """Initialise une file d'attente vide."""
        self._head: Optional[Node] = None
        self._tail: Optional[Node] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        """
        Vérifie si la file est vide.

        Returns:
            True si la file est vide, False sinon
        """
        return self._head is None

    def size(self) -> int:
        """
        Retourne le nombre d'éléments dans la file.

        Returns:
            Nombre d'éléments
        """
        return self._size

    def enqueue(self, data: Any) -> None:
        """
        Ajoute un élément à la fin de la file.

        Args:
            data: Données à ajouter
        """
        new_node = Node(data)

        if self.is_empty():
            self._head = new_node
            self._tail = new_node
        else:
            self._tail.next = new_node
            self._tail = new_node

        self._size += 1

    def dequeue(self) -> Any:
        """
        Retire et retourne le premier élément de la file.

        Returns:
            Données du premier élément

        Raises:
            ValueError: Si la file est vide
        """
        if self.is_empty():
            raise ValueError("Impossible de retirer : la file est vide")

        data = self._head.data
        self._head = self._head.next

        if self._head is None:
            self._tail = None

        self._size -= 1
        return data

    def peek(self) -> Any:
        """
        Consulte le premier élément sans le retirer.

        Returns:
            Données du premier élément

        Raises:
            ValueError: Si la file est vide
        """
        if self.is_empty():
            raise ValueError("Impossible de consulter : la file est vide")
        return self._head.data

    def __iter__(self) -> Iterator:
        """Permet d'itérer sur la file."""
        current = self._head
        while current is not None:
            yield current.data
            current = current.next

    def __len__(self) -> int:
        """Retourne la taille de la file."""
        return self._size

    def __str__(self) -> str:
        """Retourne une représentation textuelle de la file."""
        if self.is_empty():
            return "Queue([])"
        elements = [str(data) for data in self]
        return f"Queue([{' <- '.join(elements)}])"

    def __repr__(self) -> str:
        """Retourne une représentation pour le débogage."""
        return f"Queue(size={self._size})"
