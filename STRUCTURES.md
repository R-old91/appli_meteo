# Documentation des Structures de Données Complexes

Ce document décrit les structures de données personnalisées implémentées dans
l'application météo. Elles se trouvent dans `src/data_structures/`.

---

## 1. Liste Chaînée (LinkedList)

**Fichier :** `src/data_structures/linked_list.py`

### Principe

Une liste chaînée est une structure linéaire où chaque élément (nœud) contient
une donnée et un pointeur vers le nœud suivant. Contrairement aux tableaux,
les éléments ne sont pas stockés de manière contiguë en mémoire.

### Schéma

```
head -> [A|•] -> [B|•] -> [C|None]
```

### Complexité

| Opération | Complexité |
|-----------|-----------|
| `append` (ajout fin) | O(n) |
| `prepend` (ajout début) | O(1) |
| `get(index)` | O(n) |
| `remove_first` | O(1) |
| `size` | O(1) |

### Utilisation dans l'application

- Stocker les données météo d'une station de manière séquentielle
- Fusionner les données existantes avec les mises à jour
- Parcourir les mesures dans l'ordre chronologique

### Exemple

```python
from src.data_structures.linked_list import LinkedList

ll = LinkedList()
ll.append("mesure_1")
ll.append("mesure_2")

for mesure in ll:
    print(mesure)
```

---

## 2. File d'Attente (Queue)

**Fichier :** `src/data_structures/queue.py`

### Principe

Une file d'attente (FIFO : First In, First Out) est une structure où le premier
élément ajouté est le premier retiré. Implémentée ici avec des nœuds chaînés
et un double pointeur (head + tail) pour des opérations en O(1).

### Schéma

```
enqueue ->  [C|•] -> [B|•] -> [A|None]  -> dequeue
(tail)                          (head)
```

### Complexité

| Opération | Complexité |
|-----------|-----------|
| `enqueue` (ajout) | O(1) |
| `dequeue` (retrait) | O(1) |
| `peek` (consultation) | O(1) |
| `size` | O(1) |

### Utilisation dans l'application

- Gérer les requêtes API en file d'attente
- Traiter les demandes de mise à jour dans l'ordre d'arrivée
- Garantir un traitement équitable (premier arrivé, premier servi)

### Exemple

```python
from src.data_structures.queue import Queue

queue = Queue()
queue.enqueue("requete_toulouse")
queue.enqueue("requete_paris")

premiere = queue.dequeue()  # "requete_toulouse"
```

---

## 3. Dictionnaire Personnalisé (WeatherDict)

**Fichier :** `src/data_structures/weather_dict.py`

### Principe

Un dictionnaire (table de hachage) stocke des paires clé-valeur avec un accès
rapide par clé. L'implémentation utilise le **chaînage** pour gérer les
collisions : chaque bucket contient une liste de paires.

### Schéma

```
Index 0: []
Index 1: [(clé_A, valeur_A)]
Index 2: [(clé_B, valeur_B), (clé_C, valeur_C)]  <- collision
Index 3: []
...
```

### Complexité

| Opération | Moyenne | Pire cas |
|-----------|---------|----------|
| `put` (ajout) | O(1) | O(n) |
| `get` (accès) | O(1) | O(n) |
| `remove` (suppression) | O(1) | O(n) |
| `contains` (recherche) | O(1) | O(n) |

### Utilisation dans l'application

- Cache des données météo par station (accès rapide par ID)
- Éviter les requêtes API répétées pour les mêmes données
- Indexer les résultats par nom de ville

### Exemple

```python
from src.data_structures.weather_dict import WeatherDict

cache = WeatherDict()
cache.put("station_42", weather_data)
result = cache.get("station_42")  # Accès O(1)
```

---

## Relations entre les structures

```
┌─────────────┐      ┌──────────┐      ┌──────────────┐
│   Queue     │ ---> │ API Repo │ ---> │  LinkedList   │
│ (Requêtes)  │      │          │      │ (Résultats)   │
└─────────────┘      │          │      └──────────────┘
                     │          │
                     │  Cache   │
                     │    ↓     │
                     │ WeatherDict │
                     └──────────┘
```

1. Les **requêtes** sont mises en file (Queue)
2. L'**APIWeatherRepository** traite chaque requête
3. Les résultats sont stockés en cache (WeatherDict) et retournés comme LinkedList
