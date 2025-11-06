"""
Modèle de classes pour une application météo
Principes appliqués: POO, SOLID, Clean Code
"""

from datetime import datetime
from typing import List, Tuple, Dict, Optional
import csv
import os


# ============================================
# 1. ENTITÉS MÉTIER (Modèle de données)
# ============================================

class Station:
    """
    Représente une station météo physique.
    Responsabilité: Stocker les informations d'une station.
    """
    
    def __init__(self, id: str, nom: str, latitude: float, longitude: float, 
                 ville: str, altitude: Optional[float] = None):
        self.id = id
        self.nom = nom
        self.latitude = latitude
        self.longitude = longitude
        self.ville = ville
        self.altitude = altitude
    
    def __str__(self) -> str:
        return f"Station {self.nom} ({self.ville}) - ID: {self.id}"
    
    def __repr__(self) -> str:
        return f"Station(id={self.id}, nom={self.nom}, ville={self.ville})"


class DonneeMeteo:
    """
    Représente une observation météo à un instant T.
    Responsabilité: Stocker une mesure météorologique.
    """
    
    def __init__(self, station_id: str, timestamp: datetime, 
                 temperature: float, humidite: float, pression: float,
                 vitesse_vent: float, direction_vent: int, precipitation: float):
        self.station_id = station_id
        self.timestamp = timestamp
        self.temperature = temperature
        self.humidite = humidite
        self.pression = pression
        self.vitesse_vent = vitesse_vent
        self.direction_vent = direction_vent
        self.precipitation = precipitation
    
    def est_valide(self) -> bool:
        """
        Vérifie la cohérence des données météo.
        
        Returns:
            bool: True si les données sont cohérentes, False sinon
        """
        if self.temperature < -100 or self.temperature > 60:
            return False
        if self.humidite < 0 or self.humidite > 100:
            return False
        if self.pression < 800 or self.pression > 1100:
            return False
        if self.vitesse_vent < 0:
            return False
        if self.direction_vent < 0 or self.direction_vent > 360:
            return False
        if self.precipitation < 0:
            return False
        return True
    
    def __str__(self) -> str:
        return (f"Données météo du {self.timestamp.strftime('%Y-%m-%d %H:%M')} - "
                f"Station {self.station_id}: {self.temperature}°C, "
                f"{self.humidite}% humidité")
    
    def __repr__(self) -> str:
        return (f"DonneeMeteo(station_id={self.station_id}, "
                f"timestamp={self.timestamp}, temperature={self.temperature})")


# ============================================
# 2. SERVICES (Logique métier)
# ============================================

