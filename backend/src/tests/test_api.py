#!/usr/bin/env python3
"""
Script de teste para verificar se a API está funcionando
Execute: python test_api.py
"""

import requests
import json
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

def test_health_check():
    """Testa o endpoint de health check"""
    print("Testando health check...")
    try:
        response = requests.get('http://127.0.0.1:5000/api/health')
        if response.status_code == 200:
            print(" Health check funcionando")
            return True
        else:
            print(f"Health check falhou: {response.status_code}")
            return False
    except Exception as e:
        print(f" Erro no health check: {e}")
        return False

def test_recommendations_api():
    """Testa o endpoint de recomendações"""
    print("\nTestando endpoint de recomendações...")
    
    # Dados de teste
    test_data = {
        "text": "restaurantes italianos",
        "latitude": -9.6498,
        "longitude": -35.7089
    }
    
    try:
        response = requests.post(
            'http://127.0.0.1:5000/api/recommendations',
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        if response.status_code == 200:
            data = response.json()
            print("Endpoint de recomendações funcionando")
            print(f"Restaurantes encontrados: {len(data.get('data', {}).get('recommendations', []))}")
            return True
        else:
            print(f" Endpoint falhou: {response.status_code}")
            print(f"Resposta: {response.text}")
            return False
    except Exception as e:
        print(f" Erro no endpoint: {e}")
        return False

def check_environment():
    """Verifica as configurações de ambiente"""
    print("\nVerificando configurações...")
    
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if api_key and api_key != 'sua_chave_aqui':
        print(" Google Maps API Key configurada")
        return True
    else:
        print("Google Maps API Key não configurada - usando dados mockados")
        return False

def main():
    """Função principal"""
    print(" Iniciando testes da API Sabora")
    print("=" * 50)
    
    # Verificar configurações
    has_api_key = check_environment()
    
    # Testar health check
    health_ok = test_health_check()
    
    # Testar endpoint de recomendações
    recommendations_ok = test_recommendations_api()
    
    # Resumo
    print("\n" + "=" * 50)
    print("📋 RESUMO DOS TESTES")
    print("=" * 50)
    
    if health_ok:
        print(" Health check: OK")
    else:
        print(" Health check: FALHOU")
    
    if recommendations_ok:
        print(" Endpoint de recomendações: OK")
    else:
        print(" Endpoint de recomendações: FALHOU")
    
    if has_api_key:
        print(" Google Maps API: Configurada")
    else:
        print(" Google Maps API: Não configurada (usando mockados)")
    
    print("\n PRÓXIMOS PASSOS:")
    if not has_api_key:
        print("1. Configure a GOOGLE_MAPS_API_KEY no arquivo .env")
        print("2. Execute: cp env.example .env")
        print("3. Edite o arquivo .env com sua chave da API")
    else:
        print("1. Tudo configurado! Teste a aplicação no frontend")
    
    print("\n Frontend: http://localhost:5173")
    print("Backend: http://127.0.0.1:5000")

if __name__ == "__main__":
    main()
