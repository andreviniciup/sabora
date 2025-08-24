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
        return any(cuisine.lower() in restaurant_cuisine for cuisine in cuisine_types)
    
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


# Dados mockados de restaurantes para desenvolvimento
MOCK_RESTAURANTS = [
    Restaurant(
        id=1,
        name="Bodega do Sertão",
        latitude=-9.65333,
        longitude=-35.70920,
        rating=4.6,
        cuisine_type="Nordestina / self-service",
        price_range="medio",
        address="Av. Dr. Júlio Marques Luz, 62 — Jatiúca, Maceió-AL",
        phone="(82) 3327-4446",
        opening_hours="Seg-Dom: 11h30-16h, 17h30-22h",
        features=["decoração temática", "buffet self-service", "culinária regional"]
    ),
    Restaurant(
        id=2,
        name="Janga Praia",
        latitude=-9.66328,
        longitude=-35.70562,
        rating=4.8,
        cuisine_type="Brasileira, Frutos do mar",
        price_range="medio-alto",
        address="Av. Silvio Carlos Viana, 1731 — Ponta Verde, Maceió-AL",
        phone="+55 82 98233-1030",
        website="https://linktr.ee/PedidosJanga",
        opening_hours="Dom-Qua: 12h-16h e 18h30-23h; Qui-Sáb: até 00h",
        features=["beira-mar", "frutos do mar", "opções vegetarianas/sem glúten", "entrega"]
    ),
    Restaurant(
        id=3,
        name="Maria Antonieta",
        latitude=-9.65090,
        longitude=-35.70102,
        rating=4.7,
        cuisine_type="Italiana sofisticada",
        price_range="alto",
        address="Av. Dr. Antônio Gomes de Barros, 150 — Jatiúca, Maceió-AL",
        phone="(82) 3202-8828",
        website="https://mariaantonieta-al.com.br/",
        features=["ambiente elegante", "pratos elaborados (raviolone)", "ideal para jantar especial"]
    ),
    Restaurant(
        id=4,
        name="Divina Gula",
        latitude=-9.64632,
        longitude=-35.70491,
        rating=4.6,
        cuisine_type="Mineira / Regional",
        price_range="alto",
        address="Av. Paulo Brandão Nogueira, 85 - Jatiúca, Maceió-AL",
        phone="(82) 3235-1016",
        features=["ambiente acolhedor", "ingredientes frescos", "sofisticado"]
    ),
    Restaurant(
        id=5,
        name="Cheiro da Terra",
        latitude=-9.671455999415862,
        longitude=-35.71602995613105,
        rating=4.6,
        cuisine_type="Nordestina / Buffet",
        price_range="medio",
        address="Av. Dr. Antônio Gouveia, 487 - Pajuçara, Maceió-AL",
        features=["buffet", "ambiente rústico", "música ao vivo", "lojinha"]
    )
]


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
