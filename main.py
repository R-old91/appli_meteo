"""
Application Météo - Point d'entrée principal
Application en ligne de commande pour afficher les données météorologiques.

Design Patterns utilisés :
    - Repository : Abstraction de l'accès aux données (CSV et API)
    - Factory : Création centralisée des objets Station
    - Singleton : Instance unique de configuration

Structures de données :
    - LinkedList : Stockage séquentiel des données météo
    - Queue : File d'attente des requêtes API
    - WeatherDict : Cache de données par station
"""
from src.repositories.weather_repository import CSVWeatherRepository
from src.repositories.api_weather_repository import APIWeatherRepository
from src.services.weather_updater import WeatherUpdater


def print_separator():
    """Affiche un séparateur visuel."""
    print("\n" + "=" * 60 + "\n")


def display_menu():
    """Affiche le menu principal."""
    print_separator()
    print("=== Application Météo ===")
    print("\n1. Afficher les stations (CSV)")
    print("2. Afficher les données météo d'une station (CSV)")
    print("3. Afficher les données météo avec liste chaînée")
    print("4. Mettre à jour les données d'une station (CSV)")
    print("5. Météo en ligne (API)")
    print("6. Rafraîchir les données API")
    print("7. Quitter")
    print_separator()


def display_stations(repository):
    """
    Affiche toutes les stations disponibles.

    Args:
        repository: Instance du repository
    """
    print("\nStations disponibles:")
    print("-" * 60)

    try:
        stations = repository.get_all_stations()

        if not stations:
            print("Aucune station trouvée.")
            return

        for station in stations:
            print(f"  • {station}")

    except Exception as err:
        print(f"Erreur lors de la récupération des stations: {err}")


def display_weather_data(repository):
    """
    Affiche les données météo pour une station spécifique.

    Args:
        repository: Instance du repository
    """
    try:
        station_id = int(input("\nEntrez l'ID de la station: "))

        weather_data_list = repository.get_weather_data(station_id, limit=10)

        if not weather_data_list:
            print(f"\nAucune donnée trouvée pour la station {station_id}.")
            return

        stations = repository.get_all_stations()
        station_name = next(
            (s.name for s in stations if s.id == station_id),
            f"Station {station_id}"
        )

        print(f"\nDonnées météo pour {station_name}:")
        print("-" * 60)

        for data in weather_data_list:
            print(f"  {data}")

        print(f"\n{len(weather_data_list)} enregistrement(s) affiché(s)")

    except ValueError as err:
        print(f"\nErreur: {err}")
    except Exception as err:
        print(f"\nErreur inattendue: {err}")


def display_weather_data_linked_list(repository):
    """
    Affiche les données météo en utilisant une liste chaînée.

    Args:
        repository: Instance du repository
    """
    try:
        station_id = int(input("\nEntrez l'ID de la station: "))

        linked_list = repository.get_weather_data_as_linked_list(
            station_id, limit=10
        )

        if linked_list.is_empty():
            print(f"\nAucune donnée trouvée pour la station {station_id}.")
            return

        stations = repository.get_all_stations()
        station_name = next(
            (s.name for s in stations if s.id == station_id),
            f"Station {station_id}"
        )

        print(f"\nDonnées météo pour {station_name} (Liste Chaînée):")
        print("-" * 60)
        print(f"Taille: {linked_list.size()} élément(s)")
        print("-" * 60)

        for i, data in enumerate(linked_list):
            print(f"  [{i}] {data}")

        print(
            f"\n{linked_list.size()} enregistrement(s) "
            f"affiché(s) depuis la liste chaînée"
        )

    except ValueError as err:
        print(f"\nErreur: {err}")
    except Exception as err:
        print(f"\nErreur inattendue: {err}")


def update_weather_data(repository, updater):
    """
    Met à jour les données météo d'une station avec les données fictives.

    Args:
        repository: Instance du repository
        updater: Instance du service de mise à jour
    """
    try:
        print("\nStations disponibles pour mise à jour:")
        print("-" * 60)
        stations = repository.get_all_stations()
        for station in stations:
            print(f"  • {station}")

        station_id = int(
            input("\nEntrez l'ID de la station à mettre à jour: ")
        )

        station_name = next(
            (s.name for s in stations if s.id == station_id),
            f"Station {station_id}"
        )

        # Afficher les données AVANT mise à jour
        print(f"\n--- AVANT mise à jour ({station_name}) ---")
        existing_list = repository.get_weather_data_as_linked_list(
            station_id, limit=5
        )
        print(f"Nombre d'enregistrements: {existing_list.size()}")
        for i, data in enumerate(existing_list):
            print(f"  [{i}] {data}")

        # Charger les nouvelles données
        print("\nChargement des nouvelles données...")
        new_data = updater.load_update_data(station_id)
        print(f"Nouvelles données chargées: {new_data.size()} enregistrement(s)")
        for i, data in enumerate(new_data):
            print(f"  [NEW {i}] {data}")

        # Fusionner
        print("\nFusion des données...")
        merged_list = updater.update_station_data(station_id)

        # Afficher les données APRÈS mise à jour
        print(f"\n--- APRÈS mise à jour ({station_name}) ---")
        print(f"Nombre total d'enregistrements: {merged_list.size()}")
        print("-" * 60)
        for i, data in enumerate(merged_list):
            print(f"  [{i}] {data}")

        print(
            f"\n✅ Mise à jour terminée! "
            f"{merged_list.size()} enregistrement(s) au total"
        )

    except ValueError as err:
        print(f"\nErreur: {err}")
    except Exception as err:
        print(f"\nErreur inattendue: {err}")


