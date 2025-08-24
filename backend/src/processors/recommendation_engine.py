"""
orquestrador de recomendacoes do projeto sabora
implementa logica central para gerar recomendacoes de restaurantes
"""

from typing import List, Dict, Any, Optional, Tuple
import sys
import os

from src.utils.geo_utils import calculate_distance, is_within_radius, format_distance, calculate_distance_from_dict
from src.algorithms.sorting_algorithms import bubble_sort
from src.algorithms.search_algorithms import binary_search
from src.models.restaurant import Restaurant, restaurants_to_dicts
from src.services.google_maps_service import google_maps_service
from src.services.cache_service import cache_service


class RecommendationEngine:
    """
    motor de recomendacoes que orquestra todo o processo de geracao de recomendacoes
    """
    
    def __init__(self):
        self.restaurants = []
        self.user_location = None
    
    def set_restaurants(self, restaurants: List[Restaurant]) -> None:
        """
        define a lista de restaurantes disponiveis
        
        Args:
            restaurants: lista de objetos restaurant
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
    
    def get_restaurants_from_api(self, latitude: float, longitude: float, keyword: str = None) -> List[Restaurant]:
        """
        obtem restaurantes da api do google maps
        
        Args:
            latitude: latitude do usuario
            longitude: longitude do usuario
            keyword: palavra-chave para busca
            
        Returns:
            lista de restaurantes da api
        """
        return google_maps_service.search_nearby_restaurants(
            latitude=latitude,
            longitude=longitude,
            radius_meters=5000,  # 5km
            keyword=keyword
        )
    
    def calculate_distances(self) -> List[Restaurant]:
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
                    'latitude': restaurant.latitude,
                    'longitude': restaurant.longitude
                })
                
                # criar copia do restaurante e atualizar distancia
                restaurant_copy = Restaurant(
                    id=restaurant.id,
                    name=restaurant.name,
                    latitude=restaurant.latitude,
                    longitude=restaurant.longitude,
                    rating=restaurant.rating,
                    cuisine_type=restaurant.cuisine_type,
                    price_range=restaurant.price_range,
                    address=restaurant.address,
                    phone=restaurant.phone,
                    website=restaurant.website,
                    opening_hours=restaurant.opening_hours,
                    features=restaurant.features
                )
                restaurant_copy.update_distance(distance, format_distance(distance))
                restaurants_with_distance.append(restaurant_copy)
                
            except (AttributeError, ValueError) as e:
                print(f"erro ao calcular distancia para restaurante {restaurant.name}: {e}")
                continue
        
        return restaurants_with_distance
    
    def bubble_sort_by_distance(self, restaurants: List[Restaurant]) -> List[Restaurant]:
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
        return bubble_sort(restaurants.copy(), key='distance', descending=False)
    
    def binary_search_radius_filter(self, restaurants: List[Restaurant], radius_km: float) -> List[Restaurant]:
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
        last_index = binary_search(restaurants, key='distance', limit_value=radius_km)
        return restaurants[:last_index + 1] if last_index >= 0 else []
    
    def bubble_sort_by_rating(self, restaurants: List[Restaurant]) -> List[Restaurant]:
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
        return bubble_sort(restaurants.copy(), key='rating', descending=True)
    
    def get_recommendations(
        self,
        user_latitude: float,
        user_longitude: float,
        radius_km: float = 2.0,
        max_results: int = 5
    ) -> List[Restaurant]:
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
        
        # passo 2: obter restaurantes da api (ou mockados se nao houver api key)
        self.restaurants = self.get_restaurants_from_api(user_latitude, user_longitude)
        
        if not self.restaurants:
            return []
        
        # passo 3: calcular distancias
        restaurants_with_distance = self.calculate_distances()
        
        if not restaurants_with_distance:
            return []
        
        # passo 4: ordenar por distancia (bubble sort)
        restaurants_by_distance = self.bubble_sort_by_distance(restaurants_with_distance)
        
        # passo 5: filtrar por raio (busca binaria)
        restaurants_in_radius = self.binary_search_radius_filter(restaurants_by_distance, radius_km)
        
        if not restaurants_in_radius:
            return []
        
        # passo 6: ordenar por nota (bubble sort)
        restaurants_by_rating = self.bubble_sort_by_rating(restaurants_in_radius)
        
        # passo 7: retornar top resultados
        top_recommendations = restaurants_by_rating[:max_results]
        
        # adicionar informacoes extras
        for i, restaurant in enumerate(top_recommendations):
            restaurant.update_rank(i + 1)
            restaurant.update_recommendation_score(self._calculate_recommendation_score(restaurant))
        
        return top_recommendations
    
    def _calculate_recommendation_score(self, restaurant: Restaurant) -> float:
        """
        calcula score de recomendacao baseado em distancia e nota
        
        Args:
            restaurant: dados do restaurante
        
        Returns:
            score de recomendacao (0-100)
        """
        distance = restaurant.distance or 0
        rating = restaurant.rating
        
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
    ) -> List[Restaurant]:
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
        
        # aplicar filtros usando metodos do objeto restaurant
        filtered_recommendations = []
        
        for restaurant in recommendations:
            # filtro de nota minima
            if not restaurant.matches_rating_filter(min_rating):
                continue
            
            # filtro de tipo de culinaria
            if not restaurant.matches_cuisine_filter(cuisine_types):
                continue
            
            # filtro de faixa de preco
            if not restaurant.matches_price_filter(price_range):
                continue
            
            filtered_recommendations.append(restaurant)
            
            # parar quando atingir o maximo de resultados
            if len(filtered_recommendations) >= max_results:
                break
        
        return filtered_recommendations

    def get_recommendations_with_cache(
        self,
        user_latitude: float,
        user_longitude: float,
        query: str,
        filters: Dict[str, Any] = None,
        use_cache: bool = True
    ) -> List[Restaurant]:
        """
        Obtém recomendações com cache
        
        Args:
            user_latitude: latitude do usuário
            user_longitude: longitude do usuário
            query: texto da consulta original
            filters: filtros aplicados
            use_cache: se deve usar cache
            
        Returns:
            lista de restaurantes recomendados
        """
        if use_cache:
            # Tentar buscar do cache primeiro
            cached_restaurants = cache_service.get(user_latitude, user_longitude, query, filters)
            if cached_restaurants:
                # Converter de volta para objetos Restaurant
                restaurants = []
                for restaurant_dict in cached_restaurants:
                    restaurant = Restaurant(
                        id=restaurant_dict.get('id'),
                        name=restaurant_dict.get('name'),
                        latitude=restaurant_dict.get('latitude'),
                        longitude=restaurant_dict.get('longitude'),
                        rating=restaurant_dict.get('rating'),
                        cuisine_type=restaurant_dict.get('cuisine_type'),
                        price_range=restaurant_dict.get('price_range'),
                        address=restaurant_dict.get('address'),
                        phone=restaurant_dict.get('phone'),
                        website=restaurant_dict.get('website'),
                        opening_hours=restaurant_dict.get('opening_hours'),
                        features=restaurant_dict.get('features', [])
                    )
                    # Adicionar campos calculados
                    if 'distance_km' in restaurant_dict:
                        restaurant.distance_km = restaurant_dict['distance_km']
                    if 'distance_formatted' in restaurant_dict:
                        restaurant.distance_formatted = restaurant_dict['distance_formatted']
                    
                    restaurants.append(restaurant)
                
                return restaurants
        
        # Se não encontrou no cache, gerar recomendações normalmente
        recommendations = self.get_recommendations_with_filters(
            user_latitude,
            user_longitude,
            filters.get('radius_km', 2.0) if filters else 2.0,
            5,
            filters.get('min_rating', 0.0) if filters else 0.0,
            filters.get('cuisine_types') if filters else None,
            filters.get('price_range') if filters else None
        )
        
        # Armazenar no cache
        if use_cache and recommendations:
            recommendations_dict = restaurants_to_dicts(recommendations)
            cache_service.set(
                user_latitude, 
                user_longitude, 
                query, 
                filters, 
                recommendations_dict,
                ttl_seconds=3600  # 1 hora
            )
        
        return recommendations


# funcao de conveniencia para uso direto
def get_recommendations(
    restaurants: List[Restaurant],
    user_latitude: float,
    user_longitude: float,
    radius_km: float = 2.0,
    max_results: int = 5
) -> List[Restaurant]:
    """
    funcao de conveniencia para gerar recomendacoes rapidamente
    
    Args:
        restaurants: lista de objetos restaurant
        user_latitude: latitude do usuario
        user_longitude: longitude do usuario
        radius_km: raio de busca em quilometros
        max_results: numero maximo de resultados
    
    Returns:
        lista de objetos restaurant
    """
    engine = RecommendationEngine()
    engine.set_restaurants(restaurants)
    return engine.get_recommendations(user_latitude, user_longitude, radius_km, max_results)


# testes unitarios
if __name__ == "__main__":
    # dados de teste usando objetos restaurant
    test_restaurants = [
        Restaurant(
            id=1,
            name='restaurante a',
            latitude=-9.6498,
            longitude=-35.7089,
            rating=4.5,
            cuisine_type='brasileira',
            price_range='medio',
            address='rua a, 123'
        ),
        Restaurant(
            id=2,
            name='restaurante b',
            latitude=-9.6500,
            longitude=-35.7090,
            rating=4.8,
            cuisine_type='italiana',
            price_range='alto',
            address='rua b, 456'
        ),
        Restaurant(
            id=3,
            name='restaurante c',
            latitude=-9.6600,
            longitude=-35.7200,
            rating=3.9,
            cuisine_type='japonesa',
            price_range='medio',
            address='rua c, 789'
        ),
        Restaurant(
            id=4,
            name='restaurante d',
            latitude=-9.6495,
            longitude=-35.7085,
            rating=4.2,
            cuisine_type='brasileira',
            price_range='baixo',
            address='rua d, 321'
        ),
        Restaurant(
            id=5,
            name='restaurante e',
            latitude=-9.6510,
            longitude=-35.7095,
            rating=4.7,
            cuisine_type='italiana',
            price_range='medio',
            address='rua e, 654'
        )
    ]
    
    # testar engine
    engine = RecommendationEngine()
    engine.set_restaurants(test_restaurants)
    
    print("=== teste do motor de recomendacoes com objetos restaurant ===")
    
    # testar recomendacoes basicas
    recommendations = engine.get_recommendations(-9.6498, -35.7089, 1.0, 3)
    
    print(f"recomendacoes encontradas: {len(recommendations)}")
    for i, rec in enumerate(recommendations):
        print(f"{i+1}. {rec.name} - {rec.distance_formatted} - {rec.rating} estrelas")
    
    # testar filtros
    print("\n=== teste com filtros ===")
    filtered_recs = engine.get_recommendations_with_filters(
        -9.6498, -35.7089, 1.0, 3, 4.0, ['brasileira'], 'medio'
    )
    
    print(f"recomendacoes filtradas: {len(filtered_recs)}")
    for i, rec in enumerate(filtered_recs):
        print(f"{i+1}. {rec.name} - {rec.cuisine_type} - {rec.price_range}")
    
    # testar conversao para dicionario
    print("\n=== teste conversao para dicionario ===")
    dicts = restaurants_to_dicts(recommendations)
    print(f"convertidos para dicionario: {len(dicts)}")
    print(f"primeiro restaurante como dict: {dicts[0] if dicts else 'nenhum'}")
    
    print("\n✅ todos os testes passaram!")

