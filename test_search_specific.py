#!/usr/bin/env python3

import requests
import json

def test_specific_searches():
    url = "https://sabora-backend.onrender.com/api/recommendations"
    
    test_cases = [
        {
            "name": "pizza simples",
            "text": "pizza",
            "expected_count": "> 0"
        },
        {
            "name": "restaurante japonês",
            "text": "restaurante japonês",
            "expected_count": "> 0"
        },
        {
            "name": "comida italiana",
            "text": "comida italiana",
            "expected_count": "> 0"
        },
        {
            "name": "melhores pizzas perto de mim",
            "text": "melhores pizzas perto de mim",
            "expected_count": "> 0"
        }
    ]
    
    for test in test_cases:
        print(f"\n🧪 Testando: {test['name']}")
        print(f"📝 Query: '{test['text']}'")
        
        data = {
            "text": test['text'],
            "latitude": -9.5882089,
            "longitude": -35.7741114
        }
        
        try:
            response = requests.post(url, json=data)
            print(f"📊 Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                recommendations = result.get('data', {}).get('recommendations', [])
                count = len(recommendations)
                
                print(f"🍽️  Restaurantes encontrados: {count}")
                print(f"📋 Título: {result.get('data', {}).get('dynamic_title', 'N/A')}")
                
                if count > 0:
                    print("✅ SUCESSO - Encontrou restaurantes")
                    # Mostrar primeiro restaurante
                    first = recommendations[0]
                    print(f"   🏪 Primeiro: {first.get('name', 'N/A')}")
                    print(f"   📍 Distância: {first.get('distance_formatted', 'N/A')}")
                else:
                    print("❌ FALHOU - Nenhum restaurante encontrado")
                    
            else:
                print(f"❌ Erro HTTP: {response.status_code}")
                print(f"📄 Resposta: {response.text}")
                
        except Exception as e:
            print(f"❌ Erro: {e}")
        
        print("-" * 50)

if __name__ == "__main__":
    test_specific_searches()