class CollecteurDonnees:
    """
    Responsabilité: Récupérer les données brutes depuis des fichiers CSV locaux.
    """
    
    def __init__(self, dossier_data: str):
        """
        Initialise le collecteur avec le chemin vers le dossier contenant les CSV.
        
        Args:
            dossier_data: Chemin vers le dossier contenant les fichiers CSV
        """
        self.dossier_data = dossier_data
        self.fichiers_csv = []
    
    def collecter_donnees(self) -> List[Dict]:
        """
        Récupère les données brutes depuis les fichiers CSV.
        
        Returns:
            List[Dict]: Liste de dictionnaires contenant les données brutes
        """
        print(f"Collecte des données depuis {self.dossier_data}...")
        
        # Lister tous les fichiers CSV dans le dossier
        self._lister_fichiers_csv()
        
        if not self.fichiers_csv:
            print("❌ Aucun fichier CSV trouvé dans le dossier.")
            return []
        
        # Lire tous les fichiers CSV
        donnees_brutes = self._lire_tous_les_csv()
        print(f"✓ {len(donnees_brutes)} enregistrements collectés depuis {len(self.fichiers_csv)} fichier(s)")
        return donnees_brutes
    
    def _lister_fichiers_csv(self) -> None:
        """
        Liste tous les fichiers CSV présents dans le dossier data.
        """
        if not os.path.exists(self.dossier_data):
            print(f"❌ Le dossier {self.dossier_data} n'existe pas.")
            return
        
        self.fichiers_csv = [
            f for f in os.listdir(self.dossier_data) 
            if f.endswith('.csv')
        ]
        
        if self.fichiers_csv:
            print(f"  Fichiers trouvés: {', '.join(self.fichiers_csv)}")
    
    def _lire_tous_les_csv(self) -> List[Dict]:
        """
        Lit tous les fichiers CSV et retourne les données brutes.
        
        Returns:
            List[Dict]: Données brutes de tous les fichiers
        """
        donnees_brutes = []
        
        for fichier in self.fichiers_csv:
            chemin_complet = os.path.join(self.dossier_data, fichier)
            donnees_fichier = self._lire_csv(chemin_complet, fichier)
            donnees_brutes.extend(donnees_fichier)
        
        return donnees_brutes
    
    def _lire_csv(self, chemin_fichier: str, nom_fichier: str) -> List[Dict]:
        """
        Lit un fichier CSV et extrait les données.
        Détermine automatiquement le nom de la station depuis le nom du fichier.
        
        Args:
            chemin_fichier: Chemin complet vers le fichier CSV
            nom_fichier: Nom du fichier (pour extraire le nom de la station)
            
        Returns:
            List[Dict]: Données du fichier CSV
        """
        donnees = []
        
        # Extraire le nom de la station depuis le nom du fichier
        # Ex: "meteo_compans.csv" -> "compans"
        station_nom = nom_fichier.replace('meteo_', '').replace('.csv', '').capitalize()
        station_id = f"ST_{station_nom.upper()}"
        
        # Mapping des noms de colonnes du CSV vers les attributs attendus
        mapping_colonnes = {
            'humidite': 'humidite',
            'pression': 'pression',
            'temperature': 'temperature',
            'heure_utc': 'timestamp',
            'id': 'id'
        }
        
        try:
            with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
                lecteur = csv.DictReader(fichier)
                
                for ligne in lecteur:
                    # Créer un dictionnaire avec les données nettoyées
                    donnee = {
                        'station_id': station_id,
                        'station_nom': f"Station {station_nom}",
                        'ville': station_nom,
                    }
                    
                    # Extraire uniquement les colonnes nécessaires
                    for col_csv, col_interne in mapping_colonnes.items():
                        if col_csv in ligne:
                            donnee[col_interne] = ligne[col_csv]
                    
                    # Valeurs par défaut pour les colonnes optionnelles
                    donnee.setdefault('vitesse_vent', 0)
                    donnee.setdefault('direction_vent', 0)
                    donnee.setdefault('precipitation', 0)
                    donnee.setdefault('latitude', 0.0)
                    donnee.setdefault('longitude', 0.0)
                    donnee.setdefault('altitude', 0)
                    
                    donnees.append(donnee)
            
            print(f"  ✓ {len(donnees)} enregistrements lus depuis {nom_fichier}")
            
        except Exception as e:
            print(f"  ❌ Erreur lors de la lecture de {nom_fichier}: {str(e)}")
        
        return donnees


