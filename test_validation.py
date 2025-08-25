#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from utils.search_validator import search_validator

def test_validation():
    test_cases = [
        ("oi", False, "Deve ser inválido"),
        ("teste", False, "Deve ser inválido"),
        ("hello", False, "Deve ser inválido"),
        ("pizza", True, "Deve ser válido"),
        ("restaurante japonês", True, "Deve ser válido"),
        ("comida italiana", True, "Deve ser válido"),
    ]
    
    print("🧪 Testando validação de busca...")
    print("=" * 50)
    
    for query, expected_valid, description in test_cases:
        result = search_validator.validate_search_query(query)
        status = "✅ PASSOU" if result.is_valid == expected_valid else "❌ FALHOU"
        
        print(f"Query: '{query}'")
        print(f"Esperado: {'Válido' if expected_valid else 'Inválido'}")
        print(f"Resultado: {'Válido' if result.is_valid else 'Inválido'}")
        print(f"Status: {status}")
        if not result.is_valid:
            print(f"Erros: {result.errors}")
        print("-" * 30)

if __name__ == "__main__":
    test_validation()
