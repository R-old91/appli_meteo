"""
StationFactory - Factory pour créer des objets Station
Pattern: Factory - Centralise la logique de création des stations
"""
from typing import Dict
from ..models.station import Station


class StationFactory:
    """
    Factory pour créer des instances de Station.
    Centralise la logique de création et facilite les tests.
    """
    
    @staticmethod
    def create_station(station_id: int, name: str, station_type: str) -> Station:
        """
        Crée une instance de Station.
        
        Args:
            station_id: Identifiant unique de la station
            name: Nom de la station
            station_type: Type de station
            
        Returns:
            Instance de Station
        """
        return Station(id=station_id, name=name, station_type=station_type)
    
    @staticmethod
    def create_from_config(config: Dict) -> Station:
        """
        Crée une instance de Station à partir d'un dictionnaire de configuration.
        
        Args:
            config: Dictionnaire contenant 'id', 'name' et 'type'
            
        Returns:
            Instance de Station
            
        Raises:
            ValueError: Si des champs requis sont manquants
        """
        required_fields = ['id', 'name', 'type']
        missing_fields = [field for field in required_fields if field not in config]
        
        if missing_fields:
            raise ValueError(f"Champs manquants dans la configuration: {', '.join(missing_fields)}")
        
        return StationFactory.create_station(
            station_id=config['id'],
            name=config['name'],
            station_type=config['type']
        )
