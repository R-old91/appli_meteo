"""
Application Météo - Point d'entrée principal
Application simple en ligne de commande pour afficher les données météorologiques
"""
from src.repositories.weather_repository import CSVWeatherRepository


def print_separator():
    """Affiche un séparateur visuel."""
    print("\n" + "=" * 60 + "\n")


def display_menu():
    """Affiche le menu principal."""
    print_separator()
    print("=== Application Météo ===")
    print("\n1. Afficher les stations")
    print("2. Afficher les données météo d'une station")
    print("3. Quitter")
    print_separator()


def display_stations(repository: CSVWeatherRepository):
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
        
    except Exception as e:
        print(f"Erreur lors de la récupération des stations: {e}")


def display_weather_data(repository: CSVWeatherRepository):
    """
    Affiche les données météo pour une station spécifique.
    
    Args:
        repository: Instance du repository
    """
    try:
        station_id = int(input("\nEntrez l'ID de la station: "))
        
        # Récupérer les données
        weather_data_list = repository.get_weather_data(station_id, limit=10)
        
        if not weather_data_list:
            print(f"\nAucune donnée trouvée pour la station {station_id}.")
            return
        
        # Trouver le nom de la station
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
        
    except ValueError as e:
        print(f"\nErreur: {e}")
    except Exception as e:
        print(f"\nErreur inattendue: {e}")


def main():
    """Fonction principale de l'application."""
    # Initialiser le repository (Dependency Injection)
    repository = CSVWeatherRepository()
    
    print("\nBienvenue dans l'Application Météo!")
    
    while True:
        display_menu()
        
        try:
            choice = input("Votre choix: ").strip()
            
            if choice == "1":
                display_stations(repository)
            
            elif choice == "2":
                display_weather_data(repository)
            
            elif choice == "3":
                print("\nMerci d'avoir utilisé l'Application Météo!")
                print("Au revoir!\n")
                break
            
            else:
                print("\nChoix invalide. Veuillez choisir 1, 2 ou 3.")
        
        except KeyboardInterrupt:
            print("\n\nInterruption détectée. Au revoir!\n")
            break
        except Exception as e:
            print(f"\nErreur: {e}")


if __name__ == "__main__":
    main()
