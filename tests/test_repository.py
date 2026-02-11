"""
Tests pour le Repository CSV et le WeatherUpdater — style pytest
Convention: test_<nom_de_la_fonction_testée>
"""
import pytest

from src.repositories.weather_repository import CSVWeatherRepository
from src.services.weather_updater import WeatherUpdater
from src.models.station import Station
from src.models.weather_data import WeatherData


# ── Fixtures ────────────────────────────────────────────


@pytest.fixture
def csv_repository():
    """Fixture : crée un CSVWeatherRepository."""
    return CSVWeatherRepository()


@pytest.fixture
def weather_updater(csv_repository):
    """Fixture : crée un WeatherUpdater avec le repository CSV."""
    return WeatherUpdater(csv_repository)


# ── Tests CSVWeatherRepository ──────────────────────────


def test_get_all_stations(csv_repository):
    """Vérifie que les stations sont correctement chargées."""
    stations = csv_repository.get_all_stations()

    assert len(stations) == 2
    assert isinstance(stations[0], Station)

    station_names = [s.name for s in stations]
    assert "Compans" in station_names
    assert "Marengo" in station_names


def test_get_weather_data(csv_repository):
    """Vérifie que les données météo sont correctement chargées."""
    data = csv_repository.get_weather_data(station_id=42, limit=5)

    assert len(data) == 5
    assert isinstance(data[0], WeatherData)

    for weather in data:
        assert isinstance(weather.temperature, float)
        assert isinstance(weather.humidity, int)
        assert 0 <= weather.humidity <= 100


def test_get_weather_data_station_inexistante(csv_repository):
    """Vérifie qu'une erreur est levée pour une station inexistante."""
    with pytest.raises(ValueError):
        csv_repository.get_weather_data(station_id=999, limit=5)


def test_get_weather_data_as_linked_list(csv_repository):
    """Vérifie que les données sont retournées dans une LinkedList."""
    linked_list = csv_repository.get_weather_data_as_linked_list(
        station_id=42, limit=3
    )

    assert linked_list.size() == 3
    assert isinstance(linked_list.get(0), WeatherData)


# ── Tests WeatherUpdater ───────────────────────────────


def test_load_update_data(weather_updater):
    """Vérifie que les données de mise à jour sont chargées."""
    update_data = weather_updater.load_update_data(station_id=42)

    assert update_data.size() > 0
    assert isinstance(update_data.get(0), WeatherData)


def test_update_station_data_fusion(csv_repository, weather_updater):
    """Vérifie que la fusion ajoute les nouvelles données."""
    existing = csv_repository.get_weather_data_as_linked_list(
        station_id=42, limit=10
    )
    existing_size = existing.size()

    update = weather_updater.load_update_data(station_id=42)
    update_size = update.size()

    merged = weather_updater.update_station_data(station_id=42)

    assert merged.size() == existing_size + update_size
