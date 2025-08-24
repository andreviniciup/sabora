"""
sistema de validação baseado nas regras de negócio
valida entrada de dados e regras do sistema
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass

@dataclass
class ValidationError:
    """erro de validação"""
    field: str
    message: str
    code: str

class BusinessRuleValidator:
    """validador de regras de negócio"""
    
    # constantes das regras de negócio
    MAX_QUERY_LENGTH = 500
    MIN_QUERY_LENGTH = 1
    MAX_RESTAURANT_NAME_LENGTH = 100
    MIN_RESTAURANT_NAME_LENGTH = 3
    MAX_RADIUS_KM = 50.0
    MIN_RADIUS_KM = 0.1
    MAX_RESULTS = 20
    MIN_RATING = 0.0
    MAX_RATING = 5.0
    
    # tipos de culinária oficiais
    VALID_CUISINE_TYPES = {
        'nordestina', 'italiana', 'japonesa', 'brasileira', 'chinesa',
        'árabe', 'portuguesa', 'peruana', 'mediterrânea', 'mexicana',
        'indiana', 'francesa', 'frutos do mar', 'vegana', 'saudável',
        'fast food', 'padaria'
    }
    
    # faixas de preço válidas
    VALID_PRICE_RANGES = {'baixo', 'medio', 'alto'}
    
    def validate_search_query(self, data: Dict[str, Any]) -> List[ValidationError]:
        """
        valida dados de consulta de busca
        
        Args:
            data: dados da consulta
            
        Returns:
            lista de erros de validação
        """
        errors = []
        
        # validar texto da consulta
        text = data.get('text', '').strip()
        if not text:
            errors.append(ValidationError(
                field='text',
                message='texto da consulta é obrigatório',
                code='REQUIRED_FIELD'
            ))
        elif len(text) < self.MIN_QUERY_LENGTH:
            errors.append(ValidationError(
                field='text',
                message=f'texto deve ter pelo menos {self.MIN_QUERY_LENGTH} caractere',
                code='MIN_LENGTH'
            ))
        elif len(text) > self.MAX_QUERY_LENGTH:
            errors.append(ValidationError(
                field='text',
                message=f'texto deve ter no máximo {self.MAX_QUERY_LENGTH} caracteres',
                code='MAX_LENGTH'
            ))
        
        # validar latitude
        latitude = data.get('latitude')
        if latitude is None:
            errors.append(ValidationError(
                field='latitude',
                message='latitude é obrigatória',
                code='REQUIRED_FIELD'
            ))
        elif not isinstance(latitude, (int, float)):
            errors.append(ValidationError(
                field='latitude',
                message='latitude deve ser um número',
                code='INVALID_TYPE'
            ))
        elif not (-90 <= latitude <= 90):
            errors.append(ValidationError(
                field='latitude',
                message='latitude deve estar entre -90 e 90 graus',
                code='OUT_OF_RANGE'
            ))
        
        # validar longitude
        longitude = data.get('longitude')
        if longitude is None:
            errors.append(ValidationError(
                field='longitude',
                message='longitude é obrigatória',
                code='REQUIRED_FIELD'
            ))
        elif not isinstance(longitude, (int, float)):
            errors.append(ValidationError(
                field='longitude',
                message='longitude deve ser um número',
                code='INVALID_TYPE'
            ))
        elif not (-180 <= longitude <= 180):
            errors.append(ValidationError(
                field='longitude',
                message='longitude deve estar entre -180 e 180 graus',
                code='OUT_OF_RANGE'
            ))
        
        return errors
    
    def validate_restaurant(self, restaurant: Dict[str, Any]) -> List[ValidationError]:
        """
        valida dados de restaurante
        
        Args:
            restaurant: dados do restaurante
            
        Returns:
            lista de erros de validação
        """
        errors = []
        
        # validar id
        restaurant_id = restaurant.get('id')
        if restaurant_id is None:
            errors.append(ValidationError(
                field='id',
                message='id é obrigatório',
                code='REQUIRED_FIELD'
            ))
        elif not isinstance(restaurant_id, int):
            errors.append(ValidationError(
                field='id',
                message='id deve ser um número inteiro',
                code='INVALID_TYPE'
            ))
        
        # validar nome
        name = restaurant.get('name', '').strip()
        if not name:
            errors.append(ValidationError(
                field='name',
                message='nome é obrigatório',
                code='REQUIRED_FIELD'
            ))
        elif len(name) < self.MIN_RESTAURANT_NAME_LENGTH:
            errors.append(ValidationError(
                field='name',
                message=f'nome deve ter pelo menos {self.MIN_RESTAURANT_NAME_LENGTH} caracteres',
                code='MIN_LENGTH'
            ))
        elif len(name) > self.MAX_RESTAURANT_NAME_LENGTH:
            errors.append(ValidationError(
                field='name',
                message=f'nome deve ter no máximo {self.MAX_RESTAURANT_NAME_LENGTH} caracteres',
                code='MAX_LENGTH'
            ))
        
        # validar coordenadas
        latitude = restaurant.get('latitude')
        longitude = restaurant.get('longitude')
        
        if latitude is None or longitude is None:
            errors.append(ValidationError(
                field='coordinates',
                message='latitude e longitude são obrigatórias',
                code='REQUIRED_FIELD'
            ))
        else:
            if not (-90 <= latitude <= 90):
                errors.append(ValidationError(
                    field='latitude',
                    message='latitude deve estar entre -90 e 90 graus',
                    code='OUT_OF_RANGE'
                ))
            if not (-180 <= longitude <= 180):
                errors.append(ValidationError(
                    field='longitude',
                    message='longitude deve estar entre -180 e 180 graus',
                    code='OUT_OF_RANGE'
                ))
        
        # validar rating
        rating = restaurant.get('rating')
        if rating is None:
            errors.append(ValidationError(
                field='rating',
                message='rating é obrigatório',
                code='REQUIRED_FIELD'
            ))
        elif not isinstance(rating, (int, float)):
            errors.append(ValidationError(
                field='rating',
                message='rating deve ser um número',
                code='INVALID_TYPE'
            ))
        elif not (self.MIN_RATING <= rating <= self.MAX_RATING):
            errors.append(ValidationError(
                field='rating',
                message=f'rating deve estar entre {self.MIN_RATING} e {self.MAX_RATING}',
                code='OUT_OF_RANGE'
            ))
        
        # validar tipo de culinária
        cuisine_type = restaurant.get('cuisine_type', '').strip()
        if not cuisine_type:
            errors.append(ValidationError(
                field='cuisine_type',
                message='tipo de culinária é obrigatório',
                code='REQUIRED_FIELD'
            ))
        elif cuisine_type.lower() not in {c.lower() for c in self.VALID_CUISINE_TYPES}:
            errors.append(ValidationError(
                field='cuisine_type',
                message=f'tipo de culinária deve ser um dos: {", ".join(sorted(self.VALID_CUISINE_TYPES))}',
                code='INVALID_VALUE'
            ))
        
        # validar faixa de preço
        price_range = restaurant.get('price_range', '').strip()
        if not price_range:
            errors.append(ValidationError(
                field='price_range',
                message='faixa de preço é obrigatória',
                code='REQUIRED_FIELD'
            ))
        elif price_range.lower() not in {p.lower() for p in self.VALID_PRICE_RANGES}:
            errors.append(ValidationError(
                field='price_range',
                message=f'faixa de preço deve ser uma das: {", ".join(sorted(self.VALID_PRICE_RANGES))}',
                code='INVALID_VALUE'
            ))
        
        # validar endereço
        address = restaurant.get('address', '').strip()
        if not address:
            errors.append(ValidationError(
                field='address',
                message='endereço é obrigatório',
                code='REQUIRED_FIELD'
            ))
        
        # validar telefone (opcional)
        phone = restaurant.get('phone')
        if phone and not self._is_valid_phone(phone):
            errors.append(ValidationError(
                field='phone',
                message='telefone deve estar em formato brasileiro válido',
                code='INVALID_FORMAT'
            ))
        
        # validar website (opcional)
        website = restaurant.get('website')
        if website and not self._is_valid_url(website):
            errors.append(ValidationError(
                field='website',
                message='website deve ser uma url válida',
                code='INVALID_FORMAT'
            ))
        
        return errors
    
    def validate_filters(self, filters: Dict[str, Any]) -> List[ValidationError]:
        """
        valida filtros de busca
        
        Args:
            filters: filtros aplicados
            
        Returns:
            lista de erros de validação
        """
        errors = []
        
        # validar raio
        radius_km = filters.get('radius_km')
        if radius_km is not None:
            if not isinstance(radius_km, (int, float)):
                errors.append(ValidationError(
                    field='radius_km',
                    message='raio deve ser um número',
                    code='INVALID_TYPE'
                ))
            elif not (self.MIN_RADIUS_KM <= radius_km <= self.MAX_RADIUS_KM):
                errors.append(ValidationError(
                    field='radius_km',
                    message=f'raio deve estar entre {self.MIN_RADIUS_KM} e {self.MAX_RADIUS_KM} km',
                    code='OUT_OF_RANGE'
                ))
        
        # validar nota mínima
        min_rating = filters.get('min_rating')
        if min_rating is not None:
            if not isinstance(min_rating, (int, float)):
                errors.append(ValidationError(
                    field='min_rating',
                    message='nota mínima deve ser um número',
                    code='INVALID_TYPE'
                ))
            elif not (self.MIN_RATING <= min_rating <= self.MAX_RATING):
                errors.append(ValidationError(
                    field='min_rating',
                    message=f'nota mínima deve estar entre {self.MIN_RATING} e {self.MAX_RATING}',
                    code='OUT_OF_RANGE'
                ))
        
        # validar tipos de culinária
        cuisine_types = filters.get('cuisine_types')
        if cuisine_types is not None:
            if not isinstance(cuisine_types, list):
                errors.append(ValidationError(
                    field='cuisine_types',
                    message='tipos de culinária devem ser uma lista',
                    code='INVALID_TYPE'
                ))
            else:
                for cuisine in cuisine_types:
                    if cuisine.lower() not in {c.lower() for c in self.VALID_CUISINE_TYPES}:
                        errors.append(ValidationError(
                            field='cuisine_types',
                            message=f'tipo de culinária inválido: {cuisine}',
                            code='INVALID_VALUE'
                        ))
        
        # validar faixa de preço
        price_range = filters.get('price_range')
        if price_range is not None:
            if price_range.lower() not in {p.lower() for p in self.VALID_PRICE_RANGES}:
                errors.append(ValidationError(
                    field='price_range',
                    message=f'faixa de preço inválida: {price_range}',
                    code='INVALID_VALUE'
                ))
        
        return errors
    
    def validate_cache_params(self, ttl_seconds: int) -> List[ValidationError]:
        """
        valida parâmetros de cache
        
        Args:
            ttl_seconds: tempo de vida em segundos
            
        Returns:
            lista de erros de validação
        """
        errors = []
        
        if not isinstance(ttl_seconds, int):
            errors.append(ValidationError(
                field='ttl_seconds',
                message='ttl deve ser um número inteiro',
                code='INVALID_TYPE'
            ))
        elif not (60 <= ttl_seconds <= 86400):
            errors.append(ValidationError(
                field='ttl_seconds',
                message='ttl deve estar entre 60 e 86400 segundos (1 min a 24h)',
                code='OUT_OF_RANGE'
            ))
        
        return errors
    
    def _is_valid_phone(self, phone: str) -> bool:
        """valida formato de telefone brasileiro"""
        # padrão para telefones brasileiros
        pattern = r'^(\+55\s?)?(\(?\d{2}\)?\s?)?(\d{4,5}-?\d{4})$'
        return bool(re.match(pattern, phone.strip()))
    
    def _is_valid_url(self, url: str) -> bool:
        """valida formato de url"""
        pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        return bool(re.match(pattern, url.strip()))
    
    def sanitize_query_text(self, text: str) -> str:
        """
        sanitiza texto da consulta
        
        Args:
            text: texto original
            
        Returns:
            texto sanitizado
        """
        # remover caracteres especiais perigosos
        text = re.sub(r'[<>"\']', '', text)
        # remover múltiplos espaços
        text = re.sub(r'\s+', ' ', text)
        # trim
        return text.strip()
    
    def get_business_rules_summary(self) -> Dict[str, Any]:
        """
        retorna resumo das regras de negócio
        
        Returns:
            dicionário com regras
        """
        return {
            'limits': {
                'max_query_length': self.MAX_QUERY_LENGTH,
                'min_query_length': self.MIN_QUERY_LENGTH,
                'max_restaurant_name_length': self.MAX_RESTAURANT_NAME_LENGTH,
                'min_restaurant_name_length': self.MIN_RESTAURANT_NAME_LENGTH,
                'max_radius_km': self.MAX_RADIUS_KM,
                'min_radius_km': self.MIN_RADIUS_KM,
                'max_results': self.MAX_RESULTS,
                'min_rating': self.MIN_RATING,
                'max_rating': self.MAX_RATING
            },
            'valid_cuisine_types': sorted(list(self.VALID_CUISINE_TYPES)),
            'valid_price_ranges': sorted(list(self.VALID_PRICE_RANGES))
        }

# instância global do validador
business_validator = BusinessRuleValidator()
