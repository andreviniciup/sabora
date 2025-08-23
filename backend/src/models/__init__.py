"""
modulo de modelos de dados do projeto sabora
"""

from .restaurant import (
    Restaurant,
    restaurants_to_dicts,
    dicts_to_restaurants
)

__all__ = [
    'Restaurant',
    'restaurants_to_dicts',
    'dicts_to_restaurants'
]
