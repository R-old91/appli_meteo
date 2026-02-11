"""
ConfigManager - Singleton pour gérer la configuration
Pattern: Singleton - Une seule instance de configuration dans l'application
"""
import json
from pathlib import Path
from typing import Dict, List, Optional


class ConfigManager:
    """
    Gestionnaire de configuration utilisant le pattern Singleton.
    Charge et fournit l'accès à la configuration de l'application.
    """
    _instance: Optional['ConfigManager'] = None
    _config: Optional[Dict] = None

    def __new__(cls):
        """Implémentation du Singleton - retourne toujours la même instance."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialise le gestionnaire (appelé une seule fois)."""
        if self._config is None:
            self._load_config()

    def _load_config(self) -> None:
        """Charge la configuration depuis le fichier config.json."""
        config_path = Path(__file__).parent.parent.parent / 'config.json'

        if not config_path.exists():
            raise FileNotFoundError(f"Fichier de configuration non trouvé: {config_path}")

        try:
            with open(config_path, 'r', encoding='utf-8') as file:
                self._config = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(
                f"Erreur de format dans le fichier de configuration: {e}"
            ) from e

    def get_data_source(self, station_name: str) -> str:
        """
        Retourne le chemin du fichier de données pour une station.

        Args:
            station_name: Nom de la station (ex: 'compans', 'marengo')

        Returns:
            Chemin relatif vers le fichier CSV
        """
        data_sources = self._config.get('data_sources', {})
        if station_name not in data_sources:
            raise ValueError(f"Station '{station_name}' non trouvée dans la configuration")
        return data_sources[station_name]

    def get_stations_config(self) -> List[Dict]:
        """
        Retourne la liste des configurations de stations.

        Returns:
            Liste de dictionnaires contenant les infos des stations
        """
        return self._config.get('stations', [])

    def get_update_sources(self) -> Dict[str, str]:
        """
        Retourne les chemins des fichiers de mise à jour.

        Returns:
            Dictionnaire {nom_station: chemin_fichier_update}
        """
        return self._config.get('update_sources', {})

    def get_api_config(self) -> Dict:
        """
        Retourne la configuration de l'API météo.

        Returns:
            Dictionnaire contenant base_url, api_key et cities
        """
        return self._config.get('api', {})

    def get_base_path(self) -> Path:
        """Retourne le chemin de base du projet."""
        return Path(__file__).parent.parent.parent
