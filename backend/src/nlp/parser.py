import re
from typing import Dict, List, Any, Optional


class QueryParser:
    """
    parser para converter consultas em portugues natural para filtros estruturados
    """
    
    def __init__(self):
        """
        inicializa o parser com dicionarios de sinonimos vazios
        os dicionarios serao preenchidos posteriormente
        """
        # dicionarios de sinonimos (serao preenchidos depois)
        self.cuisine_synonyms = {} 
        self.price_synonyms = {}   
        self.distance_synonyms = {} 
        self.rating_synonyms = {}  
        
        # padroes regex para capturar informacoes especificas
        self.distance_pattern = re.compile(r'(\d+)\s*(km|quilometros?)', re.IGNORECASE)
        self.rating_pattern = re.compile(r'(nota|estrela).*?(\d+)', re.IGNORECASE)
        self.open_now_pattern = re.compile(r'(aberto|funcionando)', re.IGNORECASE)
    
    def set_cuisine_synonyms(self, synonyms: Dict[str, List[str]]) -> None:
        """
        define o dicionario de sinonimos de culinaria
        
        Args:
            synonyms: dicionario com tipo de culinaria como chave e lista de sinonimos como valor
        """
        self.cuisine_synonyms = synonyms
    
    def set_price_synonyms(self, synonyms: Dict[str, List[str]]) -> None:
        """
        define o dicionario de sinonimos de preco
        
        Args:
            synonyms: dicionario com faixa de preco como chave e lista de sinonimos como valor
        """
        self.price_synonyms = synonyms
    
    def set_distance_synonyms(self, synonyms: Dict[str, List[str]]) -> None:
        """
        define o dicionario de sinonimos de distancia
        
        Args:
            synonyms: dicionario com tipo de distancia como chave e lista de sinonimos como valor
        """
        self.distance_synonyms = synonyms
    
    def set_rating_synonyms(self, synonyms: Dict[str, List[str]]) -> None:
        """
        define o dicionario de sinonimos de avaliacao
        
        Args:
            synonyms: dicionario com tipo de avaliacao como chave e lista de sinonimos como valor
        """
        self.rating_synonyms = synonyms
    
    def _find_cuisine_types(self, text: str) -> List[str]:
        """
        encontra tipos de culinaria no texto usando sinonimos
        
        Args:
            text: texto da consulta
            
        Returns:
            lista de tipos de culinaria encontrados
        """
        if not self.cuisine_synonyms:
            return []
        
        found_cuisines = []
        text_lower = text.lower()
        
        for cuisine_type, synonyms in self.cuisine_synonyms.items():
            for synonym in synonyms:
                if synonym.lower() in text_lower:
                    found_cuisines.append(cuisine_type)
                    break
        
        return list(set(found_cuisines))  # remove duplicatas
    
    def _find_price_range(self, text: str) -> Optional[str]:
        """
        encontra faixa de preco no texto usando sinonimos
        
        Args:
            text: texto da consulta
            
        Returns:
            faixa de preco encontrada ou None
        """
        if not self.price_synonyms:
            return None
        
        text_lower = text.lower()
        
        for price_range, synonyms in self.price_synonyms.items():
            for synonym in synonyms:
                if synonym.lower() in text_lower:
                    return price_range
        
        return None
    
    def _find_distance(self, text: str) -> Optional[float]:
        """
        encontra distancia no texto usando regex
        
        Args:
            text: texto da consulta
            
        Returns:
            distancia em km ou None
        """
        # procurar por padrao numerico (ex: "2 km", "3 quilometros")
        match = self.distance_pattern.search(text)
        if match:
            return float(match.group(1))
        
        # procurar por sinonimos de "perto" (padrao: 2km)
        if self.distance_synonyms:
            text_lower = text.lower()
            for distance_type, synonyms in self.distance_synonyms.items():
                for synonym in synonyms:
                    if synonym.lower() in text_lower:
                        # valores padrao baseados no tipo de distancia
                        if distance_type == "perto":
                            return 2.0
                        elif distance_type == "medio":
                            return 5.0
                        elif distance_type == "longe":
                            return 10.0
        
        return None
    
    def _find_min_rating(self, text: str) -> Optional[float]:
        """
        encontra nota minima no texto
        
        Args:
            text: texto da consulta
            
        Returns:
            nota minima ou None
        """
        # procurar por padrao de nota (ex: "nota 4", "estrela 4")
        match = self.rating_pattern.search(text)
        if match:
            return float(match.group(2))
        
        # procurar por sinonimos de avaliacao
        if self.rating_synonyms:
            text_lower = text.lower()
            for rating_type, synonyms in self.rating_synonyms.items():
                for synonym in synonyms:
                    if synonym.lower() in text_lower:
                        # valores padrao baseados no tipo de avaliacao
                        if rating_type == "bom":
                            return 4.0
                        elif rating_type == "otimo":
                            return 4.5
                        elif rating_type == "excelente":
                            return 5.0
        
        return None
    
    def _find_open_now(self, text: str) -> bool:
        """
        verifica se a consulta menciona "aberto agora"
        
        Args:
            text: texto da consulta
            
        Returns:
            true se mencionar que deve estar aberto
        """
        return bool(self.open_now_pattern.search(text))
    
    def parse_query(self, text: str) -> Dict[str, Any]:
        """
        converte consulta em portugues natural para filtros estruturados
        
        Args:
            text: consulta do usuario (ex: "quero uma italiana barata perto de mim")
            
        Returns:
            dicionario com filtros estruturados
        """
        if not text or not text.strip():
            return {}
        
        # normalizar texto
        text = text.strip()
        
        # extrair informacoes
        cuisine_types = self._find_cuisine_types(text)
        price_range = self._find_price_range(text)
        distance = self._find_distance(text)
        min_rating = self._find_min_rating(text)
        open_now = self._find_open_now(text)
        
        # construir resultado
        result = {}
        
        if cuisine_types:
            result['cuisine_types'] = cuisine_types
        
        if price_range:
            result['price_range'] = price_range
        
        if distance:
            result['radius_km'] = distance
        
        if min_rating:
            result['min_rating'] = min_rating
        
        if open_now:
            result['open_now'] = open_now
        
        return result

