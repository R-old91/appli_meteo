"""
WeatherRepository - Repository pour l'accès aux données météo
Pattern: Repository - Abstrait l'accès aux données
Principe: Dependency Inversion - Dépend d'une abstraction
"""
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List

from ..models.station import Station
from ..models.weather_data import WeatherData
from ..factories.station_factory import StationFactory
from ..config.config_manager import ConfigManager
from ..utils.csv_reader import read_csv
from ..data_structures.linked_list import LinkedList


class WeatherRepository(ABC):
    """
    Interface abstraite pour l'accès aux données météorologiques.
    Permet de changer l'implémentation sans modifier le code client.
    """

    @abstractmethod
    def get_all_stations(self) -> List[Station]:
        """Retourne toutes les stations disponibles."""

    @abstractmethod
    def get_weather_data(self, station_id: int, limit: int = 10) -> List[WeatherData]:
        """
        Retourne les données météo pour une station.

        Args:
            station_id: ID de la station
            limit: Nombre maximum de résultats
        """

    @abstractmethod
    def get_weather_data_as_linked_list(self, station_id: int, limit: int = 10) -> LinkedList:
        """
        Retourne les données météo pour une station sous forme de liste chaînée.

        Args:
            station_id: ID de la station
            limit: Nombre maximum de résultats

        Returns:
            LinkedList contenant les WeatherData
        """


class CSVWeatherRepository(WeatherRepository):
    """
    Implémentation du Repository pour les fichiers CSV.
    """

    def __init__(self):
        """Initialise le repository avec le gestionnaire de configuration."""
        self.config_manager = ConfigManager()
        self.base_path = self.config_manager.get_base_path()

    def get_all_stations(self) -> List[Station]:
        """
        Retourne toutes les stations configurées.

        Returns:
            Liste des stations
        """
        stations_config = self.config_manager.get_stations_config()
        stations = []

        for config in stations_config:
            try:
                station = StationFactory.create_from_config(config)
                stations.append(station)
            except ValueError as e:
                print(f"Erreur lors de la création de la station: {e}")

        return stations

    def get_weather_data(self, station_id: int, limit: int = 10) -> List[WeatherData]:
        """
        Retourne les données météo pour une station depuis le fichier CSV.

        Args:
            station_id: ID de la station
            limit: Nombre maximum de résultats

        Returns:
            Liste des données météo

        Raises:
            ValueError: Si la station n'existe pas
        """
        # Trouver le fichier correspondant à la station
        station_file = self._get_station_file(station_id)

        if not station_file:
            raise ValueError(f"Aucune station trouvée avec l'ID {station_id}")

        # Lire les données CSV
        file_path = self.base_path / station_file
        csv_data = read_csv(str(file_path))

        # Convertir en objets WeatherData
        weather_data_list = []
        for i, row in enumerate(csv_data):
            if i >= limit:
                break

            try:
                weather_data = self._parse_weather_data(row)
                weather_data_list.append(weather_data)
            except (ValueError, KeyError):
                # Ignorer les lignes mal formatées
                continue

        return weather_data_list

    def _get_station_file(self, station_id: int) -> str:
        """
        Trouve le fichier de données pour une station donnée.

        Args:
            station_id: ID de la station

        Returns:
            Chemin du fichier ou None si non trouvé
        """
        stations_config = self.config_manager.get_stations_config()

        for station_config in stations_config:
            if station_config['id'] == station_id:
                station_name = station_config['name'].lower()
                return self.config_manager.get_data_source(station_name)

        return None

    def _parse_weather_data(self, row: dict) -> WeatherData:
        """
        Parse une ligne CSV en objet WeatherData.

        Args:
            row: Dictionnaire représentant une ligne CSV

        Returns:
            Instance de WeatherData
        """
        # Parser la température
        temperature = float(row['temperature'])

        # Parser l'humidité
        humidity = int(row['humidite'])

        # Parser la date/heure
        timestamp = datetime.fromisoformat(row['heure_de_paris'])

        # Champs optionnels
        pressure = int(row['pression']) if row.get('pression') else None
        rain = float(row['pluie']) if row.get('pluie') else None

        return WeatherData(
            temperature=temperature,
            humidity=humidity,
            timestamp=timestamp,
            pressure=pressure,
            rain=rain
        )

    def get_weather_data_as_linked_list(self, station_id: int, limit: int = 10) -> LinkedList:
        """
        Retourne les données météo pour une station sous forme de liste chaînée.

        Args:
            station_id: ID de la station
            limit: Nombre maximum de résultats

        Returns:
            LinkedList contenant les WeatherData

        Raises:
            ValueError: Si la station n'existe pas
        """
        # Récupérer les données sous forme de liste
        weather_data_list = self.get_weather_data(station_id, limit)

        # Créer une liste chaînée et y ajouter les données
        linked_list = LinkedList()
        for weather_data in weather_data_list:
            linked_list.append(weather_data)

        return linked_list
