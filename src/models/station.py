"""
Classe Station - Représente une station météorologique
Principe: Single Responsibility - Gère uniquement les informations d'une station
"""
from dataclasses import dataclass


@dataclass
class Station:
    """
    Représente une station météorologique.
    
    Attributes:
        id: Identifiant unique de la station
        name: Nom de la station
        station_type: Type de station (ex: ISS)
    """
    id: int
    name: str
    station_type: str
    
    def __str__(self) -> str:
        """Retourne une représentation textuelle de la station."""
        return f"Station {self.name} (ID: {self.id}) - Type: {self.station_type}"
    
    def __repr__(self) -> str:
        """Retourne une représentation pour le débogage."""
        return f"Station(id={self.id}, name='{self.name}', station_type='{self.station_type}')"
