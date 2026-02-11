"""
Data Structures package - Structures de données personnalisées

Ce package contient les structures de données implémentées manuellement
à des fins pédagogiques :
    - LinkedList : Liste chaînée simple
    - Queue : File d'attente (FIFO)
    - WeatherDict : Dictionnaire personnalisé (table de hachage)
"""
from .linked_list import Node, LinkedList
from .queue import Queue
from .weather_dict import WeatherDict

__all__ = ['Node', 'LinkedList', 'Queue', 'WeatherDict']
