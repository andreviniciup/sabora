"""
servico para integracao com google maps platform
implementa busca de restaurantes usando google places api
"""

import os
import requests
from typing import List, Dict, Any, Optional
from src.models.restaurant import Restaurant


class GoogleMapsService:
    """
    servico para integracao com google maps platform
    """
    
    def __init__(self, api_key: str = None):
        """
        inicializa o servico com a chave da api
        
        Args:
            api_key: chave da api do google maps (opcional, pode ser lida de variavel de ambiente)
        """
        self.api_key = api_key or os.getenv('GOOGLE_MAPS_API_KEY')
        self.base_url = 'https://maps.googleapis.com/maps/api'
        
        if not self.api_key:
            print("⚠️ AVISO: GOOGLE_MAPS_API_KEY não configurada. Usando dados mockados.")
    
    def search_nearby_restaurants(
        self, 
        latitude: float, 
        longitude: float, 
        radius_meters: int = 2000,
        keyword: str = None,
        type_filter: str = 'restaurant'
    ) -> List[Restaurant]:
        """
        busca restaurantes proximos usando google places api
        
        Args:
            latitude: latitude do ponto central
            longitude: longitude do ponto central
            radius_meters: raio de busca em metros
            keyword: palavra-chave para busca (ex: "italiano", "pizza")
            type_filter: tipo de estabelecimento
            
        Returns:
            lista de objetos restaurant
        """
        if not self.api_key:
            print("⚠️ Usando dados mockados (API key não configurada)")
            return self._get_mock_restaurants(latitude, longitude)
        
        try:
            # construir url da api
            url = f"{self.base_url}/place/nearbysearch/json"
            params = {
                'location': f"{latitude},{longitude}",
                'radius': radius_meters,
                'type': type_filter,
                'key': self.api_key
            }
            
            if keyword:
                params['keyword'] = keyword
            
            # fazer requisição
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] != 'OK':
                print(f"⚠️ Erro na API do Google: {data['status']}")
                return self._get_mock_restaurants(latitude, longitude)
            
            # converter resultados para objetos restaurant
            restaurants = []
            for place in data.get('results', []):
                restaurant = self._place_to_restaurant(place, latitude, longitude)
                if restaurant:
                    restaurants.append(restaurant)
            
            return restaurants
            
        except Exception as e:
            print(f"⚠️ Erro ao buscar restaurantes: {e}")
            return self._get_mock_restaurants(latitude, longitude)
    
    def _place_to_restaurant(self, place: Dict[str, Any], user_lat: float, user_lon: float) -> Optional[Restaurant]:
        """
        converte resultado da api do google para objeto restaurant
        
        Args:
            place: dados do lugar da api do google
            user_lat: latitude do usuario
            user_lon: longitude do usuario
            
        Returns:
            objeto restaurant ou None se invalido
        """
        try:
            # extrair dados basicos
            place_id = place.get('place_id', '')
            name = place.get('name', '')
            rating = place.get('rating', 0.0)
            price_level = place.get('price_level', 0)
            vicinity = place.get('vicinity', '')
            
            # coordenadas
            location = place.get('geometry', {}).get('location', {})
            lat = location.get('lat', 0)
            lng = location.get('lng', 0)
            
            # tipos de culinaria
            types = place.get('types', [])
            cuisine_type = self._extract_cuisine_type(types)
            
            # converter price_level para string
            price_range = self._price_level_to_range(price_level)
            
            # calcular distancia
            from src.utils.geo_utils import calculate_distance, format_distance
            distance = calculate_distance(user_lat, user_lon, lat, lng)
            distance_formatted = format_distance(distance)
            
            # criar objeto restaurant
            restaurant = Restaurant(
                id=hash(place_id) % 1000000,  # id unico baseado no place_id
                name=name,
                latitude=lat,
                longitude=lng,
                rating=rating,
                cuisine_type=cuisine_type,
                price_range=price_range,
                address=vicinity,
                distance=distance,
                distance_formatted=distance_formatted
            )
            
            return restaurant
            
        except Exception as e:
            print(f"⚠️ Erro ao converter lugar para restaurante: {e}")
            return None
    
    def _extract_cuisine_type(self, types: List[str]) -> str:
        """
        extrai tipo de culinaria dos tipos do google
        
        Args:
            types: lista de tipos do google places
            
        Returns:
            tipo de culinaria
        """
        cuisine_mapping = {
            'restaurant': 'Restaurante',
            'italian_restaurant': 'Italiana',
            'japanese_restaurant': 'Japonesa',
            'chinese_restaurant': 'Chinesa',
            'indian_restaurant': 'Indiana',
            'mexican_restaurant': 'Mexicana',
            'thai_restaurant': 'Tailandesa',
            'brazilian_restaurant': 'Brasileira',
            'seafood_restaurant': 'Frutos do Mar',
            'steakhouse': 'Churrascaria',
            'pizza_restaurant': 'Pizzaria',
            'bakery': 'Padaria',
            'cafe': 'Café',
            'bar': 'Bar',
            'fast_food': 'Fast Food'
        }
        
        for type_name in types:
            if type_name in cuisine_mapping:
                return cuisine_mapping[type_name]
        
        return 'Restaurante'
    
    def _price_level_to_range(self, price_level: int) -> str:
        """
        converte price_level do google para faixa de preco
        
        Args:
            price_level: nivel de preco do google (0-4)
            
        Returns:
            faixa de preco
        """
        mapping = {
            0: 'baixo',
            1: 'baixo',
            2: 'medio',
            3: 'medio-alto',
            4: 'alto'
        }
        return mapping.get(price_level, 'medio')
    
    def _get_mock_restaurants(self, latitude: float, longitude: float) -> List[Restaurant]:
        """
        retorna dados mockados quando api nao esta disponivel
        
        Args:
            latitude: latitude do usuario
            longitude: longitude do usuario
            
        Returns:
            lista de restaurantes mockados
        """
        from src.models.restaurant import MOCK_RESTAURANTS
        
        # atualizar distancias dos mockados baseado na localizacao do usuario
        from src.utils.geo_utils import calculate_distance, format_distance
        
        mock_restaurants = []
        for restaurant in MOCK_RESTAURANTS:
            distance = calculate_distance(latitude, longitude, restaurant.latitude, restaurant.longitude)
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
                features=restaurant.features,
                distance=distance,
                distance_formatted=format_distance(distance)
            )
            mock_restaurants.append(restaurant_copy)
        
        return mock_restaurants
    
    def geocode_address(self, address: str) -> Optional[Dict[str, float]]:
        """
        converte endereco em coordenadas usando google geocoding api
        
        Args:
            address: endereco para converter
            
        Returns:
            dicionario com latitude e longitude ou None
        """
        if not self.api_key:
            return None
        
        try:
            url = f"{self.base_url}/geocode/json"
            params = {
                'address': address,
                'key': self.api_key
            }
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            if data['status'] != 'OK' or not data.get('results'):
                return None
            
            location = data['results'][0]['geometry']['location']
            return {
                'latitude': location['lat'],
                'longitude': location['lng']
            }
            
        except Exception as e:
            print(f"⚠️ Erro no geocoding: {e}")
            return None


# instancia global do servico
google_maps_service = GoogleMapsService()
