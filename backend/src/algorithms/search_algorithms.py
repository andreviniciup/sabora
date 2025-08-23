from .sorting_algorithms import bubble_sort

def busca_linear(lista_de_itens: list, chave: str, valor_procurado: str):
    for item in lista_de_itens:
        valor_no_item = item.get(chave)
        if valor_no_item and valor_procurado.lower() in valor_no_item.lower():
            return item
    return None

def busca_binaria(lista_ordenada: list, chave: str, valor_limite: float):
    inicio, fim = 0, len(lista_ordenada) - 1
    ultimo_indice_valido = -1

    while inicio <= fim:
        meio = (inicio + fim) // 2
        # obter valor baseado no tipo de objeto
        if hasattr(lista_ordenada[meio], chave):
            # objeto com atributos (ex: Restaurant)
            valor_meio = getattr(lista_ordenada[meio], chave)
        else:
            # dicionario
            valor_meio = lista_ordenada[meio].get(chave)

        if valor_meio is None:
            inicio = meio + 1
            continue

        if valor_meio <= valor_limite:
            ultimo_indice_valido = meio
            inicio = meio + 1
        else:
            fim = meio - 1
    return ultimo_indice_valido

### Exemplo de Uso:

if __name__ == '__main__':
    restaurantes = [
        {'nome': 'Restaurante Sabor Divino', 'nota': 4.5, 'distancia': 1.2},
        {'nome': 'Cantina da Praia', 'nota': 4.9, 'distancia': 2.5},
        {'nome': 'Pizzaria do Bairro', 'nota': 4.4, 'distancia': 0.8},
        {'nome': 'Churrascaria Fogo no Chão', 'nota': 4.9, 'distancia': 1.9},
        {'nome': 'O Quintal', 'nota': 3.8, 'distancia': 0.5},
    ]
    print("Lista Original para Buscas:")
    print(restaurantes)
    print("-" * 30)

    # Teste da Busca Linear
    print("Testando Busca Linear...")
    nome_busca = "praia"
    encontrado = busca_linear(restaurantes, chave='nome', valor_procurado=nome_busca)
    if encontrado:
        print(f"Busca por '{nome_busca}': Encontrado -> {encontrado['nome']}")
    else:
        print(f"Busca por '{nome_busca}': Nenhum restaurante encontrado.")
    
    nome_busca_falha = "Inexistente"
    encontrado_falha = busca_linear(restaurantes, chave='nome', valor_procurado=nome_busca_falha)
    print(f"Busca por '{nome_busca_falha}': {'Encontrado' if encontrado_falha else 'Não encontrado'}")
    print("-" * 30)

    # Teste da Busca Binária
    print("Testando Busca Binária...")
    restaurantes_ordenados_dist = bubble_sort(restaurantes.copy(), chave='distancia')
    print("Lista ordenada por distância para a busca binária:")
    for r in restaurantes_ordenados_dist:
        print(f"- {r['nome']}: {r['distancia']} km")
    
    raio_maximo_km = 2.0
    indice_limite = busca_binaria(
        restaurantes_ordenados_dist, 
        chave='distancia', 
        valor_limite=raio_maximo_km
    )

    if indice_limite != -1:
        resultados_dentro_do_raio = restaurantes_ordenados_dist[:indice_limite + 1]
        print(f"\nRestaurantes encontrados dentro de {raio_maximo_km} km:")
        for r in resultados_dentro_do_raio:
            print(f"- {r['nome']} (Distância: {r['distancia']} km)")
    else:
        print(f"\nNenhum restaurante encontrado dentro de {raio_maximo_km} km.")