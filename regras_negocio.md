# regras de negócio - sistema sabora

## 1. entidades principais

### 1.1 restaurante
- **id**: identificador único (obrigatório)
- **name**: nome do restaurante (obrigatório, 3-100 caracteres)
- **latitude/longitude**: coordenadas geográficas (obrigatório, -90 a 90, -180 a 180)
- **rating**: nota média (0.0 a 5.0, obrigatório)
- **cuisine_type**: tipo de culinária (obrigatório, lista predefinida)
- **price_range**: faixa de preço (baixo, medio, alto, obrigatório)
- **address**: endereço completo (obrigatório)
- **phone**: telefone (opcional, formato brasileiro)
- **website**: site (opcional, url válida)
- **opening_hours**: horários (opcional, formato legível)
- **features**: características especiais (lista, opcional)
- **distance**: distância calculada do usuário (km, calculado)
- **distance_formatted**: distância formatada (calculado)
- **rank**: posição na lista de recomendações (calculado)
- **recommendation_score**: score de recomendação 0-100 (calculado)

### 1.2 usuário
- **location**: localização atual (latitude/longitude, obrigatório para busca)
- **preferences**: preferências salvas (opcional)
- **search_history**: histórico de buscas (opcional)

### 1.3 consulta de busca
- **text**: texto da consulta (obrigatório, 1-500 caracteres)
- **latitude/longitude**: localização do usuário (obrigatório)
- **filters**: filtros aplicados (opcional)
- **timestamp**: momento da busca (automático)

## 2. tipos de culinária (cuisine_type)

### 2.1 lista oficial
- nordestina
- italiana
- japonesa
- brasileira
- chinesa
- árabe
- portuguesa
- peruana
- mediterrânea
- mexicana
- indiana
- francesa
- frutos do mar
- vegana
- saudável
- fast food
- padaria

### 2.2 regras de mapeamento
- sinônimos são mapeados para tipos oficiais
- múltiplos tipos podem ser combinados
- "pizza" mapeia para "italiana" e "fast food"
- "sushi" mapeia para "japonesa"
- "feijoada" mapeia para "brasileira"

## 3. faixas de preço (price_range)

### 3.1 categorias
- **baixo**: até r$ 30 por pessoa
- **medio**: r$ 30 a r$ 80 por pessoa
- **alto**: acima de r$ 80 por pessoa

### 3.2 sinônimos
- baixo: barato, econômico, acessível, em conta, popular
- alto: caro, luxo, premium, sofisticado, exclusivo

## 4. algoritmo de recomendação

### 4.1 fluxo principal
1. **entrada**: consulta + localização + filtros
2. **busca**: restaurantes próximos (raio configurável)
3. **cálculo**: distância do usuário para cada restaurante
4. **filtros**: aplicar filtros de culinária, preço, nota
5. **ordenação**: por distância (menor primeiro)
6. **filtro raio**: manter apenas dentro do raio especificado
7. **reordenação**: por nota (maior primeiro)
8. **limite**: retornar top n resultados
9. **score**: calcular score de recomendação

### 4.2 cálculo de distância
- fórmula de haversine para coordenadas geográficas
- resultado em quilômetros
- arredondamento para 2 casas decimais

### 4.3 score de recomendação
- **fórmula**: (distância_score * 0.6) + (rating_score * 0.4)
- **distância_score**: max(0, 100 - (distância * 20))
- **rating_score**: rating * 20
- **resultado**: 0 a 100

### 4.4 filtros aplicados
- **nota mínima**: rating >= min_rating
- **culinária**: cuisine_type contém tipo desejado
- **preço**: price_range igual ao desejado
- **raio**: distance <= radius_km

## 5. processamento de linguagem natural (nlp)

### 5.1 extração de filtros
- **culinária**: reconhece tipos e sinônimos
- **preço**: reconhece faixas e sinônimos
- **distância**: reconhece "perto", "longe", valores numéricos
- **avaliação**: reconhece "bom", "excelente", notas numéricas
- **abertura**: reconhece "aberto agora", "funcionando"

### 5.2 sinônimos suportados
- **perto**: próximo, perto de mim, nas redondezas, ao lado
- **longe**: distante, afastado, mais afastado
- **bom**: ótimo, excelente, top, maravilhoso, incrível
- **aberto**: funcionando, aberto agora

