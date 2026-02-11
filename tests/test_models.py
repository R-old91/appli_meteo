"""
Tests pour les modèles Station et WeatherData — style pytest
Convention: test_<nom_de_la_fonction_testée>
"""
import pytest
from datetime import datetime

from src.models.station import Station
from src.models.weather_data import WeatherData


# ── Tests Station ───────────────────────────────────────


def test_station_creation():
    """Vérifie qu'une station est correctement créée avec ses attributs."""
    station = Station(id=42, name="Compans", station_type="ISS")

    assert station.id == 42
    assert station.name == "Compans"
    assert station.station_type == "ISS"


def test_station_str():
    """Vérifie que __str__ retourne le format attendu."""
    station = Station(id=42, name="Compans", station_type="ISS")

    result = str(station)

    assert "Compans" in result
    assert "42" in result
    assert "ISS" in result


def test_station_egalite():
    """Vérifie que deux stations avec les mêmes attributs sont égales."""
    station1 = Station(id=42, name="Compans", station_type="ISS")
    station2 = Station(id=42, name="Compans", station_type="ISS")

    assert station1 == station2


# ── Tests WeatherData ──────────────────────────────────


@pytest.fixture
def sample_weather_data():
    """Fixture : crée un WeatherData pour les tests."""
    timestamp = datetime(2025, 9, 10, 7, 45)
    return WeatherData(temperature=13.2, humidity=79, timestamp=timestamp)


def test_weather_data_creation(sample_weather_data):
    """Vérifie qu'un WeatherData est correctement créé."""
    assert sample_weather_data.temperature == 13.2
    assert sample_weather_data.humidity == 79
    assert sample_weather_data.timestamp == datetime(2025, 9, 10, 7, 45)


def test_weather_data_immutabilite(sample_weather_data):
    """Vérifie que WeatherData est immuable (frozen dataclass)."""
    with pytest.raises(AttributeError):
        sample_weather_data.temperature = 20.0


def test_weather_data_str(sample_weather_data):
    """Vérifie que __str__ affiche la température et l'humidité."""
    result = str(sample_weather_data)

    assert "13.2°C" in result
    assert "79%" in result
    assert "2025-09-10" in result