class NettoyeurDonnees:
    """
    Responsabilité: Nettoyer et valider les données brutes.
    """
    
    def nettoyer(self, donnees_brutes: List[Dict]) -> List[Dict]:
        """
        Applique le pipeline de nettoyage complet.
        
        Args:
            donnees_brutes: Données brutes à nettoyer
            
        Returns:
            List[Dict]: Données nettoyées
        """
        print("Nettoyage des données...")
        donnees = self._supprimer_doublons(donnees_brutes)
        donnees = self._gerer_valeurs_manquantes(donnees)
        donnees = self._valider_format(donnees)
        print(f"✓ {len(donnees)} enregistrements valides après nettoyage")
        return donnees
    
    def _supprimer_doublons(self, donnees: List[Dict]) -> List[Dict]:
        """
        Supprime les enregistrements en double.
        
        Args:
            donnees: Liste des données
            
        Returns:
            List[Dict]: Données sans doublons
        """
        # Utilise un set pour identifier les doublons basés sur station_id et timestamp
        vus = set()
        donnees_uniques = []
        
        for d in donnees:
            cle = (d.get('station_id'), d.get('timestamp'))
            if cle not in vus:
                vus.add(cle)
                donnees_uniques.append(d)
        
        nb_doublons = len(donnees) - len(donnees_uniques)
        if nb_doublons > 0:
            print(f"  - {nb_doublons} doublon(s) supprimé(s)")
        
        return donnees_uniques
    
    def _gerer_valeurs_manquantes(self, donnees: List[Dict]) -> List[Dict]:
        """
        Gère les valeurs manquantes (suppression ou imputation).
        
        Args:
            donnees: Liste des données
            
        Returns:
            List[Dict]: Données complètes
        """
        donnees_completes = []
        
        champs_obligatoires = ['station_id', 'timestamp', 'temperature', 
                               'humidite', 'pression']
        
        for d in donnees:
            # Vérifier que les champs obligatoires sont présents
            if all(d.get(champ) is not None for champ in champs_obligatoires):
                # Remplir les champs optionnels avec des valeurs par défaut
                d.setdefault('vitesse_vent', 0)
                d.setdefault('direction_vent', 0)
                d.setdefault('precipitation', 0)
                donnees_completes.append(d)
        
        nb_rejetes = len(donnees) - len(donnees_completes)
        if nb_rejetes > 0:
            print(f"  - {nb_rejetes} enregistrement(s) incomplet(s) rejeté(s)")
        
        return donnees_completes
    
    def _valider_format(self, donnees: List[Dict]) -> List[Dict]:
        """
        Valide le format des données (types, plages de valeurs).
        Convertit la pression de Pa en hPa si nécessaire.
        
        Args:
            donnees: Liste des données
            
        Returns:
            List[Dict]: Données avec format valide
        """
        donnees_valides = []
        
        for d in donnees:
            try:
                # Conversion et validation des types
                d['temperature'] = float(d['temperature'])
                d['humidite'] = float(d['humidite'])
                
                # Conversion de la pression : si > 10000, c'est en Pa, on convertit en hPa
                pression = float(d['pression'])
                if pression > 10000:
                    d['pression'] = pression / 100  # Conversion Pa -> hPa
                else:
                    d['pression'] = pression
                
                # Champs optionnels
                d['vitesse_vent'] = float(d.get('vitesse_vent', 0))
                d['direction_vent'] = int(d.get('direction_vent', 0))
                d['precipitation'] = float(d.get('precipitation', 0))
                
                # Validation basique des plages
                if (-100 <= d['temperature'] <= 60 and
                    0 <= d['humidite'] <= 100 and
                    800 <= d['pression'] <= 1100):
                    donnees_valides.append(d)
                else:
                    print(f"  ⚠️ Valeur hors plage ignorée: T={d['temperature']}°C, H={d['humidite']}%, P={d['pression']}hPa")
                    
            except (ValueError, TypeError, KeyError) as e:
                # Ignorer les enregistrements invalides
                print(f"  ⚠️ Enregistrement invalide ignoré: {str(e)}")
                continue
        
        nb_invalides = len(donnees) - len(donnees_valides)
        if nb_invalides > 0:
            print(f"  - {nb_invalides} enregistrement(s) au format invalide rejeté(s)")
        
        return donnees_valides


