# Application Météo 🌤️

Application simple en ligne de commande pour afficher les données de stations météorologiques.

## 📋 Description

Cette application permet de consulter les données météo de deux stations :
- **Station Compans** (ID: 42)
- **Station Marengo** (ID: 2)

Elle affiche la température et l'humidité pour chaque station.

## 🚀 Utilisation

### Lancer l'application

```bash
python main.py
```

### Menu interactif

```
=== Application Météo ===

1. Afficher les stations
2. Afficher les données météo d'une station
3. Quitter
```

### Exemples

**Afficher les stations disponibles** :
- Choisir l'option `1`
- Les stations s'affichent avec leur ID et type

**Afficher les données météo** :
- Choisir l'option `2`
- Entrer l'ID de la station (42 pour Compans, 2 pour Marengo)
- Les 10 dernières mesures s'affichent

## 🏗️ Architecture

L'application utilise une architecture clean code avec plusieurs design patterns :

- **Repository Pattern** : Abstraction de l'accès aux données
- **Factory Pattern** : Création centralisée des objets Station
- **Singleton Pattern** : Gestion unique de la configuration
- **Value Object** : Données météo immuables

## 📁 Structure

```
meteo/
├── data/                   # Fichiers CSV de données
├── src/
│   ├── models/            # Modèles de domaine
│   ├── repositories/      # Accès aux données
│   ├── factories/         # Création d'objets
│   ├── config/            # Configuration
│   └── utils/             # Utilitaires
├── config.json            # Configuration
└── main.py               # Point d'entrée
```

## 🎯 Principes Appliqués

- ✅ **SOLID** : Tous les principes respectés
- ✅ **DRY** : Pas de duplication de code
- ✅ **KISS** : Code simple et lisible
- ✅ **Clean Code** : Nommage explicite, séparation des préoccupations

## 📝 Configuration

Le fichier `config.json` contient :
- Les chemins vers les fichiers de données
- Les informations des stations

Pour ajouter une nouvelle station, modifier ce fichier.

## 🧪 Tests

Pour tester rapidement l'application :

```python
from src.repositories.weather_repository import CSVWeatherRepository

# Créer le repository
repo = CSVWeatherRepository()

# Afficher les stations
stations = repo.get_all_stations()
for s in stations:
    print(s)

# Afficher les données météo
data = repo.get_weather_data(42, limit=5)
for d in data:
    print(d)
```

## 📚 Documentation

- Voir [walkthrough.md](file:///C:/Users/hmahunon/.gemini/antigravity/brain/b63bc5dc-6074-4239-9b0b-fef2f5bb957b/walkthrough.md) pour une documentation complète
- Voir [implementation_plan.md](file:///C:/Users/hmahunon/.gemini/antigravity/brain/b63bc5dc-6074-4239-9b0b-fef2f5bb957b/implementation_plan.md) pour le plan d'implémentation

---

Développé avec les principes du clean code et les design patterns 🎨
