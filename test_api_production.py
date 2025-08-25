#!/usr/bin/env python3

import requests
import json

def test_api_production():
    url = "https://sabora-backend.onrender.com/api/recommendations"
    
    # Teste com "oi" - deve retornar erro 400
    print("🧪 Testando 'oi' na produção (deve ser inválido)...")
    data_oi = {
        "text": "oi",
        "latitude": -9.5882089,
        "longitude": -35.7741114
    }
    
    try:
        response = requests.post(url, json=data_oi)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print("-" * 50)
    except Exception as e:
        print(f"Erro: {e}")
    
    # Teste com "pizza" - deve retornar sucesso
    print("🧪 Testando 'pizza' na produção (deve ser válido)...")
    data_pizza = {
        "text": "pizza",
        "latitude": -9.5882089,
        "longitude": -35.7741114
    }
    
    try:
        response = requests.post(url, json=data_pizza)
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        print("-" * 50)
    except Exception as e:
        print(f"Erro: {e}")

if __name__ == "__main__":
    test_api_production()
