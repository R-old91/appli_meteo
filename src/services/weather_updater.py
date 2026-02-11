"""
WeatherUpdater - Service de mise à jour des données météo
Responsabilité unique: Gérer la mise à jour des données d'une station via la liste chaînée
"""
from datetime import datetime
from typing import Optional

from ..data_structures.linked_list import LinkedList
from ..models.weather_data import WeatherData
from ..repositories.weather_repository import CSVWeatherRepository
from ..utils.csv_reader import read_csv
from ..config.config_manager import ConfigManager


class WeatherUpdater:
    """
    Service de mise à jour des données météo.

    Responsabilité unique: Charger des données de mise à jour depuis des fichiers CSV
    fictifs et les injecter dans une LinkedList existante.

    Attributes:
        repository: Repository pour accéder aux données existantes
        config_manager: Gestionnaire de configuration
    """

    def __init__(self, repository: CSVWeatherRepository):
        """
        Initialise le service de mise à jour.

        Args:
            repository: Instance du repository pour accéder aux données
        """
        self.repository = repository
        self.config_manager = ConfigManager()
        self.base_path = self.config_manager.get_base_path()

    def load_update_data(self, station_id: int) -> LinkedList:
        """
        Charge les données de mise à jour depuis le fichier CSV fictif.

        Args:
            station_id: ID de la station à mettre à jour

        Returns:
            LinkedList contenant les nouvelles données

        Raises:
            ValueError: Si aucune donnée de mise à jour disponible
        """
        update_file = self._get_update_file(station_id)

        if not update_file:
            raise ValueError(f"Aucune mise à jour disponible pour la station {station_id}")

        file_path = self.base_path / update_file
        csv_data = read_csv(str(file_path))

        update_list = LinkedList()
        for row in csv_data:
            try:
                weather_data = self._parse_weather_data(row)
                update_list.append(weather_data)
            except (ValueError, KeyError):
                continue

        return update_list

    def update_station_data(self, station_id: int) -> LinkedList:
        """
        Met à jour les données d'une station en combinant données existantes et nouvelles.

        Les nouvelles données sont ajoutées à la fin de la liste chaînée existante.

        Args:
            station_id: ID de la station à mettre à jour

        Returns:
            LinkedList contenant les données existantes + les nouvelles données
        """
        # Charger les données existantes dans une liste chaînée
        existing_data = self.repository.get_weather_data_as_linked_list(station_id, limit=10)

        # Charger les données de mise à jour
        update_data = self.load_update_data(station_id)

        # Fusionner : ajouter les nouvelles données à la fin de la liste existante
        for data in update_data:
            existing_data.append(data)

        return existing_data

    def _get_update_file(self, station_id: int) -> Optional[str]:
        """
        Trouve le fichier de mise à jour pour une station.

        Args:
            station_id: ID de la station

        Returns:
            Chemin du fichier de mise à jour, ou None
        """
        update_sources = self.config_manager.get_update_sources()

        stations_config = self.config_manager.get_stations_config()
        for station_config in stations_config:
            if station_config['id'] == station_id:
                station_name = station_config['name'].lower()
                return update_sources.get(station_name)

        return None

    def _parse_weather_data(self, row: dict) -> WeatherData:
        """
        Parse une ligne CSV en objet WeatherData.

        Args:
            row: Dictionnaire représentant une ligne CSV

        Returns:
            Instance de WeatherData
        """
        temperature = float(row['temperature'])
        humidity = int(row['humidite'])
        timestamp = datetime.fromisoformat(row['heure_de_paris'])
        pressure = int(row['pression']) if row.get('pression') else None
        rain = float(row['pluie']) if row.get('pluie') else None

        return WeatherData(
            temperature=temperature,
            humidity=humidity,
            timestamp=timestamp,
            pressure=pressure,
            rain=rain
        )
