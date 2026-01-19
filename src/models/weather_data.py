"""
Classe WeatherData - Value Object pour les données météorologiques
Principe: Immutabilité - Les données météo ne changent pas une fois créées
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass(frozen=True)
class WeatherData:
    """
    Value Object représentant les données météorologiques à un instant donné.
    
    Attributes:
        temperature: Température en degrés Celsius
        humidity: Humidité en pourcentage
        timestamp: Date et heure de la mesure
        pressure: Pression atmosphérique (optionnel)
        rain: Quantité de pluie (optionnel)
    """
    temperature: float
    humidity: int
    timestamp: datetime
    pressure: Optional[int] = None
    rain: Optional[float] = None
    
    def __str__(self) -> str:
        """Retourne une représentation textuelle formatée des données météo."""
        time_str = self.timestamp.strftime("%Y-%m-%d %H:%M")
        return f"[{time_str}] Température: {self.temperature}°C, Humidité: {self.humidity}%"
    
    def get_detailed_info(self) -> str:
        """Retourne une représentation détaillée incluant toutes les données disponibles."""
        info = str(self)
        if self.pressure is not None:
            info += f", Pression: {self.pressure / 100:.1f} hPa"
        if self.rain is not None and self.rain > 0:
            info += f", Pluie: {self.rain} mm"
        return info