### 5.3 valores padrão
- **perto**: 2.0 km
- **medio**: 5.0 km
- **longe**: 10.0 km
- **bom**: 4.0 estrelas
- **ótimo**: 4.5 estrelas
- **excelente**: 5.0 estrelas

## 6. sistema de cache

### 6.1 estratégia de cache
- **chave**: hash md5 dos parâmetros da busca
- **ttl**: 1 hora (3600 segundos)
- **fallback**: cache em memória se redis indisponível
- **invalidação**: por localização ou manual

### 6.2 parâmetros da chave
- latitude (arredondada para 6 casas)
- longitude (arredondada para 6 casas)
- texto da consulta (lowercase, trim)
- filtros aplicados (json ordenado)

### 6.3 invalidação
- **manual**: endpoint /api/cache/clear
- **por localização**: endpoint /api/cache/invalidate
- **automática**: ttl expira

## 7. integração com google maps

### 7.1 apis utilizadas
- **places api**: busca de restaurantes próximos
- **geocoding api**: conversão de endereços

### 7.2 parâmetros de busca
- **raio**: 5000 metros (5 km)
- **tipo**: restaurant
- **keyword**: palavra-chave da consulta (opcional)

### 7.3 fallback
- se api key não configurada: dados mockados
- se erro na api: dados mockados
- dados mockados baseados em maceió-al

## 8. validações

### 8.1 entrada de dados
- **texto**: não vazio, máximo 500 caracteres
- **latitude**: -90 a 90 graus
- **longitude**: -180 a 180 graus
- **raio**: 0.1 a 50 km
- **nota mínima**: 0.0 a 5.0

### 8.2 restaurantes
- **nome**: 3 a 100 caracteres
- **nota**: 0.0 a 5.0
- **coordenadas**: válidas
- **endereço**: não vazio

### 8.3 cache
- **ttl**: 60 a 86400 segundos (1 min a 24h)
- **chave**: máximo 255 caracteres

## 9. tratamento de erros

### 9.1 erros de validação
- **400 bad request**: dados inválidos
- **422 unprocessable entity**: dados malformados

### 9.2 erros de sistema
- **500 internal server error**: erro interno
- **503 service unavailable**: serviço indisponível

### 9.3 erros de localização
- **403 forbidden**: localização não permitida
- **404 not found**: localização não encontrada

### 9.4 mensagens de erro
- sempre em português
- descritivas e úteis
- sem informações sensíveis

## 10. performance e limites

### 10.1 limites de resposta
- **máximo de resultados**: 20 restaurantes
- **raio máximo**: 50 km
- **timeout**: 30 segundos

### 10.2 cache
- **hit rate esperado**: > 80%
- **tempo de resposta cache**: < 10ms
- **tempo de resposta sem cache**: < 2s

### 10.3 rate limiting
- **requisições por minuto**: 100 por ip
- **requisições por hora**: 1000 por ip

## 11. segurança

### 11.1 validação de entrada
- sanitização de strings
- validação de tipos
- escape de caracteres especiais

### 11.2 cors
- origens permitidas configuráveis
- métodos: get, post
- headers: content-type, authorization

### 11.3 api keys
- google maps api key em variável de ambiente
- não exposta em logs ou respostas
- validação de domínio (se configurada)

## 12. monitoramento

### 12.1 métricas
- tempo de resposta médio
- taxa de cache hit
- número de requisições por minuto
- erros por tipo

### 12.2 logs
- nível info para operações normais
- nível warning para situações não críticas
- nível error para erros
- sem dados sensíveis

### 12.3 alertas
- tempo de resposta > 5s
- taxa de erro > 5%
- cache hit rate < 50%

## 13. configuração

### 13.1 variáveis de ambiente obrigatórias
- google_maps_api_key (para dados reais)
- flask_debug (true/false)
- port (número da porta)

### 13.2 variáveis opcionais
- redis_url (para cache)
- cache_enabled (true/false)
- cache_ttl_seconds (tempo de vida)
- secret_key (para sessões)
- allowed_origins (para cors)

### 13.3 valores padrão
- port: 5000
- cache_ttl: 3600
- max_results: 5
- default_radius: 2.0 km