def display_online_weather(api_repository):
    """
    Affiche les données météo récupérées depuis l'API en ligne.

    Utilise les structures de données :
        - Queue pour mettre en file les requêtes
        - WeatherDict comme cache
        - LinkedList pour stocker les résultats

    Args:
        api_repository: Instance du APIWeatherRepository
    """
    try:
        print("\nStations disponibles (API en ligne):")
        print("-" * 60)
        stations = api_repository.get_all_stations()

        if not stations:
            print("Aucune station API configurée.")
            print("Renseignez la section 'api' dans config.json")
            return

        for station in stations:
            print(f"  • {station}")

        station_id = int(input("\nEntrez l'ID de la station: "))

        # Récupérer les données via l'API
        data_list = api_repository.get_weather_data(station_id)

        if not data_list:
            print("\nAucune donnée récupérée.")
            print("Vérifiez votre connexion internet.")
            return

        # Afficher dans une liste chaînée
        linked_list = api_repository.get_weather_data_as_linked_list(
            station_id
        )

        station_name = next(
            (s.name for s in stations if s.id == station_id),
            f"Station {station_id}"
        )

        print(f"\n🌤️ Dernières mesures pour {station_name}:")
        print("-" * 60)
        for data in linked_list:
            print(f"  {data.get_detailed_info()}")

    except ValueError as err:
        print(f"\nErreur: {err}")
    except Exception as err:
        print(f"\nErreur inattendue: {err}")


def refresh_api_data(api_repository):
    """
    Rafraîchit les données météo depuis l'API.

    Vide le cache (WeatherDict) et relance les requêtes
    pour obtenir les données les plus récentes.

    Args:
        api_repository: Instance de APIWeatherRepository
    """
    print("\n🔄 Rafraîchissement des données API...")
    print("-" * 60)

    try:
        # Vider le cache
        api_repository.clear_cache()

        # Récupérer les stations disponibles
        stations = api_repository.get_all_stations()

        if not stations:
            print("Aucune station API configurée.")
            return

        # Utiliser la Queue pour traiter toutes les stations
        for station in stations:
            api_repository.enqueue_request(station.id)

        # Traiter la file d'attente
        all_data = api_repository.process_queue()

        print(f"\n✅ {len(all_data)} mesures récupérées")

        # Afficher les données les plus récentes
        for station in stations:
            linked_list = api_repository.get_weather_data_as_linked_list(
                station.id, limit=5
            )
            print(f"\n🌤️ {station.name} (dernières mesures):")
            for data in linked_list:
                print(f"  {data.get_detailed_info()}")

    except Exception as err:
        print(f"\nErreur lors du rafraîchissement: {err}")


def main():
    """Fonction principale de l'application."""
    # Initialiser les composants (Dependency Injection)
    csv_repository = CSVWeatherRepository()
    api_repository = APIWeatherRepository()
    updater = WeatherUpdater(csv_repository)

    print("\nBienvenue dans l'Application Météo!")

    while True:
        display_menu()

        try:
            choice = input("Votre choix: ").strip()

            if choice == "1":
                display_stations(csv_repository)

            elif choice == "2":
                display_weather_data(csv_repository)

            elif choice == "3":
                display_weather_data_linked_list(csv_repository)

            elif choice == "4":
                update_weather_data(csv_repository, updater)

            elif choice == "5":
                display_online_weather(api_repository)

            elif choice == "6":
                refresh_api_data(api_repository)

            elif choice == "7":
                print("\nMerci d'avoir utilisé l'Application Météo!")
                print("Au revoir!\n")
                break

            else:
                print("\nChoix invalide. Veuillez choisir 1 à 7.")

        except KeyboardInterrupt:
            print("\n\nInterruption détectée. Au revoir!\n")
            break
        except Exception as err:
            print(f"\nErreur: {err}")


if __name__ == "__main__":
    main()
