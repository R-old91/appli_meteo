# Application Météo

Application en ligne de commande pour afficher et gérer les données météorologiques.

## Installation

```bash
# Cloner le projet
git clone <url-du-repo>
cd appli_meteo

# Créer et activer l'environnement virtuel
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Linux/Mac

# Installer les dépendances
pip install -r requirements.txt
```

## Lancer l'application

```bash
# Activer le venv si pas déjà fait
venv\Scripts\activate        # Windows

# Lancer
python main.py
```

## Lancer les tests

```bash
# Tous les tests
python -m unittest discover -s tests -v

# Un fichier spécifique
python -m unittest tests.test_models -v
```


## Installation avec Docker

Vous pouvez également lancer l'application via Docker sans installer Python localement.

```bash
# Construire l'image
docker build -t meteo-app .

# Lancer le conteneur (mode interactif)
docker run -it --rm meteo-app
```

## Vérifier le code avec pylint

```bash
python -m pylint src/ main.py
```

## Menu de l'application

```
1. Afficher les stations (CSV)
2. Afficher les données météo d'une station (CSV)
3. Afficher les données météo avec liste chaînée
4. Mettre à jour les données d'une station (CSV)
5. Météo en ligne (API)
6. Rafraîchir les données API
7. Quitter
```

## Structure du Projet

```
meteo/
├── main.py                    # Point d'entrée
├── config.json                # Configuration (stations, API)
├── README.md                  # Documentation d'utilisation
├── STRUCTURES.md              # Documentation des structures de données
├── data/
│   ├── meteo_compans.csv      # Données station Compans
│   ├── meteo_marengo.csv      # Données station Marengo
│   ├── update_compans.csv     # Données fictives pour mise à jour
│   └── update_marengo.csv     # Données fictives pour mise à jour
├── src/
│   ├── config/
│   │   └── config_manager.py  # Singleton de configuration
│   ├── data_structures/
│   │   ├── linked_list.py     # Liste chaînée (LinkedList)
│   │   ├── queue.py           # File d'attente (Queue, FIFO)
│   │   └── weather_dict.py    # Dictionnaire personnalisé (table de hachage)
│   ├── factories/
│   │   └── station_factory.py # Factory de stations
│   ├── models/
│   │   ├── station.py         # Modèle Station
│   │   └── weather_data.py    # Value Object WeatherData
│   ├── repositories/
│   │   ├── weather_repository.py     # Repository CSV (abstrait + concret)
│   │   └── api_weather_repository.py # Repository API
│   ├── services/
│   │   └── weather_updater.py # Service de mise à jour
│   └── utils/
│       └── csv_reader.py      # Utilitaire de lecture CSV
└── tests/
    ├── test_models.py         # Tests des modèles
    ├── test_linked_list.py    # Tests de la liste chaînée
    ├── test_data_structures.py # Tests Queue + WeatherDict
    └── test_repository.py     # Tests du repository + updater
```

## Jeu de Données

### Sources CSV

Les fichiers CSV sont séparés par `;` et contiennent les colonnes suivantes :

| Colonne | Type | Description |
|---------|------|-------------|
| `data` | string | Identifiant unique de la mesure |
| `id` | int | ID de la station |
| `humidite` | int | Humidité en % (0-100) |
| `temperature` | float | Température en °C |
| `pression` | int | Pression en Pa |
| `pluie` | float | Quantité de pluie en mm |
| `heure_de_paris` | datetime | Horodatage (fuseau Paris) |
| `heure_utc` | datetime | Horodatage UTC |
| `type_de_station` | string | Type de station (ISS) |

### Stations disponibles

| ID | Nom | Fichier CSV | Fichier Update |
|----|-----|-------------|----------------|
| 42 | Compans | `meteo_compans.csv` | `update_compans.csv` |
| 2 | Marengo | `meteo_marengo.csv` | `update_marengo.csv` |

### API en ligne (Toulouse Métropole)

L'application récupère les données météo en temps réel via l'API OpenDataSoft
de Toulouse Métropole. Cette API est **publique** et ne nécessite **pas de clé API**.

- **URL** : `https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets`
- **Dataset** : `01-station-meteo-toulouse-meteopole`
- **Station configurée** : Toulouse Météopole (ID: 1)

Les données retournées incluent : `temperature_en_degre_c`, `humidite`,
`pression`, `pluie`, `heure_utc`.

Pour ajouter d'autres stations, modifier la section `api.stations` dans `config.json`.

## Design Patterns

1. **Repository Pattern** : Abstraction de l'accès aux données
   (`CSVWeatherRepository`, `APIWeatherRepository`)
2. **Factory Pattern** : Création centralisée des objets Station
   (`StationFactory`)
3. **Singleton Pattern** : Instance unique de configuration
   (`ConfigManager`)

## Principes Clean Code

- **SOLID** : Chaque classe a une responsabilité unique
- **DRY** : Fonctions réutilisables (`csv_reader`, `ConfigManager`)
- **KISS** : Code simple et lisible
- **YAGNI** : Pas de fonctionnalité inutile
- **PEP 8** : Conventions Python respectées
- **Pylint** : Score 9.87/10 (config dans `.pylintrc`)
