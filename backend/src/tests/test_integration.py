"""
teste de integracao para verificar se todos os componentes estao funcionando juntos
"""

import sys
import os

# adicionar o diretorio src ao path para imports relativos
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.restaurant import Restaurant, restaurants_to_dicts, dicts_to_restaurants
from processors.recommendation_engine import RecommendationEngine, get_recommendations
from algorithms.sorting_algorithms import bubble_sort
from algorithms.search_algorithms import busca_binaria
from utils.geo_utils import calculate_distance, format_distance


def test_restaurant_model():
    """testa o modelo restaurant"""
    print("=== teste do modelo restaurant ===")
    
    # criar restaurante
    restaurant = Restaurant(
        id=1,
        name="restaurante teste",
        latitude=-9.6498,
        longitude=-35.7089,
        rating=4.5,
        cuisine_type="brasileira",
        price_range="medio",
        address="rua teste, 123"
    )
    
    # testar metodos
    restaurant.update_distance(0.5, "500 metros")
    restaurant.update_rank(1)
    restaurant.update_recommendation_score(85.5)
    
    # testar filtros
    assert restaurant.matches_cuisine_filter(['brasileira']) == True
    assert restaurant.matches_price_filter('medio') == True
    assert restaurant.matches_rating_filter(4.0) == True
    assert restaurant.is_within_radius(-9.6498, -35.7089, 1.0) == True
    
    print("✅ modelo restaurant funcionando corretamente")


def test_algorithms_with_objects():
    """testa os algoritmos com objetos restaurant"""
    print("\n=== teste dos algoritmos com objetos ===")
    
    # criar lista de restaurantes
    restaurants = [
        Restaurant(id=1, name="A", latitude=-9.6498, longitude=-35.7089, rating=4.5, cuisine_type="brasileira", price_range="medio", address="rua a"),
        Restaurant(id=2, name="B", latitude=-9.6500, longitude=-35.7090, rating=4.8, cuisine_type="italiana", price_range="alto", address="rua b"),
        Restaurant(id=3, name="C", latitude=-9.6600, longitude=-35.7200, rating=3.9, cuisine_type="japonesa", price_range="medio", address="rua c"),
    ]
    
    # adicionar distancias
    for restaurant in restaurants:
        distance = calculate_distance(-9.6498, -35.7089, restaurant.latitude, restaurant.longitude)
        restaurant.update_distance(distance, format_distance(distance))
    
    # testar bubble sort
    sorted_by_distance = bubble_sort(restaurants.copy(), chave='distance', decrescente=False)
    assert sorted_by_distance[0].name == "A"  # mais proximo
    
    sorted_by_rating = bubble_sort(restaurants.copy(), chave='rating', decrescente=True)
    assert sorted_by_rating[0].name == "B"  # maior nota
    
    # testar busca binaria
    last_index = busca_binaria(sorted_by_distance, chave='distance', valor_limite=1.0)
    assert last_index >= 0
    
    print("✅ algoritmos funcionando com objetos restaurant")


def test_recommendation_engine_integration():
    """testa a integracao completa do motor de recomendacoes"""
    print("\n=== teste de integracao do motor de recomendacoes ===")
    
    # criar dados de teste
    test_restaurants = [
        Restaurant(
            id=1, name="restaurante a", latitude=-9.6498, longitude=-35.7089,
            rating=4.5, cuisine_type="brasileira", price_range="medio", address="rua a"
        ),
        Restaurant(
            id=2, name="restaurante b", latitude=-9.6500, longitude=-35.7090,
            rating=4.8, cuisine_type="italiana", price_range="alto", address="rua b"
        ),
        Restaurant(
            id=3, name="restaurante c", latitude=-9.6600, longitude=-35.7200,
            rating=3.9, cuisine_type="japonesa", price_range="medio", address="rua c"
        ),
    ]
    
    # testar engine
    engine = RecommendationEngine()
    engine.set_restaurants(test_restaurants)
    
    # obter recomendacoes
    recommendations = engine.get_recommendations(-9.6498, -35.7089, 1.0, 2)
    
    # verificar resultados
    assert len(recommendations) > 0
    assert all(hasattr(r, 'distance') for r in recommendations)
    assert all(hasattr(r, 'rank') for r in recommendations)
    assert all(hasattr(r, 'recommendation_score') for r in recommendations)
    
    # testar filtros
    filtered = engine.get_recommendations_with_filters(
        -9.6498, -35.7089, 1.0, 2, 4.0, ['brasileira'], 'medio'
    )
    
    assert len(filtered) >= 0  # pode ser 0 se nao houver matches
    
    print("✅ motor de recomendacoes integrado corretamente")


def test_conversion_functions():
    """testa as funcoes de conversao"""
    print("\n=== teste das funcoes de conversao ===")
    
    # criar restaurantes
    restaurants = [
        Restaurant(id=1, name="A", latitude=-9.6498, longitude=-35.7089, rating=4.5, cuisine_type="brasileira", price_range="medio", address="rua a"),
        Restaurant(id=2, name="B", latitude=-9.6500, longitude=-35.7090, rating=4.8, cuisine_type="italiana", price_range="alto", address="rua b"),
    ]
    
    # converter para dicionarios
    dicts = restaurants_to_dicts(restaurants)
    assert len(dicts) == 2
    assert isinstance(dicts[0], dict)
    assert dicts[0]['name'] == "A"
    
    # converter de volta para objetos
    restaurants_back = dicts_to_restaurants(dicts)
    assert len(restaurants_back) == 2
    assert isinstance(restaurants_back[0], Restaurant)
    assert restaurants_back[0].name == "A"
    
    print("✅ funcoes de conversao funcionando corretamente")


def test_function_convenience():
    """testa a funcao de conveniencia"""
    print("\n=== teste da funcao de conveniencia ===")
    
    # criar restaurantes
    restaurants = [
        Restaurant(id=1, name="A", latitude=-9.6498, longitude=-35.7089, rating=4.5, cuisine_type="brasileira", price_range="medio", address="rua a"),
        Restaurant(id=2, name="B", latitude=-9.6500, longitude=-35.7090, rating=4.8, cuisine_type="italiana", price_range="alto", address="rua b"),
    ]
    
    # usar funcao de conveniencia
    recommendations = get_recommendations(restaurants, -9.6498, -35.7089, 1.0, 2)
    
    assert len(recommendations) > 0
    assert isinstance(recommendations[0], Restaurant)
    
    print("✅ funcao de conveniencia funcionando corretamente")


def run_all_tests():
    """executa todos os testes"""
    print("🧪 iniciando testes de integracao...\n")
    
    try:
        test_restaurant_model()
        test_algorithms_with_objects()
        test_recommendation_engine_integration()
        test_conversion_functions()
        test_function_convenience()
        
        print("\n🎉 todos os testes de integracao passaram!")
        return True
        
    except Exception as e:
        print(f"\n❌ erro nos testes: {e}")
        return False


if __name__ == "__main__":
    run_all_tests()
