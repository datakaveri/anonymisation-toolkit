"""
A toolkit for data anonymisation.
"""
__version__ = "0.1.2.3"


'''Functions to be exposed to user'''
from src.cdpg_anonkit.sanitisation import *
from src.cdpg_anonkit.generalisation import *
from src.cdpg_anonkit.aggregation import *

__all__ = [
    'SanitiseData',
    'GeneraliseData',
    'IncrementalGroupbyAggregator',
    'get_final_result',
    'process_chunk',
    'sanitise_data',
    'format_coordinates',
    'generalise_spatial',
    'generalise_temporal',
    'generalise_categorical'
]
