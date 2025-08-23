"""
modelo de dados para restaurantes do projeto sabora
define a estrutura de dados central para restaurantes
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, asdict


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
    
    id: int = 1
    name: str = "Bodega do Sertão"
    latitude: float = -9.65333
    longitude: float = -35.70920
    rating: float = 4.6
    cuisine_type: str = "Nordestina / self-service"
    price_range: str = "medio"
    address: str = "Av. Dr. Júlio Marques Luz, 62 — Jatiúca, Maceió-AL"
    phone: Optional[str] = "(82) 3327-4446"
    website: Optional[str] = ""
    opening_hours: Optional[str] = "Seg-Dom: 11h30-16h, 17h30-22h"
    features: Optional[List[str]] = ["decoração temática", "buffet self-service", "culinária regional"]
    distance: Optional[float] = None
    distance_formatted: Optional[str] = ""
    rank: Optional[int] = 0
    recommendation_score: Optional[float] = 0

    id: int = 2
    name: str = "Janga Praia"
    latitude: float = -9.66328
    longitude: float = -35.70562
    rating: float = 4.8
    cuisine_type: str = "Brasileira, Frutos do mar"
    price_range: str = "medio-alto"
    address: str = "Av. Silvio Carlos Viana, 1731 — Ponta Verde, Maceió-AL"
    phone: Optional[str] = "+55 82 98233-1030"
    website: Optional[str] = "https://linktr.ee/PedidosJanga"
    opening_hours: Optional[str] = "Dom-Qua: 12h-16h e 18h30-23h; Qui-Sáb: até 00h"
    features: Optional[List[str]] = ["beira-mar", "frutos do mar", "opções vegetarianas/sem glúten", "entrega"]
    distance: Optional[float] = None
    distance_formatted: Optional[str] = ""
    rank: Optional[int] = 0
    recommendation_score: Optional[float] = 0

    id: int = 3
    name: str = "Maria Antonieta"
    latitude: float = -9.65090
    longitude: float = -35.70102
    rating: float = 4.7
    cuisine_type: str = "Italiana sofisticada"
    price_range: str = "alto"
    address: str = "Av. Dr. Antônio Gomes de Barros, 150 — Jatiúca, Maceió-AL"
    phone: Optional[str] = "(82) 3202-8828"
    website: Optional[str] = "https://mariaantonieta-al.com.br/"
    opening_hours: Optional[str] = ""
    features: Optional[List[str]] = ["ambiente elegante", "pratos elaborados (raviolone)", "ideal para jantar especial"]
    distance: Optional[float] = None
    distance_formatted: Optional[str] = ""
    rank: Optional[int] = 0
    recommendation_score: Optional[float] = 0

    id: int = 4
    name: str = "Divina Gula"
    latitude: float = -9.64632
    longitude: float = -35.70491
    rating: float = 4.6
    cuisine_type: str = "Mineira / Regional"
    price_range: str = "alto"
    address: str = "Av. Paulo Brandão Nogueira, 85 - Jatiúca, Maceió-AL"
    phone: Optional[str] = "(82) 3235-1016"
    website: Optional[str] = ""
    opening_hours: Optional[str] = ""
    features: Optional[List[str]] = ["ambiente acolhedor", "ingredientes frescos", "sofisticado"]
    distance: Optional[float] = None
    distance_formatted: Optional[str] = ""
    rank: Optional[int] = 0
    recommendation_score: Optional[float] = 0

    id: int = 5
    name: str = "Cheiro da Terra"
    latitude: float = -9.671455999415862
    longitude: float = -35.71602995613105
    rating: float = 4.6
    cuisine_type: str = "Nordestina / Buffet"
    price_range: str = "medio"
    address: str = "Av. Dr. Antônio Gouveia, 487 - Pajuçara, Maceió-AL"
    phone: Optional[str] = ""
    website: Optional[str] = ""
    opening_hours: Optional[str] = ""
    features: Optional[List[str]] = ["buffet", "ambiente rústico", "música ao vivo", "lojinha"]
    distance: Optional[float] = None
    distance_formatted: Optional[str] = ""
    rank: Optional[int] = 0
    recommendation_score: Optional[float] = 0

    id: int = 6
    name: str = "Micale Restaurante"
    latitude: float = -9.6620031
    longitude: float = -35.7079004
    rating: float = 4.9
    cuisine_type: str = "Mediterrânea / Frutos do mar"
    price_range: str = "alto"
    address: str = "R. Durval Guimarães, 1298 - Ponta Verde, Maceió - AL"
    phone: Optional[str] = ""
    website: Optional[str] = ""
    opening_hours: Optional[str] = ""
    features: Optional[List[str]] = ["vista", "frutos do mar", "vinhos", "coquetéis"]
    distance: Optional[float] = None
    distance_formatted: Optional[str] = ""
    rank: Optional[int] = 0
    recommendation_score: Optional[float] = 0

    id: int = 7
    name: str = "Lopana"
    latitude: float = -9.6638247
    longitude: float = -35.703948
    rating: float = 4.5
    cuisine_type: str = "Frutos do mar / Praia"
    price_range: str = "medio"
    address: str = "Av. Silvio Carlos Viana, 27 - Ponta Verde, Maceió-AL"
    phone: Optional[str] = ""
    website: Optional[str] = ""
    opening_hours: Optional[str] = ""
    features: Optional[List[str]] = ["beira-mar", "peixes fritos", "bebidas refrescantes"]
    distance: Optional[float] = None
    distance_formatted: Optional[str] = ""
    rank: Optional[int] = 0
    recommendation_score: Optional[float] = 0

    id: int = 8
    name: str = "Wanchako"
    latitude: float = -9.6559706
    longitude: float = -35.6999379
    rating: float = 4.5
    cuisine_type: str = "Peruana / Fusão"
    price_range: str = "alto"
    address: str = "Rua Prefeito Abdon Arroxelas, 147 - Ponta Verde, Maceió - AL"
    phone: Optional[str] = ""
    website: Optional[str] = ""
    opening_hours: Optional[str] = ""
    features: Optional[List[str]] = ["ceviche", "lomo saltado", "sofisticado"]
    distance: Optional[float] = None
    distance_formatted: Optional[str] = ""
    rank: Optional[int] = 0
    recommendation_score: Optional[float] = 0

    id: int = 9
    name: str = "759 Parrilla"
    latitude: float = -9.6674273
    longitude: float = -35.713476299999996
    rating: float = 4.7
    cuisine_type: str = "Steakhouse / Carnes"
    price_range: str = "alto"
    address: str = "Av. Dr. Antônio Gouveia, 759 - Pajuçara, Maceió-AL"
    phone: Optional[str] = ""
    website: Optional[str] = ""
    opening_hours: Optional[str] = "Qua-Seg: 11h30-23h30"
    features: Optional[List[str]] = ["cortes nobres", "vinhos", "ambiente aconchegante"]
    distance: Optional[float] = None
    distance_formatted: Optional[str] = ""
    rank: Optional[int] = 0
    recommendation_score: Optional[float] = 0

    id: int = 10
    name: str = "Casa de Mãinha"
    latitude: float = -9.6721042
    longitude: float = -35.72336061581474
    rating: float = 4.5
    cuisine_type: str = "Nordestina / Caseira"
    price_range: str = "baixo"
    address: str = "R. Sá e Albuquerque, 417 - Jaraguá, Maceió - AL"
    phone: Optional[str] = ""
    website: Optional[str] = ""
    opening_hours: Optional[str] = ""
    features: Optional[List[str]] = ["caseira", "custo-benefício", "variado ambiente"]
    distance: Optional[float] = None
    distance_formatted: Optional[str] = ""
    rank: Optional[int] = 0
    recommendation_score: Optional[float] = 0

    id: int = 11
    name: str = "Armazém Guimarães"
    latitude: float = -9.6509629
    longitude: float = -35.70124324984265
    rating: float = 4.6
    cuisine_type: str = "Italiana"
    price_range: Optional[str] = None
    address: str = "Av. Dr. Antônio Gomes de Barros, 188 - Jatiúca, Maceió-AL, Parque Shopping Maceió"
    phone: Optional[str] = "(82) 3325-4545"
    website: Optional[str] = ""
    opening_hours: Optional[str] = ""
    features: Optional[List[str]] = ["pizza", "massas", "pratos tradicionais italianos"]
    distance: Optional[float] = None
    distance_formatted: Optional[str] = ""
    rank: Optional[int] = 0
    recommendation_score: Optional[float] = 0

    id: int = 12
    name: str = "SantOrégano Pizzas e Massas"
    latitude: float = -9.55787404131403
    longitude: float = -35.64056819093656
    rating: float = 4.6
    cuisine_type: str = "Pizzaria"
    price_range: Optional[str] = None
    address: str = "Rodovia AL-101 - Riacho Doce, Maceió-AL"
    phone: Optional[str] = ""
    website: Optional[str] = ""
    opening_hours: Optional[str] = ""
    features: Optional[List[str]] = ["pizza premiada (7ª do Brasil)", "saborosas opções veganas"]
    distance: Optional[float] = None
    distance_formatted: Optional[str] = ""
    rank: Optional[int] = 0
    recommendation_score: Optional[float] = 0

    id: int = 13
    name: str = "Kanoa Beach Bar"
    latitude: float = -9.66390
    longitude: float = -35.70578
    rating: float = 4.3
    cuisine_type: str = "Praia / Petiscos / Bar"
    price_range: Optional[str] = None
    address: str = "Orla de Ponta Verde - Av. Silvio Carlos Viana, 25 - Ponta Verde, Maceió - AL"
    phone: Optional[str] = ""
    website: Optional[str] = ""
    opening_hours: Optional[str] = ""
    features: Optional[List[str]] = ["à beira-mar", "petiscos", "música ao vivo", "aluguel de cadeiras"]
    distance: Optional[float] = None
    distance_formatted: Optional[str] = ""
    rank: Optional[int] = 0
    recommendation_score: Optional[float] = 0

    id: int = 14
    name: str = "Imperador dos Camarões"
    latitude: float = -9.665197
    longitude: float = -35.70998572308537
    rating: float = 4.7
    cuisine_type: str = "Frutos do mar"
    price_range: Optional[str] = None
    address: str = "Av. Dr. Antônio Gouveia, 21 - Pajuçara, Maceió - AL, 57030-170"
    phone: Optional[str] = ""
    website: Optional[str] = ""
    opening_hours: Optional[str] = ""
    features: Optional[List[str]] = ["chiclete de camarão", "variedade de frutos do mar", "custo-benefício"]
    distance: Optional[float] = None
    distance_formatted: Optional[str] = ""
    rank: Optional[int] = 0
    recommendation_score: Optional[float] = 0

    id: int = 15
    name: str = "Picuí"
    latitude: float = -9.669999226855426
    longitude: float = -35.729869603577114
    rating: float = 4.6
    cuisine_type: str = "Carne de sol / Frutos do mar"
    price_range: Optional[str] = None
    address: str = "Av. da Paz, 1140 - Jaraguá, Maceió-AL"
    phone: Optional[str] = ""
    website: Optional[str] = ""
    opening_hours: Optional[str] = ""
    features: Optional[List[str]] = ["carne de sol", "frutos do mar", "chef renomado", "risoto"]
    distance: Optional[float] = None
    distance_formatted: Optional[str] = ""
    rank: Optional[int] = 0
    recommendation_score: Optional[float] = 0
    
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
