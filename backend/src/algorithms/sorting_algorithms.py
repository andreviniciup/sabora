def bubble_sort(lista_de_itens: list, chave: str, decrescente: bool = False):
    n = len(lista_de_itens)
    for i in range(n - 1, 0, -1):
        for j in range(i):
            valor_atual = lista_de_itens[j].get(chave)
            valor_proximo = lista_de_itens[j + 1].get(chave)

            if valor_atual is None or valor_proximo is None:
                continue

            troca_necessaria = False
            if decrescente:
                if valor_atual < valor_proximo:
                    troca_necessaria = True
            else:
                if valor_atual > valor_proximo:
                    troca_necessaria = True

            if troca_necessaria:
                lista_de_itens[j], lista_de_itens[j + 1] = lista_de_itens[j + 1], lista_de_itens[j]

            
    return lista_de_itens

### Exemplo de Uso:

if __name__ == '__main__':
    restaurantes = [
        {'nome': 'Restaurante A', 'nota': 4.5, 'distancia': 1.2},
        {'nome': 'Restaurante B', 'nota': 4.9, 'distancia': 2.5},
        {'nome': 'Restaurante C', 'nota': 4.4, 'distancia': 0.8},
        {'nome': 'Restaurante D', 'nota': 4.9, 'distancia': 1.9},
        {'nome': 'Restaurante E', 'nota': 3.8, 'distancia': 0.5},
    ]

    print("Lista Original:")
    print(restaurantes)
    print("-" * 30)

    # Teste 1: Ordenar por distância em ordem CRESCENTE
    restaurantes_por_distancia = bubble_sort(restaurantes.copy(), chave='distancia')
    print("Ordenado por DISTÂNCIA (crescente):")
    for r in restaurantes_por_distancia:
        print(f"- {r['nome']}: {r['distancia']} km")
    print("-" * 30)

    # Teste 2: Ordenar por nota em ordem DECRESCENTE
    restaurantes_por_nota = bubble_sort(restaurantes.copy(), chave='nota', decrescente=True)
    print("Ordenado por NOTA (decrescente):")
    for r in restaurantes_por_nota:
        print(f"- {r['nome']}: Nota {r['nota']}")
    print("-" * 30)