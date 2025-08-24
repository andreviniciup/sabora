#!/usr/bin/env python3
"""
Script de teste para o sistema de cache Redis
Testa funcionalidades de cache e performance
"""

import sys
import os
import time
import requests
import json

# Adicionar o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from services.cache_service import cache_service

def test_cache_service():
    """
    Testa o serviço de cache diretamente
    """
    print("🧪 TESTANDO SERVIÇO DE CACHE")
    print("=" * 50)
    
    # Testar estatísticas iniciais
    print("📊 Estatísticas iniciais:")
    stats = cache_service.get_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    print()
    
    # Dados de teste
    test_data = {
        'latitude': -23.5505,
        'longitude': -46.6333,
        'query': 'italiana barata perto de mim',
        'filters': {
            'cuisine_types': ['italiana'],
            'price_range': 'baixo',
            'radius_km': 2.0
        },
        'restaurants': [
            {
                'id': 1,
                'name': 'Pizzaria Bella Italia',
                'rating': 4.5,
                'cuisine_type': 'italiana',
                'price_range': 'baixo',
                'distance_km': 0.8
            },
            {
                'id': 2,
                'name': 'Restaurante Roma',
                'rating': 4.2,
                'cuisine_type': 'italiana',
                'price_range': 'baixo',
                'distance_km': 1.2
            }
        ]
    }
    
    # Teste 1: Armazenar no cache
    print("💾 Teste 1: Armazenando no cache...")
    success = cache_service.set(
        test_data['latitude'],
        test_data['longitude'],
        test_data['query'],
        test_data['filters'],
        test_data['restaurants'],
        ttl_seconds=60  # 1 minuto para teste
    )
    print(f"✅ Armazenamento: {'Sucesso' if success else 'Falha'}")
    print()
    
    # Teste 2: Buscar do cache
    print("🔍 Teste 2: Buscando do cache...")
    cached_data = cache_service.get(
        test_data['latitude'],
        test_data['longitude'],
        test_data['query'],
        test_data['filters']
    )
    
    if cached_data:
        print("✅ Cache hit!")
        print(f"📋 Restaurantes encontrados: {len(cached_data)}")
        for i, restaurant in enumerate(cached_data, 1):
            print(f"   {i}. {restaurant['name']} - ⭐{restaurant['rating']}")
    else:
        print("❌ Cache miss!")
    print()
    
    # Teste 3: Buscar com query diferente (deve dar miss)
    print("🔍 Teste 3: Buscando com query diferente...")
    different_query = "sushi caro"
    cached_data = cache_service.get(
        test_data['latitude'],
        test_data['longitude'],
        different_query,
        test_data['filters']
    )
    
    if cached_data:
        print("❌ Cache hit inesperado!")
    else:
        print("✅ Cache miss esperado!")
    print()
    
    # Teste 4: Estatísticas após operações
    print("📊 Estatísticas após operações:")
    stats = cache_service.get_stats()
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    print()

def test_cache_performance():
    """
    Testa performance do cache
    """
    print("⚡ TESTE DE PERFORMANCE")
    print("=" * 50)
    
    # Dados de teste
    test_queries = [
        "italiana barata perto de mim",
        "sushi caro com boa avaliação",
        "restaurante brasileiro em conta",
        "comida árabe premium nota 4",
        "pizza italiana aberto agora"
    ]
    
    # Simular múltiplas consultas
    print("🔄 Simulando múltiplas consultas...")
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Consulta: '{query}'")
        
        # Primeira busca (cache miss)
        start_time = time.time()
        cached_data = cache_service.get(-23.5505, -46.6333, query, {})
        first_time = time.time() - start_time
        
        if not cached_data:
            # Armazenar dados de teste
            test_restaurants = [
                {
                    'id': i,
                    'name': f'Restaurante Teste {i}',
                    'rating': 4.0 + (i * 0.1),
                    'cuisine_type': 'teste',
                    'price_range': 'medio',
                    'distance_km': i * 0.5
                }
            ]
            
            cache_service.set(-23.5505, -46.6333, query, {}, test_restaurants, 60)
        
        # Segunda busca (cache hit)
        start_time = time.time()
        cached_data = cache_service.get(-23.5505, -46.6333, query, {})
        second_time = time.time() - start_time
        
        print(f"   Primeira busca: {first_time:.4f}s")
        print(f"   Segunda busca:  {second_time:.4f}s")
        
        if second_time < first_time:
            improvement = ((first_time - second_time) / first_time) * 100
            print(f"   🚀 Melhoria: {improvement:.1f}% mais rápido")
    
    print()

def test_cache_api_endpoints():
    """
    Testa endpoints da API de cache
    """
    print("🌐 TESTANDO ENDPOINTS DA API")
    print("=" * 50)
    
    base_url = "http://127.0.0.1:5000"
    
    # Teste 1: Estatísticas do cache
    print("📊 Teste 1: GET /api/cache/stats")
    try:
        response = requests.get(f"{base_url}/api/cache/stats")
        if response.status_code == 200:
            data = response.json()
            print("✅ Sucesso!")
            print(f"📋 Dados: {json.dumps(data['data'], indent=2, ensure_ascii=False)}")
        else:
            print(f"❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
    print()
    
    # Teste 2: Limpar cache
    print("🧹 Teste 2: POST /api/cache/clear")
    try:
        response = requests.post(f"{base_url}/api/cache/clear")
        if response.status_code == 200:
            data = response.json()
            print("✅ Sucesso!")
            print(f"📋 Mensagem: {data['message']}")
        else:
            print(f"❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
    print()
    
    # Teste 3: Invalidar por localização
    print("🗑️ Teste 3: POST /api/cache/invalidate")
    try:
        payload = {
            'latitude': -23.5505,
            'longitude': -46.6333,
            'radius_km': 5.0
        }
        response = requests.post(f"{base_url}/api/cache/invalidate", json=payload)
        if response.status_code == 200:
            data = response.json()
            print("✅ Sucesso!")
            print(f"📋 Chaves invalidadas: {data['data']['invalidated_keys']}")
        else:
            print(f"❌ Erro: {response.status_code}")
    except Exception as e:
        print(f"❌ Erro de conexão: {e}")
    print()

def main():
    """
    Função principal de teste
    """
    print("🚀 TESTE COMPLETO DO SISTEMA DE CACHE")
    print("=" * 60)
    
    # Teste do serviço de cache
    test_cache_service()
    
    # Teste de performance
    test_cache_performance()
    
    # Teste dos endpoints da API
    test_cache_api_endpoints()
    
    print("=" * 60)
    print("✅ Testes de cache concluídos!")
    print()
    print("💡 DICAS:")
    print("• O cache melhora significativamente a performance")
    print("• TTL padrão é de 1 hora para recomendações")
    print("• Cache funciona mesmo sem Redis (fallback em memória)")
    print("• Use /api/cache/stats para monitorar o cache")
    print("• Use /api/cache/clear para limpar o cache quando necessário")

if __name__ == "__main__":
    main()
