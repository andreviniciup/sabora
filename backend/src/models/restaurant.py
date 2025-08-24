"""
modelo de dados para restaurantes do projeto sabora
define a estrutura de dados central para restaurantes
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict, field


@dataclass
class Restaurant:
    """
    modelo de dados para restaurantes
    
    Attributes:
        id: identificador unico do restaurante
        name: nome do restaurante
        latitude: latitude em graus decimais
        longitude: longitude em graus decimais
        rating: nota media (0-5)
        cuisine_type: tipo de culinaria
        price_range: faixa de preco (baixo, medio, alto)
        address: endereco completo
        phone: telefone de contato
        website: site do restaurante
        opening_hours: horarios de funcionamento
        features: lista de caracteristicas especiais
        distance: distancia calculada do usuario (em km)
        distance_formatted: distancia formatada para exibicao
        rank: posicao na lista de recomendacoes
        recommendation_score: score de recomendacao (0-100)
    """
    
    id: int
    name: str
    latitude: float
    longitude: float
    rating: float
    cuisine_type: str
    price_range: str
    address: str
    phone: Optional[str] = None
    website: Optional[str] = None
    opening_hours: Optional[str] = None
    features: List[str] = field(default_factory=list)
    distance: Optional[float] = None
    distance_formatted: Optional[str] = None
    rank: Optional[int] = None
    recommendation_score: Optional[float] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        converte o objeto para dicionario
        
        Returns:
            dicionario com os dados do restaurante
        """
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Restaurant':
        """
        cria um objeto restaurant a partir de um dicionario
        
        Args:
            data: dicionario com dados do restaurante
            
        Returns:
            objeto restaurant
        """
        return cls(**data)
    
    def update_distance(self, distance: float, distance_formatted: str) -> None:
        """
        atualiza a distancia do restaurante
        
        Args:
            distance: distancia em quilometros
            distance_formatted: distancia formatada
        """
        self.distance = distance
        self.distance_formatted = distance_formatted
    
    def update_rank(self, rank: int) -> None:
        """
        atualiza a posicao do restaurante na lista
        
        Args:
            rank: posicao na lista
        """
        self.rank = rank
    
    def update_recommendation_score(self, score: float) -> None:
        """
        atualiza o score de recomendacao
        
        Args:
            score: score de recomendacao (0-100)
        """
        self.recommendation_score = score
    
    def is_within_radius(self, center_lat: float, center_lon: float, radius_km: float) -> bool:
        """
        verifica se o restaurante esta dentro de um raio
        
        Args:
            center_lat: latitude do centro
            center_lon: longitude do centro
            radius_km: raio em quilometros
            
        Returns:
            true se estiver dentro do raio
        """
        if self.distance is None:
            return False
        return self.distance <= radius_km
    
    def matches_cuisine_filter(self, cuisine_types: List[str]) -> bool:
        """
        verifica se o restaurante atende ao filtro de culinaria
        
        Args:
            cuisine_types: tipos de culinaria desejados
            
        Returns:
            true se atender ao filtro
        """
        if not cuisine_types:
            return True
        
        restaurant_cuisine = self.cuisine_type.lower()
        
        # Verificar se algum dos tipos de culinária desejados está presente no restaurante
        for cuisine in cuisine_types:
            cuisine_lower = cuisine.lower()
            
            # Verificar se o tipo de culinária está contido no nome do tipo do restaurante
            if cuisine_lower in restaurant_cuisine:
                return True
            
            # Verificar correspondências específicas
            cuisine_matches = {
                'japonesa': ['japonesa', 'japonês', 'japanese', 'sushi', 'temaki', 'sashimi', 'yaki', 'izakaya', 'oriental'],
                'italiana': ['italiana', 'italian', 'pizza', 'pasta'],
                'chinesa': ['chinesa', 'chinese', 'dim sum'],
                'brasileira': ['brasileira', 'brazilian', 'brasileiro', 'pastel', 'pastelaria', 'churrasco', 'churrascaria', 'feijoada', 'nordestina', 'nordestino', 'regional'],
                'mexicana': ['mexicana', 'mexican', 'taco', 'burrito'],
                'indiana': ['indiana', 'indian', 'curry'],
                'árabe': ['árabe', 'arabic', 'kebab', 'shawarma'],
                'mediterrânea': ['mediterrânea', 'mediterranean', 'hummus'],
                'frutos do mar': ['frutos do mar', 'seafood', 'peixe', 'camarão', 'ceviche'],
                'vegana': ['vegana', 'vegan', 'vegetariana', 'vegetarian'],
                'fast food': ['fast food', 'fast-food', 'hamburguer'],
                'padaria': ['padaria', 'bakery', 'pão'],
                'café': ['café', 'cafe', 'coffee'],
                'bar': ['bar', 'pub', 'cervejaria']
            }
            
            if cuisine_lower in cuisine_matches:
                for match_term in cuisine_matches[cuisine_lower]:
                    if match_term in restaurant_cuisine:
                        return True
        
        return False
    
    def matches_price_filter(self, price_range: str) -> bool:
        """
        verifica se o restaurante atende ao filtro de preco
        
        Args:
            price_range: faixa de preco desejada
            
        Returns:
            true se atender ao filtro
        """
        if not price_range:
            return True
        
        return self.price_range.lower() == price_range.lower()
    
    def matches_rating_filter(self, min_rating: float) -> bool:
        """
        verifica se o restaurante atende ao filtro de nota
        
        Args:
            min_rating: nota minima desejada
            
        Returns:
            true se atender ao filtro
        """
        return self.rating >= min_rating





# funcoes utilitarias para trabalhar com listas de restaurantes
def restaurants_to_dicts(restaurants: List[Restaurant]) -> List[Dict[str, Any]]:
    """
    converte lista de objetos restaurant para lista de dicionarios
    
    Args:
        restaurants: lista de objetos restaurant
        
    Returns:
        lista de dicionarios
    """
    return [restaurant.to_dict() for restaurant in restaurants]


def dicts_to_restaurants(data_list: List[Dict[str, Any]]) -> List[Restaurant]:
    """
    converte lista de dicionarios para lista de objetos restaurant
    
    Args:
        data_list: lista de dicionarios
        
    Returns:
        lista de objetos restaurant
    """
    return [Restaurant.from_dict(data) for data in data_list]
