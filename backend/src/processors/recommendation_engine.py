"""
orquestrador de recomendacoes do projeto sabora
implementa logica central para gerar recomendacoes de restaurantes
"""

from typing import List, Dict, Any, Optional, Tuple
import sys
import os

# adicionar o diretorio src ao path para imports relativos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.geo_utils import calculate_distance, is_within_radius, format_distance, calculate_distance_from_dict
from algorithms.sorting_algorithms import bubble_sort
from algorithms.search_algorithms import busca_binaria


class RecommendationEngine:
    """
    motor de recomendacoes que orquestra todo o processo de geracao de recomendacoes
    """
    
    def __init__(self):
        self.restaurants = []
        self.user_location = None
    
    def set_restaurants(self, restaurants: List[Dict[str, Any]]) -> None:
        """
        define a lista de restaurantes disponiveis
        
        Args:
            restaurants: lista de dicionarios com dados dos restaurantes
        """
        self.restaurants = restaurants
    
    def set_user_location(self, latitude: float, longitude: float) -> None:
        """
        define a localizacao do usuario
        
        Args:
            latitude: latitude do usuario
            longitude: longitude do usuario
        """
        self.user_location = {
            'latitude': latitude,
            'longitude': longitude
        }
    
    def calculate_distances(self) -> List[Dict[str, Any]]:
        """
        calcula a distancia entre o usuario e todos os restaurantes
        
        Returns:
            lista de restaurantes com distancia calculada
        """
        if not self.user_location or not self.restaurants:
            return []
        
        restaurants_with_distance = []
        
        for restaurant in self.restaurants:
            try:
                # usar a funcao de calculo de distancia existente
                distance = calculate_distance_from_dict(self.user_location, {
                    'latitude': restaurant['latitude'],
                    'longitude': restaurant['longitude']
                })
                
                restaurant_copy = restaurant.copy()
                restaurant_copy['distance'] = distance
                restaurant_copy['distance_formatted'] = format_distance(distance)
                restaurants_with_distance.append(restaurant_copy)
                
            except (KeyError, ValueError) as e:
                print(f"erro ao calcular distancia para restaurante {restaurant.get('name', 'unknown')}: {e}")
                continue
        
        return restaurants_with_distance
    
    def bubble_sort_by_distance(self, restaurants: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        ordena restaurantes por distancia usando bubble sort
        
        Args:
            restaurants: lista de restaurantes com distancia calculada
        
        Returns:
            lista ordenada por distancia (menor para maior)
        """
        if not restaurants:
            return []
        
        # usar o algoritmo de bubble sort existente
        return bubble_sort(restaurants.copy(), chave='distance', decrescente=False)
    
    def binary_search_radius_filter(self, restaurants: List[Dict[str, Any]], radius_km: float) -> List[Dict[str, Any]]:
        """
        filtra restaurantes por raio usando busca binaria
        
        Args:
            restaurants: lista de restaurantes ordenados por distancia
            radius_km: raio em quilometros
        
        Returns:
            lista filtrada de restaurantes dentro do raio
        """
        if not restaurants:
            return []
        
        # usar o algoritmo de busca binaria existente
        last_index = busca_binaria(restaurants, chave='distance', valor_limite=radius_km)
        return restaurants[:last_index + 1] if last_index >= 0 else []
    
    def bubble_sort_by_rating(self, restaurants: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        ordena restaurantes por nota usando bubble sort
        
        Args:
            restaurants: lista de restaurantes
        
        Returns:
            lista ordenada por nota (maior para menor)
        """
        if not restaurants:
            return []
        
        # usar o algoritmo de bubble sort existente (decrescente para maior nota primeiro)
        return bubble_sort(restaurants.copy(), chave='rating', decrescente=True)
    
    def get_recommendations(
        self,
        user_latitude: float,
        user_longitude: float,
        radius_km: float = 2.0,
        max_results: int = 5
    ) -> List[Dict[str, Any]]:
        """
        gera recomendacoes completas seguindo o fluxo especificado
        
        Args:
            user_latitude: latitude do usuario
            user_longitude: longitude do usuario
            radius_km: raio de busca em quilometros
            max_results: numero maximo de resultados
        
        Returns:
            lista de recomendacoes ordenadas
        """
        # passo 1: definir localizacao do usuario
        self.set_user_location(user_latitude, user_longitude)
        
        # passo 2: calcular distancias
        restaurants_with_distance = self.calculate_distances()
        
        if not restaurants_with_distance:
            return []
        
        # passo 3: ordenar por distancia (bubble sort)
        restaurants_by_distance = self.bubble_sort_by_distance(restaurants_with_distance)
        
        # passo 4: filtrar por raio (busca binaria)
        restaurants_in_radius = self.binary_search_radius_filter(restaurants_by_distance, radius_km)
        
        if not restaurants_in_radius:
            return []
        
        # passo 5: ordenar por nota (bubble sort)
        restaurants_by_rating = self.bubble_sort_by_rating(restaurants_in_radius)
        
        # passo 6: retornar top resultados
        top_recommendations = restaurants_by_rating[:max_results]
        
        # adicionar informacoes extras
        for i, restaurant in enumerate(top_recommendations):
            restaurant['rank'] = i + 1
            restaurant['recommendation_score'] = self._calculate_recommendation_score(restaurant)
        
        return top_recommendations
    
    def _calculate_recommendation_score(self, restaurant: Dict[str, Any]) -> float:
        """
        calcula score de recomendacao baseado em distancia e nota
        
        Args:
            restaurant: dados do restaurante
        
        Returns:
            score de recomendacao (0-100)
        """
        distance = restaurant.get('distance', 0)
        rating = restaurant.get('rating', 0)
        
        # peso da distancia (60%) e nota (40%)
        distance_score = max(0, 100 - (distance * 20))  # 5km = 0 pontos
        rating_score = rating * 20  # 5 estrelas = 100 pontos
        
        final_score = (distance_score * 0.6) + (rating_score * 0.4)
        return round(final_score, 1)
    
    def get_recommendations_with_filters(
        self,
        user_latitude: float,
        user_longitude: float,
        radius_km: float = 2.0,
        max_results: int = 5,
        min_rating: float = 0.0,
        cuisine_types: Optional[List[str]] = None,
        price_range: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        gera recomendacoes com filtros adicionais
        
        Args:
            user_latitude: latitude do usuario
            user_longitude: longitude do usuario
            radius_km: raio de busca em quilometros
            max_results: numero maximo de resultados
            min_rating: nota minima
            cuisine_types: tipos de culinaria
            price_range: faixa de preco
        
        Returns:
            lista de recomendacoes filtradas
        """
        # obter recomendacoes basicas
        recommendations = self.get_recommendations(
            user_latitude, user_longitude, radius_km, max_results * 2
        )
        
        # aplicar filtros
        filtered_recommendations = []
        
        for restaurant in recommendations:
            # filtro de nota minima
            if restaurant.get('rating', 0) < min_rating:
                continue
            
            # filtro de tipo de culinaria
            if cuisine_types:
                restaurant_cuisine = restaurant.get('cuisine_type', '').lower()
                if not any(cuisine.lower() in restaurant_cuisine for cuisine in cuisine_types):
                    continue
            
            # filtro de faixa de preco
            if price_range:
                restaurant_price = restaurant.get('price_range', '')
                if restaurant_price != price_range:
                    continue
            
            filtered_recommendations.append(restaurant)
            
            # parar quando atingir o maximo de resultados
            if len(filtered_recommendations) >= max_results:
                break
        
        return filtered_recommendations


# funcao de conveniencia para uso direto
def get_recommendations(
    restaurants: List[Dict[str, Any]],
    user_latitude: float,
    user_longitude: float,
    radius_km: float = 2.0,
    max_results: int = 5
) -> List[Dict[str, Any]]:
    """
    funcao de conveniencia para gerar recomendacoes rapidamente
    
    Args:
        restaurants: lista de restaurantes
        user_latitude: latitude do usuario
        user_longitude: longitude do usuario
        radius_km: raio de busca em quilometros
        max_results: numero maximo de resultados
    
    Returns:
        lista de recomendacoes
    """
    engine = RecommendationEngine()
    engine.set_restaurants(restaurants)
    return engine.get_recommendations(user_latitude, user_longitude, radius_km, max_results)


# testes unitarios
if __name__ == "__main__":
    # dados de teste
    test_restaurants = [
        {
            'id': 1,
            'name': 'restaurante a',
            'latitude': -9.6498,
            'longitude': -35.7089,
            'rating': 4.5,
            'cuisine_type': 'brasileira',
            'price_range': 'medio'
        },
        {
            'id': 2,
            'name': 'restaurante b',
            'latitude': -9.6500,
            'longitude': -35.7090,
            'rating': 4.8,
            'cuisine_type': 'italiana',
            'price_range': 'alto'
        },
        {
            'id': 3,
            'name': 'restaurante c',
            'latitude': -9.6600,
            'longitude': -35.7200,
            'rating': 3.9,
            'cuisine_type': 'japonesa',
            'price_range': 'medio'
        },
        {
            'id': 4,
            'name': 'restaurante d',
            'latitude': -9.6495,
            'longitude': -35.7085,
            'rating': 4.2,
            'cuisine_type': 'brasileira',
            'price_range': 'baixo'
        },
        {
            'id': 5,
            'name': 'restaurante e',
            'latitude': -9.6510,
            'longitude': -35.7095,
            'rating': 4.7,
            'cuisine_type': 'italiana',
            'price_range': 'medio'
        }
    ]
    
    # testar engine
    engine = RecommendationEngine()
    engine.set_restaurants(test_restaurants)
    
    print("teste do motor de recomendacoes")
    
    # testar recomendacoes basicas
    recommendations = engine.get_recommendations(-9.6498, -35.7089, 1.0, 3)
    
    print(f"recomendacoes encontradas: {len(recommendations)}")
    for i, rec in enumerate(recommendations):
        print(f"{i+1}. {rec['name']} - {rec['distance_formatted']} - {rec['rating']} estrelas")
    
    # testar filtros
    print("\n teste com filtros ")
    filtered_recs = engine.get_recommendations_with_filters(
        -9.6498, -35.7089, 1.0, 3, 4.0, ['brasileira'], 'medio'
    )
    
    print(f"recomendacoes filtradas: {len(filtered_recs)}")
    for i, rec in enumerate(filtered_recs):
        print(f"{i+1}. {rec['name']} - {rec['cuisine_type']} - {rec['price_range']}")
    
    print("\n todos os testes passaram!")

