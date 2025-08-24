from .sorting_algorithms import bubble_sort

def linear_search(items_list: list, key: str, search_value: str):
    for item in items_list:
        # obter valor baseado no tipo de objeto
        if hasattr(item, key):
            # objeto com atributos (ex: Restaurant)
            item_value = getattr(item, key)
        else:
            # dicionario
            item_value = item.get(key)
            
        if item_value and search_value.lower() in str(item_value).lower():
            return item
    return None

def binary_search(sorted_list: list, key: str, limit_value: float):
    start, end = 0, len(sorted_list) - 1
    last_valid_index = -1

    while start <= end:
        middle = (start + end) // 2
        # obter valor baseado no tipo de objeto
        if hasattr(sorted_list[middle], key):
            # objeto com atributos (ex: Restaurant)
            middle_value = getattr(sorted_list[middle], key)
        else:
            # dicionario
            middle_value = sorted_list[middle].get(key)

        if middle_value is None:
            start = middle + 1
            continue

        if middle_value <= limit_value:
            last_valid_index = middle
            start = middle + 1
        else:
            end = middle - 1
    return last_valid_index

### Exemplo de Uso:

if __name__ == '__main__':
    # Exemplo com dicionários (compatibilidade com código existente)
    restaurants_dict = [
        {'nome': 'Restaurante Sabor Divino', 'nota': 4.5, 'distancia': 1.2},
        {'nome': 'Cantina da Praia', 'nota': 4.9, 'distancia': 2.5},
        {'nome': 'Pizzaria do Bairro', 'nota': 4.4, 'distancia': 0.8},
        {'nome': 'Churrascaria Fogo no Chão', 'nota': 4.9, 'distancia': 1.9},
        {'nome': 'O Quintal', 'nota': 3.8, 'distancia': 0.5},
    ]
    
    # Exemplo com objetos Restaurant (modelo real do projeto)
    from models.restaurant import Restaurant
    
    restaurants_objects = [
        Restaurant(id=1, name='Restaurante Sabor Divino', latitude=-23.5505, longitude=-46.6333, 
                  rating=4.5, cuisine_type='Brasileira', price_range='medio', address='Rua A, 123',
                  distance=1.2),
        Restaurant(id=2, name='Cantina da Praia', latitude=-23.5505, longitude=-46.6333,
                  rating=4.9, cuisine_type='Italiana', price_range='alto', address='Rua B, 456',
                  distance=2.5),
        Restaurant(id=3, name='Pizzaria do Bairro', latitude=-23.5505, longitude=-46.6333,
                  rating=4.4, cuisine_type='Italiana', price_range='baixo', address='Rua C, 789',
                  distance=0.8),
    ]
    
    print("=== TESTE COM DICIONÁRIOS ===")
    print("Lista Original para Buscas:")
    print(restaurants_dict)
    print("-" * 30)

    # Teste da Busca Linear com dicionários
    print("Testando Linear Search (dicionários)...")
    search_name = "praia"
    found = linear_search(restaurants_dict, key='nome', search_value=search_name)
    if found:
        print(f"Busca por '{search_name}': Encontrado -> {found['nome']}")
    else:
        print(f"Busca por '{search_name}': Nenhum restaurante encontrado.")
    
    search_name_fail = "Inexistente"
    found_fail = linear_search(restaurants_dict, key='nome', search_value=search_name_fail)
    print(f"Busca por '{search_name_fail}': {'Encontrado' if found_fail else 'Não encontrado'}")
    print("-" * 30)

    # Teste da Busca Binária com dicionários
    print("Testando Binary Search (dicionários)...")
    restaurants_sorted_dist = bubble_sort(restaurants_dict.copy(), chave='distancia')
    print("Lista ordenada por distância para a busca binária:")
    for r in restaurants_sorted_dist:
        print(f"- {r['nome']}: {r['distancia']} km")
    
    max_radius_km = 2.0
    limit_index = binary_search(
        restaurants_sorted_dist, 
        key='distancia', 
        limit_value=max_radius_km
    )

    if limit_index != -1:
        results_within_radius = restaurants_sorted_dist[:limit_index + 1]
        print(f"\nRestaurantes encontrados dentro de {max_radius_km} km:")
        for r in results_within_radius:
            print(f"- {r['nome']} (Distância: {r['distancia']} km)")
    else:
        print(f"\nNenhum restaurante encontrado dentro de {max_radius_km} km.")
    
    print("\n" + "="*50)
    print("=== TESTE COM OBJETOS RESTAURANT ===")
    
    # Teste da Busca Linear com objetos Restaurant
    print("Testando Linear Search (objetos Restaurant)...")
    search_name = "praia"
    found = linear_search(restaurants_objects, key='name', search_value=search_name)
    if found:
        print(f"Busca por '{search_name}': Encontrado -> {found.name}")
    else:
        print(f"Busca por '{search_name}': Nenhum restaurante encontrado.")
    
    # Teste da Busca Binária com objetos Restaurant
    print("\nTestando Binary Search (objetos Restaurant)...")
    restaurants_sorted_dist = bubble_sort(restaurants_objects.copy(), chave='distance')
    print("Lista ordenada por distância para a busca binária:")
    for r in restaurants_sorted_dist:
        print(f"- {r.name}: {r.distance} km")
    
    max_radius_km = 2.0
    limit_index = binary_search(
        restaurants_sorted_dist, 
        key='distance', 
        limit_value=max_radius_km
    )

    if limit_index != -1:
        results_within_radius = restaurants_sorted_dist[:limit_index + 1]
        print(f"\nRestaurantes encontrados dentro de {max_radius_km} km:")
        for r in results_within_radius:
            print(f"- {r.name} (Distância: {r.distance} km)")
    else:
        print(f"\nNenhum restaurante encontrado dentro de {max_radius_km} km.")