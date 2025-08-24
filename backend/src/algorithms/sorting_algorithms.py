def bubble_sort(items_list: list, key: str = None, descending: bool = False):
    n = len(items_list)
    for i in range(n - 1, 0, -1):
        for j in range(i):
            # obter valores baseado no tipo de objeto
            if hasattr(items_list[j], key):
                # objeto com atributos (ex: Restaurant)
                current_value = getattr(items_list[j], key)
                next_value = getattr(items_list[j + 1], key)
            else:
                # dicionario
                current_value = items_list[j].get(key)
                next_value = items_list[j + 1].get(key)

            if current_value is None or next_value is None:
                continue

            swap_needed = False
            if descending:
                if current_value < next_value:
                    swap_needed = True
            else:
                if current_value > next_value:
                    swap_needed = True

            if swap_needed:
                items_list[j], items_list[j + 1] = items_list[j + 1], items_list[j]

            
    return items_list

### Exemplo de Uso:

if __name__ == '__main__':
    # Exemplo com dicionários (compatibilidade com código existente)
    restaurants_dict = [
        {'nome': 'Restaurante A', 'nota': 4.5, 'distancia': 1.2},
        {'nome': 'Restaurante B', 'nota': 4.9, 'distancia': 2.5},
        {'nome': 'Restaurante C', 'nota': 4.4, 'distancia': 0.8},
        {'nome': 'Restaurante D', 'nota': 4.9, 'distancia': 1.9},
        {'nome': 'Restaurante E', 'nota': 3.8, 'distancia': 0.5},
    ]

    print("=== TESTE COM DICIONÁRIOS ===")
    print("Lista Original:")
    print(restaurants_dict)
    print("-" * 30)

    # Teste 1: Ordenar por distância em ordem CRESCENTE
    restaurants_by_distance = bubble_sort(restaurants_dict.copy(), key='distancia')
    print("Ordenado por DISTÂNCIA (crescente):")
    for r in restaurants_by_distance:
        print(f"- {r['nome']}: {r['distancia']} km")
    print("-" * 30)

    # Teste 2: Ordenar por nota em ordem DECRESCENTE
    restaurants_by_rating = bubble_sort(restaurants_dict.copy(), key='nota', descending=True)
    print("Ordenado por NOTA (decrescente):")
    for r in restaurants_by_rating:
        print(f"- {r['nome']}: Nota {r['nota']}")
    print("-" * 30)
    
    print("\n" + "="*50)
    print("=== TESTE COM OBJETOS RESTAURANT ===")
    
    # Exemplo com objetos Restaurant (modelo real do projeto)
    from models.restaurant import Restaurant
    
    restaurants_objects = [
        Restaurant(id=1, name='Restaurante A', latitude=-23.5505, longitude=-46.6333, 
                  rating=4.5, cuisine_type='Brasileira', price_range='medio', address='Rua A, 123',
                  distance=1.2),
        Restaurant(id=2, name='Restaurante B', latitude=-23.5505, longitude=-46.6333,
                  rating=4.9, cuisine_type='Italiana', price_range='alto', address='Rua B, 456',
                  distance=2.5),
        Restaurant(id=3, name='Restaurante C', latitude=-23.5505, longitude=-46.6333,
                  rating=4.4, cuisine_type='Italiana', price_range='baixo', address='Rua C, 789',
                  distance=0.8),
        Restaurant(id=4, name='Restaurante D', latitude=-23.5505, longitude=-46.6333,
                  rating=4.9, cuisine_type='Japonesa', price_range='alto', address='Rua D, 101',
                  distance=1.9),
        Restaurant(id=5, name='Restaurante E', latitude=-23.5505, longitude=-46.6333,
                  rating=3.8, cuisine_type='Fast Food', price_range='baixo', address='Rua E, 202',
                  distance=0.5),
    ]

    print("Lista Original (objetos Restaurant):")
    for r in restaurants_objects:
        print(f"- {r.name}: {r.rating} estrelas, {r.distance} km")
    print("-" * 30)

    # Teste 1: Ordenar por distância em ordem CRESCENTE
    restaurants_by_distance = bubble_sort(restaurants_objects.copy(), key='distance')
    print("Ordenado por DISTÂNCIA (crescente):")
    for r in restaurants_by_distance:
        print(f"- {r.name}: {r.distance} km")
    print("-" * 30)

    # Teste 2: Ordenar por nota em ordem DECRESCENTE
    restaurants_by_rating = bubble_sort(restaurants_objects.copy(), key='rating', descending=True)
    print("Ordenado por RATING (decrescente):")
    for r in restaurants_by_rating:
        print(f"- {r.name}: {r.rating} estrelas")
    print("-" * 30)
    
    # Teste 3: Ordenar por tipo de culinária em ordem alfabética
    restaurants_by_cuisine = bubble_sort(restaurants_objects.copy(), key='cuisine_type')
    print("Ordenado por TIPO DE CULINÁRIA (alfabético):")
    for r in restaurants_by_cuisine:
        print(f"- {r.name}: {r.cuisine_type}")
    print("-" * 30)