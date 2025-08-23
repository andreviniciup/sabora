"""
modulo de processadores do projeto sabora
"""

from .recommendation_engine import RecommendationEngine, get_recommendations

__all__ = [
    'RecommendationEngine',
    'get_recommendations'
]
