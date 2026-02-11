"""
Liste Chaînée - Structure de données pour stocker les données météo
Principe: Une classe = une responsabilité
"""
from typing import Optional, Any, Iterator


class Node:
    """
    Nœud d'une liste chaînée.

    Responsabilité unique: Représenter un élément de la liste avec son lien vers le suivant.

    Attributes:
        data: Données stockées dans le nœud (ex: WeatherData)
        next: Référence vers le nœud suivant (None si dernier)
    """

    def __init__(self, data: Any):
        """
        Initialise un nœud.

        Args:
            data: Données à stocker dans le nœud
        """
        self.data = data
        self.next: Optional['Node'] = None

    def __str__(self) -> str:
        """Retourne une représentation textuelle du nœud."""
        return f"Node({self.data})"

    def __repr__(self) -> str:
        """Retourne une représentation pour le débogage."""
        next_info = "→ ..." if self.next else "→ None"
        return f"Node({self.data}) {next_info}"


class LinkedList:
    """
    Liste chaînée pour stocker une séquence de données.

    Responsabilité unique: Gérer une collection ordonnée d'éléments avec insertion,
    suppression et parcours.

    Attributes:
        head: Premier nœud de la liste (None si vide)
        _size: Nombre d'éléments dans la liste
    """

    def __init__(self):
        """Initialise une liste chaînée vide."""
        self.head: Optional[Node] = None
        self._size: int = 0

    def is_empty(self) -> bool:
        """
        Vérifie si la liste est vide.

        Returns:
            True si la liste est vide, False sinon
        """
        return self.head is None

    def size(self) -> int:
        """
        Retourne la taille de la liste.

        Returns:
            Nombre d'éléments dans la liste
        """
        return self._size

    def append(self, data: Any) -> None:
        """
        Ajoute un élément à la fin de la liste.

        Args:
            data: Données à ajouter
        """
        new_node = Node(data)

        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node

        self._size += 1

    def prepend(self, data: Any) -> None:
        """
        Ajoute un élément au début de la liste.

        Args:
            data: Données à ajouter
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self._size += 1

    def insert_at(self, index: int, data: Any) -> None:
        """
        Insère un élément à une position spécifique.

        Args:
            index: Position d'insertion (0 = début)
            data: Données à insérer

        Raises:
            IndexError: Si l'index est invalide
        """
        if index < 0 or index > self._size:
            raise IndexError(f"Index {index} hors limites (taille: {self._size})")

        if index == 0:
            self.prepend(data)
            return

        new_node = Node(data)
        current = self.head

        for _ in range(index - 1):
            current = current.next

        new_node.next = current.next
        current.next = new_node
        self._size += 1

    def remove_first(self) -> Any:
        """
        Supprime et retourne le premier élément.

        Returns:
            Données du premier élément

        Raises:
            ValueError: Si la liste est vide
        """
        if self.is_empty():
            raise ValueError("Impossible de supprimer : la liste est vide")

        data = self.head.data
        self.head = self.head.next
        self._size -= 1
        return data

    def remove_at(self, index: int) -> Any:
        """
        Supprime et retourne l'élément à une position spécifique.

        Args:
            index: Position de l'élément à supprimer

        Returns:
            Données de l'élément supprimé

        Raises:
            IndexError: Si l'index est invalide
        """
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} hors limites (taille: {self._size})")

        if index == 0:
            return self.remove_first()

        current = self.head
        for _ in range(index - 1):
            current = current.next

        data = current.next.data
        current.next = current.next.next
        self._size -= 1
        return data

    def get(self, index: int) -> Any:
        """
        Récupère l'élément à une position spécifique.

        Args:
            index: Position de l'élément

        Returns:
            Données de l'élément

        Raises:
            IndexError: Si l'index est invalide
        """
        if index < 0 or index >= self._size:
            raise IndexError(f"Index {index} hors limites (taille: {self._size})")

        current = self.head
        for _ in range(index):
            current = current.next

        return current.data

    def to_list(self) -> list:
        """
        Convertit la liste chaînée en liste Python.

        Returns:
            Liste Python contenant tous les éléments
        """
        result = []
        current = self.head

        while current is not None:
            result.append(current.data)
            current = current.next

        return result

    def clear(self) -> None:
        """Vide complètement la liste."""
        self.head = None
        self._size = 0

    def __iter__(self) -> Iterator:
        """
        Permet d'itérer sur la liste avec une boucle for.

        Returns:
            Itérateur sur les éléments de la liste
        """
        current = self.head
        while current is not None:
            yield current.data
            current = current.next

    def __len__(self) -> int:
        """Retourne la taille de la liste (pour len())."""
        return self._size

    def __str__(self) -> str:
        """Retourne une représentation textuelle de la liste."""
        if self.is_empty():
            return "LinkedList([])"

        elements = [str(data) for data in self]
        return f"LinkedList([{', '.join(elements)}])"

    def __repr__(self) -> str:
        """Retourne une représentation pour le débogage."""
        return f"LinkedList(size={self._size})"
