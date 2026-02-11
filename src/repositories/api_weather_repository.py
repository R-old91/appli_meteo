"""
APIWeatherRepository - Repository pour l'accès aux données météo via API
Pattern: Repository - Même interface que CSVWeatherRepository
Principe: Open/Closed - Extension sans modification du code existant

Ce module utilise les structures de données personnalisées :
    - WeatherDict: Cache des données par station (accès O(1))
    - Queue: File d'attente des requêtes API
    - LinkedList: Stockage séquentiel des données météo

API utilisée: OpenDataSoft - Toulouse Métropole
URL: https://data.toulouse-metropole.fr/api/explore/v2.1/catalog/datasets/
"""
import json
from datetime import datetime
from typing import List, Optional
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from urllib.parse import urlencode

from ..models.station import Station
from ..models.weather_data import WeatherData
from ..config.config_manager import ConfigManager
from ..data_structures.linked_list import LinkedList
from ..data_structures.queue import Queue
from ..data_structures.weather_dict import WeatherDict
from .weather_repository import WeatherRepository


class APIWeatherRepository(WeatherRepository):
    """
    Repository pour récupérer les données météo via l'API Toulouse Métropole.

    Utilise les structures de données personnalisées :
        - WeatherDict comme cache pour éviter les requêtes répétées
        - Queue pour gérer les requêtes en attente
        - LinkedList pour stocker les résultats

    Attributes:
        _config: Gestionnaire de configuration
        _cache: Cache des données météo (WeatherDict)
        _request_queue: File d'attente des requêtes (Queue)
    """

    def __init__(self):
        """Initialise le repository API avec cache et file d'attente."""
        self._config = ConfigManager()
        self._cache = WeatherDict()
        self._request_queue = Queue()

    def get_all_stations(self) -> List[Station]:
        """
        Retourne les stations configurées pour l'API.

        Returns:
            Liste des stations disponibles
        """
        api_config = self._config.get_api_config()
        stations = []
        for station_cfg in api_config.get("stations", []):
            station = Station(
                id=station_cfg["id"],
                name=station_cfg["name"],
                station_type="API"
            )
            stations.append(station)
        return stations

    def get_weather_data(
        self, station_id: int, limit: int = 10
    ) -> List[WeatherData]:
        """
        Récupère les données météo depuis l'API.

        Vérifie d'abord le cache (WeatherDict). Si les données
        ne sont pas en cache, effectue une requête API.

        Args:
            station_id: ID de la station
            limit: Nombre maximum de résultats

        Returns:
            Liste des données météo
        """
        cache_key = f"station_{station_id}"
        cached = self._cache.get(cache_key)
        if cached is not None:
            print(
                f"  [CACHE] Données en cache pour station {station_id}"
            )
            return cached[:limit]

        data = self._fetch_from_api(station_id, limit)
        if data:
            self._cache.put(cache_key, data)
        return data

    def get_weather_data_as_linked_list(
        self, station_id: int, limit: int = 10
    ) -> LinkedList:
        """
        Retourne les données météo sous forme de liste chaînée.

        Args:
            station_id: ID de la station
            limit: Nombre maximum de résultats

        Returns:
            LinkedList contenant les WeatherData
        """
        data_list = self.get_weather_data(station_id, limit)
        linked_list = LinkedList()
        for data in data_list:
            linked_list.append(data)
        return linked_list

    def enqueue_request(self, station_id: int) -> None:
        """
        Ajoute une requête dans la file d'attente.

        Args:
            station_id: ID de la station à requêter
        """
        self._request_queue.enqueue(station_id)
        print(f"  [QUEUE] Requête ajoutée pour station {station_id}")

    def process_queue(self) -> List[WeatherData]:
        """
        Traite toutes les requêtes en attente dans la file.

        Returns:
            Liste de toutes les données récupérées
        """
        all_data = []
        while not self._request_queue.is_empty():
            station_id = self._request_queue.dequeue()
            print(
                f"  [QUEUE] Traitement requête station {station_id}"
            )
            data = self.get_weather_data(station_id)
            all_data.extend(data)
        return all_data

    def clear_cache(self) -> None:
        """Vide le cache des données météo."""
        self._cache.clear()
        print("  [CACHE] Cache vidé")

    def _fetch_from_api(
        self, station_id: int, limit: int = 10
    ) -> List[WeatherData]:
        """
        Effectue la requête HTTP vers l'API Toulouse Métropole.

        Args:
            station_id: ID de la station
            limit: Nombre de résultats

        Returns:
            Liste des données météo parsées
        """
        api_config = self._config.get_api_config()
        base_url = api_config.get("base_url", "")

        dataset = self._get_dataset(station_id)
        if not dataset:
            print(f"  [API] Station {station_id} non configurée")
            return []

        params = urlencode({
            "limit": limit,
            "order_by": "heure_utc DESC",
            "where": "temperature_en_degre_c > -40",
        })
        url = f"{base_url}/{dataset}/records?{params}"

        try:
            print(f"  [API] Requête: {url}")
            req = Request(
                url, headers={"User-Agent": "MeteoApp/1.0"}
            )
            with urlopen(req, timeout=10) as response:
                raw_data = json.loads(
                    response.read().decode("utf-8")
                )
                return self._parse_api_response(raw_data)
        except HTTPError as err:
            print(f"  [API] Erreur HTTP {err.code}: {err.reason}")
        except URLError as err:
            print(f"  [API] Erreur de connexion: {err.reason}")
        except (json.JSONDecodeError, KeyError) as err:
            print(f"  [API] Erreur de parsing: {err}")

        return []

    def _get_dataset(self, station_id: int) -> Optional[str]:
        """
        Trouve le dataset API pour un ID de station.

        Args:
            station_id: ID de la station

        Returns:
            Nom du dataset ou None
        """
        api_config = self._config.get_api_config()
        for station_cfg in api_config.get("stations", []):
            if station_cfg["id"] == station_id:
                return station_cfg["dataset"]
        return None

    def _parse_api_response(
        self, raw_data: dict
    ) -> List[WeatherData]:
        """
        Parse la réponse de l'API Toulouse Métropole.

        Format attendu (OpenDataSoft):
        {
            "total_count": 140000,
            "results": [
                {
                    "temperature_en_degre_c": 10.6,
                    "humidite": 79,
                    "pression": 98000,
                    "pluie": 0.0,
                    "heure_utc": "2022-12-13T23:30:00+00:00"
                }
            ]
        }

        Args:
            raw_data: Données JSON brutes de l'API

        Returns:
            Liste de WeatherData
        """
        results = raw_data.get("results", [])
        weather_list = []

        for record in results:
            try:
                weather = self._parse_record(record)
                if weather is not None:
                    weather_list.append(weather)
            except (ValueError, TypeError):
                continue

        return weather_list

    def _parse_record(self, record: dict) -> Optional[WeatherData]:
        """
        Parse un enregistrement individuel de l'API.

        Filtre les données aberrantes (température < -40°C).

        Args:
            record: Dictionnaire d'un enregistrement

        Returns:
            WeatherData ou None si données invalides
        """
        temperature = float(record.get("temperature_en_degre_c", 0))

        # Filtrer les données aberrantes
        if temperature < -40:
            return None

        humidity = int(record.get("humidite", 0))
        timestamp_str = record.get("heure_utc", "")
        pressure = int(record.get("pression", 0))
        rain = float(record.get("pluie", 0.0))

        timestamp = datetime.fromisoformat(timestamp_str)

        return WeatherData(
            temperature=temperature,
            humidity=humidity,
            timestamp=timestamp,
            pressure=pressure,
            rain=rain
        )
