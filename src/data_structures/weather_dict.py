"""
WeatherDict - Dictionnaire personnalisé (table de hachage)
Responsabilité unique: Stocker et retrouver des données météo par clé

Utilisation dans l'application: Cache de données météo indexé par
identifiant de station pour un accès rapide.
"""
from typing import Any, Optional, List, Tuple, Iterator


class WeatherDict:
    """
    Dictionnaire personnalisé implémenté avec une table de hachage.

    Responsabilité unique: Stocker des paires clé-valeur avec un accès
    rapide par clé, utilisé comme cache de données météo.

    Implémentation:
        - Table de hachage avec chaînage pour gérer les collisions
        - Chaque bucket contient une liste de paires (clé, valeur)
        - Le facteur de charge est surveillé pour le redimensionnement

    Complexité:
        - put (ajout): O(1) en moyenne
        - get (accès): O(1) en moyenne
        - remove (suppression): O(1) en moyenne

    Attributes:
        _capacity: Taille de la table de hachage
        _buckets: Liste de buckets (chaque bucket = liste de paires)
        _size: Nombre de paires clé-valeur stockées
    """

    DEFAULT_CAPACITY = 16

    def __init__(self, capacity: int = DEFAULT_CAPACITY):
        """
        Initialise le dictionnaire.

        Args:
            capacity: Taille initiale de la table de hachage
        """
        self._capacity = capacity
        self._buckets: List[List[Tuple[Any, Any]]] = [
            [] for _ in range(capacity)
        ]
        self._size: int = 0

    def _hash(self, key: Any) -> int:
        """
        Calcule l'index du bucket pour une clé donnée.

        Args:
            key: Clé à hacher

        Returns:
            Index du bucket (entre 0 et capacity - 1)
        """
        return hash(key) % self._capacity

    def put(self, key: Any, value: Any) -> None:
        """
        Ajoute ou met à jour une paire clé-valeur.

        Args:
            key: Clé d'accès
            value: Valeur à stocker
        """
        index = self._hash(key)
        bucket = self._buckets[index]

        # Vérifier si la clé existe déjà
        for i, (existing_key, _) in enumerate(bucket):
            if existing_key == key:
                bucket[i] = (key, value)
                return

        # Nouvelle clé
        bucket.append((key, value))
        self._size += 1

    def get(self, key: Any, default: Optional[Any] = None) -> Any:
        """
        Récupère la valeur associée à une clé.

        Args:
            key: Clé à rechercher
            default: Valeur par défaut si la clé n'existe pas

        Returns:
            Valeur associée à la clé, ou default
        """
        index = self._hash(key)
        bucket = self._buckets[index]

        for existing_key, value in bucket:
            if existing_key == key:
                return value

        return default

    def remove(self, key: Any) -> Any:
        """
        Supprime et retourne la valeur associée à une clé.

        Args:
            key: Clé à supprimer

        Returns:
            Valeur supprimée

        Raises:
            KeyError: Si la clé n'existe pas
        """
        index = self._hash(key)
        bucket = self._buckets[index]

        for i, (existing_key, value) in enumerate(bucket):
            if existing_key == key:
                bucket.pop(i)
                self._size -= 1
                return value

        raise KeyError(f"Clé '{key}' non trouvée")

    def contains(self, key: Any) -> bool:
        """
        Vérifie si une clé existe dans le dictionnaire.

        Args:
            key: Clé à vérifier

        Returns:
            True si la clé existe, False sinon
        """
        index = self._hash(key)
        bucket = self._buckets[index]
        return any(k == key for k, _ in bucket)

    def keys(self) -> List[Any]:
        """Retourne toutes les clés du dictionnaire."""
        result = []
        for bucket in self._buckets:
            for key, _ in bucket:
                result.append(key)
        return result

    def values(self) -> List[Any]:
        """Retourne toutes les valeurs du dictionnaire."""
        result = []
        for bucket in self._buckets:
            for _, value in bucket:
                result.append(value)
        return result

    def items(self) -> List[Tuple[Any, Any]]:
        """Retourne toutes les paires (clé, valeur)."""
        result = []
        for bucket in self._buckets:
            for pair in bucket:
                result.append(pair)
        return result

    def is_empty(self) -> bool:
        """Vérifie si le dictionnaire est vide."""
        return self._size == 0

    def size(self) -> int:
        """Retourne le nombre de paires clé-valeur."""
        return self._size

    def clear(self) -> None:
        """Vide le dictionnaire."""
        self._buckets = [[] for _ in range(self._capacity)]
        self._size = 0

    def __iter__(self) -> Iterator:
        """Itère sur les clés du dictionnaire."""
        for bucket in self._buckets:
            for key, _ in bucket:
                yield key

    def __len__(self) -> int:
        """Retourne la taille du dictionnaire."""
        return self._size

    def __str__(self) -> str:
        """Retourne une représentation textuelle du dictionnaire."""
        pairs = [f"{key}: {value}" for key, value in self.items()]
        return "WeatherDict({" + ", ".join(pairs) + "})"

    def __repr__(self) -> str:
        """Retourne une représentation pour le débogage."""
        return f"WeatherDict(size={self._size}, capacity={self._capacity})"
