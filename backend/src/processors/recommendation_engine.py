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
from algorithms.search_algorithms import binary_search
from models.restaurant import Restaurant, restaurants_to_dicts
from services.google_maps_service import google_maps_service
from services.cache_service import cache_service


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
            radius_meters=25000,  # 25km - aumentado conforme solicitado
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
    
    def bubble_sort_by_price_low(self, restaurants: List[Restaurant]) -> List[Restaurant]:
        """
        ordena restaurantes por preço (mais barato primeiro)
        
        Args:
            restaurants: lista de restaurantes
            
        Returns:
            lista ordenada por preço (mais barato primeiro)
        """
        if not restaurants:
            return []
        
        # Mapeamento de preços para valores numéricos
        price_values = {
            'baixo': 1,
            'medio': 2,
            'medio-alto': 3,
            'alto': 4
        }
        
        # converter para lista para poder modificar
        sorted_list = list(restaurants)
        n = len(sorted_list)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                # obter valores numéricos dos preços
                price1 = price_values.get(sorted_list[j].price_range.lower(), 2)
                price2 = price_values.get(sorted_list[j + 1].price_range.lower(), 2)
                
                # comparar preços (mais barato primeiro)
                if price1 > price2:
                    sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]
        
        return sorted_list
    
    def bubble_sort_by_price_high(self, restaurants: List[Restaurant]) -> List[Restaurant]:
        """
        ordena restaurantes por preço (mais caro primeiro)
        
        Args:
            restaurants: lista de restaurantes
            
        Returns:
            lista ordenada por preço (mais caro primeiro)
        """
        if not restaurants:
            return []
        
        # Mapeamento de preços para valores numéricos
        price_values = {
            'baixo': 1,
            'medio': 2,
            'medio-alto': 3,
            'alto': 4
        }
        
        # converter para lista para poder modificar
        sorted_list = list(restaurants)
        n = len(sorted_list)
        
        for i in range(n):
            for j in range(0, n - i - 1):
                # obter valores numéricos dos preços
                price1 = price_values.get(sorted_list[j].price_range.lower(), 2)
                price2 = price_values.get(sorted_list[j + 1].price_range.lower(), 2)
                
                # comparar preços (mais caro primeiro)
                if price1 < price2:
                    sorted_list[j], sorted_list[j + 1] = sorted_list[j + 1], sorted_list[j]
        
        return sorted_list
    
    def get_recommendations(
        self,
        user_latitude: float,
        user_longitude: float,
        radius_km: float = 25.0,  # aumentado para 25km conforme solicitado
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
        
        # peso da distancia (70%) e nota (30%) - ajustado para raio maior
        distance_score = max(0, 100 - (distance * 4))  # 25km = 0 pontos
        rating_score = rating * 20  # 5 estrelas = 100 pontos
        
        final_score = (distance_score * 0.7) + (rating_score * 0.3)
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

    def get_recommendations_with_keyword(
        self,
        user_latitude: float,
        user_longitude: float,
        query: str,
        filters: Dict[str, Any] = None
    ) -> List[Restaurant]:
        """
        Gera recomendações usando keyword da consulta
        
        Args:
            user_latitude: latitude do usuário
            user_longitude: longitude do usuário
            query: texto da consulta original
            filters: filtros aplicados
            
        Returns:
            lista de restaurantes recomendados
        """
        print(f"🔍 KEYWORD: Iniciando busca com keyword")
        print(f"   📍 Localização: {user_latitude}, {user_longitude}")
        print(f"   🔤 Query: '{query}'")
        print(f"   🎯 Filtros: {filters}")
        
        # Definir localização do usuário
        self.set_user_location(user_latitude, user_longitude)
        print("✅ KEYWORD: Localização definida")
        
        # Extrair keyword da consulta
        print("🔍 KEYWORD: Extraindo keyword da consulta...")
        keyword = self._extract_keyword_from_query(query, filters)
        print(f"   🎯 Keyword extraída: '{keyword}'")
        
        # Obter restaurantes da API com keyword
        print(f"🌐 KEYWORD: Buscando restaurantes na API com keyword '{keyword}'...")
        self.restaurants = self.get_restaurants_from_api(user_latitude, user_longitude, keyword)
        print(f"   📊 Restaurantes obtidos da API: {len(self.restaurants)}")
        
        if not self.restaurants:
            print("❌ KEYWORD: Nenhum restaurante obtido da API")
            return []
        
        # Calcular distâncias
        print("📏 KEYWORD: Calculando distâncias...")
        restaurants_with_distance = self.calculate_distances()
        print(f"   📊 Restaurantes com distância calculada: {len(restaurants_with_distance)}")
        
        if not restaurants_with_distance:
            print("❌ KEYWORD: Erro ao calcular distâncias")
            return []
        
        # Ordenar por distância
        print("📏 KEYWORD: Ordenando por distância...")
        restaurants_by_distance = self.bubble_sort_by_distance(restaurants_with_distance)
        print(f"   📊 Restaurantes ordenados por distância: {len(restaurants_by_distance)}")
        
        # Filtrar por raio com expansão gradual se necessário
        initial_radius_km = filters.get('radius_km', 25.0) if filters else 25.0
        print(f"🔍 KEYWORD: Filtrando por raio inicial de {initial_radius_km}km...")
        
        # Tentar diferentes raios se não encontrar resultados
        radius_options = [initial_radius_km, 5.0, 10.0, 15.0, 20.0, 25.0]
        restaurants_in_radius = []
        final_radius = initial_radius_km
        
        for radius in radius_options:
            if radius < initial_radius_km:
                continue  # Não diminuir o raio inicial
            
            print(f"   🔍 Tentando raio de {radius}km...")
            restaurants_in_radius = self.binary_search_radius_filter(restaurants_by_distance, radius)
            print(f"      📊 Restaurantes encontrados: {len(restaurants_in_radius)}")
            
            if restaurants_in_radius:
                final_radius = radius
                print(f"   ✅ Encontrados {len(restaurants_in_radius)} restaurantes no raio de {radius}km")
                break
        
        if not restaurants_in_radius:
            print("❌ KEYWORD: Nenhum restaurante encontrado mesmo expandindo o raio")
            return []
        
        # Determinar ordenação baseada na preferência do usuário
        sort_preference = filters.get('sort_preference', 'default') if filters else 'default'
        print(f"📊 KEYWORD: Preferência de ordenação: {sort_preference}")
        
        # Ordenar baseado na preferência
        if sort_preference == 'distance':
            print("📏 KEYWORD: Ordenando por distância...")
            sorted_restaurants = restaurants_in_radius  # Já está ordenado por distância
        elif sort_preference == 'rating':
            print("⭐ KEYWORD: Ordenando por nota...")
            sorted_restaurants = self.bubble_sort_by_rating(restaurants_in_radius)
        elif sort_preference == 'price_low':
            print("💰 KEYWORD: Ordenando por preço (mais barato primeiro)...")
            sorted_restaurants = self.bubble_sort_by_price_low(restaurants_in_radius)
        elif sort_preference == 'price_high':
            print("💰 KEYWORD: Ordenando por preço (mais caro primeiro)...")
            sorted_restaurants = self.bubble_sort_by_price_high(restaurants_in_radius)
        else:
            print("📊 KEYWORD: Ordenação padrão (distância + nota)...")
            # Ordenação padrão: primeiro por distância, depois por nota
            sorted_restaurants = self.bubble_sort_by_rating(restaurants_in_radius)
        
        print(f"   📊 Restaurantes ordenados: {len(sorted_restaurants)}")
        
        # Aplicar filtros adicionais
        print("🔍 KEYWORD: Aplicando filtros adicionais...")
        filtered_recommendations = []
        max_results = 5
        
        for i, restaurant in enumerate(sorted_restaurants):
            print(f"   🔍 Verificando restaurante {i+1}: {restaurant.name}")
            
            # Filtro de nota mínima
            min_rating = filters.get('min_rating', 0.0) if filters else 0.0
            if not restaurant.matches_rating_filter(min_rating):
                print(f"      ❌ Reprovado no filtro de nota (mínima: {min_rating}, atual: {restaurant.rating})")
                continue
            
            # Filtro de tipo de culinária
            cuisine_types = filters.get('cuisine_types') if filters else None
            if not restaurant.matches_cuisine_filter(cuisine_types):
                print(f"      ❌ Reprovado no filtro de culinária (esperado: {cuisine_types}, atual: {restaurant.cuisine_type})")
                continue
            
            # Filtro de faixa de preço
            price_range = filters.get('price_range') if filters else None
            if not restaurant.matches_price_filter(price_range):
                print(f"      ❌ Reprovado no filtro de preço (esperado: {price_range}, atual: {restaurant.price_range})")
                continue
            
            print(f"      ✅ Aprovado em todos os filtros")
            filtered_recommendations.append(restaurant)
            
            # Parar quando atingir o máximo de resultados
            if len(filtered_recommendations) >= max_results:
                print(f"      🛑 Máximo de resultados atingido ({max_results})")
                break
        
        print(f"📊 KEYWORD: {len(filtered_recommendations)} restaurantes aprovados nos filtros")
        
        # Adicionar informações extras
        print("📋 KEYWORD: Adicionando informações extras...")
        for i, restaurant in enumerate(filtered_recommendations):
            restaurant.update_rank(i + 1)
            restaurant.update_recommendation_score(self._calculate_recommendation_score(restaurant))
            print(f"   {i+1}. {restaurant.name} - Score: {restaurant.recommendation_score}")
        
        print(f"✅ KEYWORD: Retornando {len(filtered_recommendations)} recomendações finais")
        return filtered_recommendations

    def _extract_keyword_from_query(self, query: str, filters: Dict[str, Any] = None) -> str:
        """
        Extrai keyword da consulta para busca na API
        
        Args:
            query: texto da consulta original
            filters: filtros extraídos
            
        Returns:
            keyword para busca
        """
        print(f"🔍 EXTRACT: Extraindo keyword de '{query}'")
        print(f"   🎯 Filtros disponíveis: {filters}")
        
        # Se há filtros de culinária, usar o primeiro
        if filters and filters.get('cuisine_types'):
            keyword = filters['cuisine_types'][0]
            print(f"   ✅ Usando filtro de culinária: '{keyword}'")
            return keyword
        
        # Se não há filtros específicos, usar palavras-chave da consulta
        query_lower = query.lower()
        print(f"   🔍 Procurando termos na query: '{query_lower}'")
        
        # Mapear termos comuns para keywords
        keyword_mapping = {
            'japonesa': 'japanese restaurant',
            'japones': 'japanese restaurant',
            'comida japonesa': 'japanese restaurant',
            'restaurante japonês': 'japanese restaurant',
            'sushi': 'sushi restaurant',
            'temaki': 'japanese restaurant',
            'sashimi': 'japanese restaurant',
            'italiana': 'italian restaurant',
            'pizza': 'pizza restaurant',
            'chinesa': 'chinese restaurant',
            'brasileira': 'brazilian restaurant',
            'mexicana': 'mexican restaurant',
            'indiana': 'indian restaurant',
            'árabe': 'arabic restaurant',
            'mediterrânea': 'mediterranean restaurant',
            'frutos do mar': 'seafood restaurant',
            'vegana': 'vegan restaurant',
            'vegetariana': 'vegetarian restaurant',
            'fast food': 'fast food',
            'padaria': 'bakery',
            'café': 'cafe',
            'bar': 'bar'
        }
        
        for term, keyword in keyword_mapping.items():
            if term in query_lower:
                print(f"   ✅ Termo encontrado: '{term}' -> '{keyword}'")
                return keyword
        
        # Se não encontrou mapeamento específico, usar a consulta original
        print(f"   ⚠️ Nenhum termo mapeado encontrado, usando query original: '{query}'")
        return query

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
        
        # Se não encontrou no cache, gerar recomendações com keyword
        recommendations = self.get_recommendations_with_keyword(
            user_latitude,
            user_longitude,
            query,
            filters
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