class TransformateurDonnees:
    """
    Responsabilité: Transformer les données nettoyées en objets métier.
    """
    
    def transformer(self, donnees_nettoyees: List[Dict]) -> Tuple[List[Station], List[DonneeMeteo]]:
        """
        Transforme les dictionnaires en objets Station et DonneeMeteo.
        
        Args:
            donnees_nettoyees: Données nettoyées sous forme de dictionnaires
            
        Returns:
            Tuple[List[Station], List[DonneeMeteo]]: Stations et données météo
        """
        print("Transformation des données en objets métier...")
        
        stations_dict = {}
        donnees_meteo = []
        
        for d in donnees_nettoyees:
            # Créer ou récupérer la station
            station_id = d['station_id']
            if station_id not in stations_dict:
                station = self._creer_station(d)
                stations_dict[station_id] = station
            
            # Créer la donnée météo
            donnee = self._creer_donnee_meteo(d)
            donnees_meteo.append(donnee)
        
        stations = list(stations_dict.values())
        print(f"✓ {len(stations)} station(s) et {len(donnees_meteo)} observation(s) créées")
        
        return stations, donnees_meteo
    
    def _creer_station(self, data: Dict) -> Station:
        """
        Crée un objet Station à partir d'un dictionnaire.
        
        Args:
            data: Dictionnaire contenant les données de la station
            
        Returns:
            Station: Objet Station créé
        """
        return Station(
            id=data['station_id'],
            nom=data.get('station_nom', f"Station {data['station_id']}"),
            latitude=data.get('latitude', 0.0),
            longitude=data.get('longitude', 0.0),
            ville=data.get('ville', 'Inconnue'),
            altitude=data.get('altitude')
        )
    
    def _creer_donnee_meteo(self, data: Dict) -> DonneeMeteo:
        """
        Crée un objet DonneeMeteo à partir d'un dictionnaire.
        
        Args:
            data: Dictionnaire contenant les données météo
            
        Returns:
            DonneeMeteo: Objet DonneeMeteo créé
        """
        # Conversion du timestamp - plusieurs formats possibles
        if isinstance(data['timestamp'], str):
            timestamp_str = data['timestamp']
            
            # Essayer différents formats de date
            formats = [
                '%Y-%m-%d %H:%M:%S',  # Format standard
                '%Y-%m-%dT%H:%M:%S%z',  # Format ISO avec timezone
                '%Y-%m-%d',  # Format date seule
            ]
            
            timestamp = None
            for fmt in formats:
                try:
                    # Nettoyer le timestamp si nécessaire
                    timestamp_clean = timestamp_str.split('+')[0].replace('T', ' ').strip()
                    if 'T' in timestamp_str and '%z' in fmt:
                        timestamp = datetime.strptime(timestamp_str, fmt)
                    else:
                        timestamp = datetime.strptime(timestamp_clean, fmt)
                    break
                except ValueError:
                    continue
            
            # Si aucun format ne marche, utiliser datetime.now()
            if timestamp is None:
                print(f"  ⚠️ Format de timestamp non reconnu: {timestamp_str}, utilisation de l'heure actuelle")
                timestamp = datetime.now()
        else:
            timestamp = data['timestamp']
        
        return DonneeMeteo(
            station_id=data['station_id'],
            timestamp=timestamp,
            temperature=float(data['temperature']),
            humidite=float(data['humidite']),
            pression=float(data['pression']),
            vitesse_vent=float(data.get('vitesse_vent', 0)),
            direction_vent=int(data.get('direction_vent', 0)),
            precipitation=float(data.get('precipitation', 0))
        )


# ============================================
# 3. SERVICE PRINCIPAL (Orchestrateur)
# ============================================

