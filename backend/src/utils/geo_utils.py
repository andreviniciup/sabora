"""
modulo de utilitarios para calculos geograficos
implementa funcoes para calculo de distancia e verificacao de raio usando a formula de haversine
"""

import math
from typing import Union, Dict


# constantes para melhor performance
EARTH_RADIUS_KM = 6371.0
RADIANS_PER_DEGREE = math.pi / 180


def calculate_distance(
    lat1: Union[float, int], 
    lon1: Union[float, int], 
    lat2: Union[float, int], 
    lon2: Union[float, int]
) -> float:
    """
    calcula a distancia entre dois pontos geograficos usando a formula de haversine
    
    Args:
        lat1: latitude do primeiro ponto (em graus decimais)
        lon1: longitude do primeiro ponto (em graus decimais)
        lat2: latitude do segundo ponto (em graus decimais)
        lon2: longitude do segundo ponto (em graus decimais)
    
    Returns:
        float: distancia em quilometros entre os dois pontos
    
    Raises:
        ValueError: se as coordenadas estiverem fora dos limites validos
    
    Example:
        >>> calculate_distance(-9.6498, -35.7089, -9.6500, -35.7090)
        0.0157
    """
    # validar coordenadas de forma mais eficiente
    if not (-90 <= lat1 <= 90 and -90 <= lat2 <= 90):
        raise ValueError("latitude deve estar entre -90 e 90 graus")
    
    if not (-180 <= lon1 <= 180 and -180 <= lon2 <= 180):
        raise ValueError("longitude deve estar entre -180 e 180 graus")
    
    # otimizacao: verificar se os pontos sao identicos
    if lat1 == lat2 and lon1 == lon2:
        return 0.0
    
    # converter graus para radianos (usando constante pre-calculada)
    lat1_rad = lat1 * RADIANS_PER_DEGREE
    lon1_rad = lon1 * RADIANS_PER_DEGREE
    lat2_rad = lat2 * RADIANS_PER_DEGREE
    lon2_rad = lon2 * RADIANS_PER_DEGREE
    
    # diferencas nas coordenadas
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # formula de haversine otimizada
    sin_dlat_half = math.sin(dlat * 0.5)
    sin_dlon_half = math.sin(dlon * 0.5)
    
    a = (sin_dlat_half * sin_dlat_half + 
         math.cos(lat1_rad) * math.cos(lat2_rad) * sin_dlon_half * sin_dlon_half)
    
    # usando atan2 de forma mais eficiente
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # distancia em quilometros
    distance = EARTH_RADIUS_KM * c
    
    return round(distance, 4)


def is_within_radius(
    center_lat: Union[float, int],
    center_lon: Union[float, int],
    target_lat: Union[float, int],
    target_lon: Union[float, int],
    radius_km: Union[float, int]
) -> bool:
    """
    verifica se um ponto esta dentro de um raio especificado de um ponto central
    
    Args:
        center_lat: latitude do ponto central (em graus decimais)
        center_lon: longitude do ponto central (em graus decimais)
        target_lat: latitude do ponto alvo (em graus decimais)
        target_lon: longitude do ponto alvo (em graus decimais)
        radius_km: raio em quilometros
    
    Returns:
        bool: true se o ponto alvo estiver dentro do raio, false caso contrario
    
    Example:
        >>> is_within_radius(-9.6498, -35.7089, -9.6500, -35.7090, 1.0)
        true
    """
    if radius_km < 0:
        raise ValueError("raio deve ser um valor positivo")
    
    # otimizacao: verificacao rapida usando aproximacao retangular
    # para distancias pequenas, evita calculo completo de haversine
    lat_diff = abs(center_lat - target_lat)
    lon_diff = abs(center_lon - target_lon)
    
    # aproximacao rapida: 1 grau ≈ 111 km
    if lat_diff > radius_km / 111 or lon_diff > radius_km / 111:
        return False
    
    distance = calculate_distance(center_lat, center_lon, target_lat, target_lon)
    return distance <= radius_km


def calculate_distance_from_dict(
    point1: Dict[str, Union[float, int]], 
    point2: Dict[str, Union[float, int]]
) -> float:
    """
    calcula a distancia entre dois pontos usando dicionarios com coordenadas
    
    Args:
        point1: dicionario com 'latitude' e 'longitude'
        point2: dicionario com 'latitude' e 'longitude'
    
    Returns:
        float: distancia em quilometros
    
    Example:
        >>> point1 = {'latitude': -9.6498, 'longitude': -35.7089}
        >>> point2 = {'latitude': -9.6500, 'longitude': -35.7090}
        >>> calculate_distance_from_dict(point1, point2)
        0.0157
    """
    # validacao otimizada
    for point, name in [(point1, 'point1'), (point2, 'point2')]:
        if not isinstance(point, dict):
            raise ValueError(f"{name} deve ser um dicionario")
        
        if 'latitude' not in point or 'longitude' not in point:
            raise ValueError(f"{name} deve conter as chaves 'latitude' e 'longitude'")
    
    return calculate_distance(
        point1['latitude'], point1['longitude'],
        point2['latitude'], point2['longitude']
    )


def is_within_radius_from_dict(
    center: Dict[str, Union[float, int]],
    target: Dict[str, Union[float, int]],
    radius_km: Union[float, int]
) -> bool:
    """
    verifica se um ponto esta dentro de um raio usando dicionarios com coordenadas
    
    Args:
        center: dicionario com coordenadas do centro
        target: dicionario com coordenadas do alvo
        radius_km: raio em quilometros
    
    Returns:
        bool: true se estiver dentro do raio
    
    Example:
        >>> center = {'latitude': -9.6498, 'longitude': -35.7089}
        >>> target = {'latitude': -9.6500, 'longitude': -35.7090}
        >>> is_within_radius_from_dict(center, target, 1.0)
        true
    """
    return is_within_radius(
        center['latitude'], center['longitude'],
        target['latitude'], target['longitude'],
        radius_km
    )


def format_distance(distance_km: float) -> str:
    """
    formata a distancia em uma string legivel
    
    Args:
        distance_km: distancia em quilometros
    
    Returns:
        str: string formatada da distancia
    
    Example:
        >>> format_distance(0.5)
        '500 metros'
        >>> format_distance(1.2)
        '1.2 km'
    """
    if distance_km < 0:
        raise ValueError("distancia deve ser um valor positivo")
    
    if distance_km < 1:
        meters = round(distance_km * 1000)
        return f"{meters} metros"
    else:
        return f"{distance_km:.1f} km"


def calculate_bearing(
    lat1: Union[float, int], 
    lon1: Union[float, int], 
    lat2: Union[float, int], 
    lon2: Union[float, int]
) -> float:
    """
    calcula o rumo (bearing) entre dois pontos geograficos
    
    Args:
        lat1, lon1: coordenadas do ponto de origem
        lat2, lon2: coordenadas do ponto de destino
    
    Returns:
        float: rumo em graus (0-360, onde 0° = norte)
    """
    lat1_rad = lat1 * RADIANS_PER_DEGREE
    lat2_rad = lat2 * RADIANS_PER_DEGREE
    dlon_rad = (lon2 - lon1) * RADIANS_PER_DEGREE
    
    y = math.sin(dlon_rad) * math.cos(lat2_rad)
    x = (math.cos(lat1_rad) * math.sin(lat2_rad) - 
         math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon_rad))
    
    bearing_rad = math.atan2(y, x)
    bearing_deg = bearing_rad / RADIANS_PER_DEGREE
    
    # normalizar para 0-360 graus
    return (bearing_deg + 360) % 360
