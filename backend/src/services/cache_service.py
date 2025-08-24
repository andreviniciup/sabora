import os
import json
import hashlib
import redis
from typing import Optional, Dict, Any, List
from datetime import timedelta
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CacheService:
    """
    Serviço de cache usando Redis para armazenar resultados de recomendações
    """
    
    def __init__(self, redis_url: str = None):
        """
        Inicializa o serviço de cache
        
        Args:
            redis_url: URL do Redis (opcional, usa variável de ambiente REDIS_URL)
        """
        self.redis_url = redis_url or os.getenv('REDIS_URL', 'redis://localhost:6379/0')
        self.redis_client = None
        self.cache_enabled = True
        
        try:
            self.redis_client = redis.from_url(self.redis_url)
            # Testar conexão
            self.redis_client.ping()
            logger.info("✅ Cache Redis conectado com sucesso")
        except Exception as e:
            logger.warning(f"⚠️ Cache Redis não disponível: {e}")
            logger.info("📝 Usando cache em memória como fallback")
            self.cache_enabled = False
            self.memory_cache = {}
    
    def _generate_cache_key(self, latitude: float, longitude: float, query: str, filters: Dict = None) -> str:
        """
        Gera uma chave única para o cache baseada nos parâmetros da busca
        
        Args:
            latitude: Latitude do usuário
            longitude: Longitude do usuário
            query: Texto da consulta
            filters: Filtros aplicados
            
        Returns:
            Chave única para o cache
        """
        # Criar string com todos os parâmetros
        cache_data = {
            'lat': round(latitude, 6),  # Arredondar para evitar variações mínimas
            'lng': round(longitude, 6),
            'query': query.lower().strip(),
            'filters': filters or {}
        }
        
        # Gerar hash MD5 da string JSON
        cache_string = json.dumps(cache_data, sort_keys=True)
        return f"sabora:recommendations:{hashlib.md5(cache_string.encode()).hexdigest()}"
    
    def get(self, latitude: float, longitude: float, query: str, filters: Dict = None) -> Optional[List[Dict]]:
        """
        Busca resultados no cache
        
        Args:
            latitude: Latitude do usuário
            longitude: Longitude do usuário
            query: Texto da consulta
            filters: Filtros aplicados
            
        Returns:
            Lista de restaurantes do cache ou None se não encontrado
        """
        if not self.cache_enabled:
            return self._get_from_memory(latitude, longitude, query, filters)
        
        try:
            cache_key = self._generate_cache_key(latitude, longitude, query, filters)
            cached_data = self.redis_client.get(cache_key)
            
            if cached_data:
                logger.info(f"🎯 Cache hit para: {query[:30]}...")
                return json.loads(cached_data)
            else:
                logger.info(f"❌ Cache miss para: {query[:30]}...")
                return None
                
        except Exception as e:
            logger.error(f"Erro ao buscar no cache: {e}")
            return None
    
    def set(self, latitude: float, longitude: float, query: str, filters: Dict, 
            restaurants: List[Dict], ttl_seconds: int = 3600) -> bool:
        """
        Armazena resultados no cache
        
        Args:
            latitude: Latitude do usuário
            longitude: Longitude do usuário
            query: Texto da consulta
            filters: Filtros aplicados
            restaurants: Lista de restaurantes para cachear
            ttl_seconds: Tempo de vida em segundos (padrão: 1 hora)
            
        Returns:
            True se armazenado com sucesso, False caso contrário
        """
        if not self.cache_enabled:
            return self._set_in_memory(latitude, longitude, query, filters, restaurants, ttl_seconds)
        
        try:
            cache_key = self._generate_cache_key(latitude, longitude, query, filters)
            cache_data = json.dumps(restaurants, ensure_ascii=False)
            
            # Armazenar no Redis com TTL
            self.redis_client.setex(cache_key, ttl_seconds, cache_data)
            
            logger.info(f"💾 Cache armazenado para: {query[:30]}... (TTL: {ttl_seconds}s)")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao armazenar no cache: {e}")
            return False
    
    def invalidate_by_location(self, latitude: float, longitude: float, radius_km: float = 5.0) -> int:
        """
        Invalida cache para uma localização específica
        
        Args:
            latitude: Latitude central
            longitude: Longitude central
            radius_km: Raio em km para invalidar
            
        Returns:
            Número de chaves invalidadas
        """
        if not self.cache_enabled:
            return 0
        
        try:
            # Buscar todas as chaves do cache
            pattern = "sabora:recommendations:*"
            keys = self.redis_client.keys(pattern)
            
            invalidated_count = 0
            
            for key in keys:
                try:
                    # Recuperar dados da chave para verificar localização
                    cached_data = self.redis_client.get(key)
                    if cached_data:
                        # Aqui você poderia implementar lógica mais sofisticada
                        # para verificar se a localização está no raio
                        # Por simplicidade, vamos invalidar todas as chaves
                        self.redis_client.delete(key)
                        invalidated_count += 1
                except Exception as e:
                    logger.error(f"Erro ao invalidar chave {key}: {e}")
            
            logger.info(f"🗑️ Invalidadas {invalidated_count} chaves de cache")
            return invalidated_count
            
        except Exception as e:
            logger.error(f"Erro ao invalidar cache: {e}")
            return 0
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Retorna estatísticas do cache
        
        Returns:
            Dicionário com estatísticas
        """
        if not self.cache_enabled:
            return {
                'enabled': False,
                'type': 'memory',
                'keys_count': len(self.memory_cache)
            }
        
        try:
            pattern = "sabora:recommendations:*"
            keys = self.redis_client.keys(pattern)
            
            return {
                'enabled': True,
                'type': 'redis',
                'keys_count': len(keys),
                'redis_url': self.redis_url
            }
        except Exception as e:
            logger.error(f"Erro ao obter estatísticas: {e}")
            return {
                'enabled': False,
                'error': str(e)
            }
    
    def clear_all(self) -> bool:
        """
        Limpa todo o cache
        
        Returns:
            True se limpo com sucesso
        """
        if not self.cache_enabled:
            self.memory_cache.clear()
            return True
        
        try:
            pattern = "sabora:recommendations:*"
            keys = self.redis_client.keys(pattern)
            
            if keys:
                self.redis_client.delete(*keys)
                logger.info(f"🧹 Cache limpo: {len(keys)} chaves removidas")
            
            return True
            
        except Exception as e:
            logger.error(f"Erro ao limpar cache: {e}")
            return False
    
    # Métodos para cache em memória (fallback)
    def _get_from_memory(self, latitude: float, longitude: float, query: str, filters: Dict = None) -> Optional[List[Dict]]:
        """Cache em memória como fallback"""
        cache_key = self._generate_cache_key(latitude, longitude, query, filters)
        return self.memory_cache.get(cache_key)
    
    def _set_in_memory(self, latitude: float, longitude: float, query: str, filters: Dict, 
                       restaurants: List[Dict], ttl_seconds: int) -> bool:
        """Armazenar em memória como fallback"""
        cache_key = self._generate_cache_key(latitude, longitude, query, filters)
        self.memory_cache[cache_key] = restaurants
        return True

# Instância global do serviço de cache
cache_service = CacheService()
