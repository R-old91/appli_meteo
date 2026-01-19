"""
CSV Reader - Utilitaire pour lire les fichiers CSV
Principe: DRY - Centralise la logique de lecture CSV
"""
import csv
from pathlib import Path
from typing import List, Dict


def read_csv(file_path: str, delimiter: str = ';') -> List[Dict[str, str]]:
    """
    Lit un fichier CSV et retourne une liste de dictionnaires.
    
    Args:
        file_path: Chemin vers le fichier CSV
        delimiter: Délimiteur utilisé dans le CSV (par défaut ';')
        
    Returns:
        Liste de dictionnaires où chaque clé est un nom de colonne
        
    Raises:
        FileNotFoundError: Si le fichier n'existe pas
        ValueError: Si le fichier est vide ou mal formaté
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Le fichier {file_path} n'existe pas")
    
    data = []
    
    try:
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=delimiter)
            data = list(reader)
            
        if not data:
            raise ValueError(f"Le fichier {file_path} est vide")
            
        return data
        
    except csv.Error as e:
        raise ValueError(f"Erreur lors de la lecture du fichier CSV: {e}")
    except Exception as e:
        raise ValueError(f"Erreur inattendue lors de la lecture du fichier: {e}")