class ServiceMeteo:
    """
    Responsabilité: Orchestrer le système et gérer les use cases.
    Point d'entrée principal de l'application.
    """
    
    def __init__(self, dossier_data: str):
        """
        Initialise le service météo.
        
        Args:
            dossier_data: Chemin vers le dossier contenant les fichiers CSV
        """
        self.collecteur = CollecteurDonnees(dossier_data)
        self.nettoyeur = NettoyeurDonnees()
        self.transformateur = TransformateurDonnees()
        
        self.stations: List[Station] = []
        self.donnees: List[DonneeMeteo] = []
    
    def initialiser(self) -> None:
        """
        Lance le pipeline complet: collecte → nettoyage → transformation.
        """
        print("\n" + "="*50)
        print("INITIALISATION DU SYSTÈME MÉTÉO")
        print("="*50 + "\n")
        
        self._charger_donnees()
        
        print("\n" + "="*50)
        print("✓ SYSTÈME INITIALISÉ AVEC SUCCÈS")
        print("="*50 + "\n")
    
    def _charger_donnees(self) -> None:
        """
        Méthode privée pour orchestrer le pipeline de traitement.
        """
        # Étape 1: Collecte
        donnees_brutes = self.collecteur.collecter_donnees()
        
        # Étape 2: Nettoyage
        donnees_nettoyees = self.nettoyeur.nettoyer(donnees_brutes)
        
        # Étape 3: Transformation
        self.stations, self.donnees = self.transformateur.transformer(donnees_nettoyees)
    
    # ============================================
    # USE CASES
    # ============================================
    
    def obtenir_stations(self) -> List[Station]:
        """
        USE CASE 1: Lister toutes les stations disponibles.
        
        Returns:
            List[Station]: Liste des stations
        """
        return self.stations
    
    def obtenir_donnees_station(self, station_id: str) -> List[DonneeMeteo]:
        """
        USE CASE 2: Obtenir toutes les données météo d'une station spécifique.
        
        Args:
            station_id: Identifiant de la station
            
        Returns:
            List[DonneeMeteo]: Liste des observations météo pour cette station
        """
        return [d for d in self.donnees if d.station_id == station_id]
    
    def afficher_stations(self) -> None:
        """
        Affiche la liste des stations de manière formatée.
        """
        print("\n" + "="*50)
        print("STATIONS DISPONIBLES")
        print("="*50)
        
        if not self.stations:
            print("Aucune station disponible.")
        else:
            for i, station in enumerate(self.stations, 1):
                print(f"\n{i}. {station}")
                print(f"   Coordonnées: {station.latitude}°N, {station.longitude}°E")
                if station.altitude:
                    print(f"   Altitude: {station.altitude}m")
        
        print("\n" + "="*50)
    
    def afficher_donnees_station(self, station_id: str) -> None:
        """
        Affiche les données météo d'une station de manière formatée.
        
        Args:
            station_id: Identifiant de la station
        """
        # Trouver la station
        station = next((s for s in self.stations if s.id == station_id), None)
        
        if not station:
            print(f"\n❌ Station {station_id} non trouvée.")
            return
        
        # Récupérer les données
        donnees = self.obtenir_donnees_station(station_id)
        
        print("\n" + "="*50)
        print(f"DONNÉES MÉTÉO - {station.nom}")
        print("="*50)
        
        if not donnees:
            print("Aucune donnée disponible pour cette station.")
        else:
            for donnee in donnees:
                print(f"\n📅 {donnee.timestamp.strftime('%d/%m/%Y %H:%M')}")
                print(f"   🌡️  Température: {donnee.temperature}°C")
                print(f"   💧 Humidité: {donnee.humidite}%")
                print(f"   📊 Pression: {donnee.pression} hPa")
                print(f"   💨 Vent: {donnee.vitesse_vent} km/h (direction: {donnee.direction_vent}°)")
                print(f"   🌧️  Précipitations: {donnee.precipitation} mm")
        
        print("\n" + "="*50)


# ============================================
# 4. EXEMPLE D'UTILISATION
# ============================================

if __name__ == "__main__":
    # Créer le service avec le chemin vers le dossier data
    # Le dossier "data" doit contenir les fichiers CSV (ex: meteo_compans.csv, meteo_marengo.csv)
    service = ServiceMeteo(dossier_data="data")
    
    # Initialiser le système (collecte, nettoyage, transformation)
    service.initialiser()
    
    # USE CASE 1: Afficher toutes les stations
    service.afficher_stations()
    
    # USE CASE 2: Choisir et afficher les données d'une station
    if service.stations:
        # Afficher les données de la première station
        premiere_station = service.stations[0]
        service.afficher_donnees_station(premiere_station.id)