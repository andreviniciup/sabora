# arquitetura do sistema sabora

## visão geral

o sistema sabora é uma aplicação web full-stack que utiliza algoritmos fundamentais de computação para fornecer recomendações inteligentes de restaurantes. a arquitetura é baseada em microserviços com separação clara entre frontend e backend.

## arquitetura geral

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   frontend      │    │    backend      │    │   google maps   │
│   (react)       │◄──►│   (flask)       │◄──►│   api           │
│                 │    │                 │    │                 │
│ - interface     │    │ - api rest      │    │ - places api    │
│ - geolocalização│    │ - algoritmos    │    │ - geocoding api │
│ - cache local   │    │ - cache redis   │    │ - distance api  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## componentes principais

### frontend (react)

#### estrutura de componentes
- **app.jsx**: componente raiz da aplicação
- **pages/**: páginas principais (home, searchresults, completelist)
- **components/**: componentes reutilizáveis
- **context/**: gerenciamento de estado global
- **services/**: comunicação com apis
- **hooks/**: hooks customizados

#### tecnologias
- **react 18**: framework principal
- **vite**: bundler e dev server
- **tailwind css**: estilização
- **axios**: cliente http
- **react router**: roteamento

### backend (flask)

#### estrutura de módulos
- **app.py**: aplicação principal flask
- **src/algorithms/**: algoritmos de ordenação e busca
- **src/services/**: integrações com apis externas
- **src/processors/**: processamento de dados
- **src/models/**: modelos de dados
- **src/nlp/**: processamento de linguagem natural
- **src/utils/**: utilitários
- **src/cache/**: sistema de cache

#### tecnologias
- **python 3.11**: linguagem principal
- **flask**: framework web
- **redis**: cache
- **google maps api**: dados de restaurantes

## fluxo de dados

### 1. entrada do usuário
```
usuário → frontend → parser nlp → validação → backend
```

### 2. processamento
```
backend → google maps api → algoritmos → cache → frontend
```

### 3. saída
```
frontend → interface → usuário
```

## algoritmos implementados

### bubble sort
- **localização**: `src/algorithms/sorting_algorithms.py`
- **uso**: ordenação de restaurantes por distância e rating
- **complexidade**: O(n²)
- **aplicação**: preparação de dados para busca eficiente

### busca binária
- **localização**: `src/algorithms/search_algorithms.py`
- **uso**: filtragem por raio de distância
- **complexidade**: O(log n)
- **aplicação**: encontrar restaurantes dentro do raio máximo

### busca linear
- **localização**: `src/algorithms/search_algorithms.py`
- **uso**: busca por nome e critérios específicos
- **complexidade**: O(n)
- **aplicação**: funcionalidades auxiliares de busca

## processamento de linguagem natural

### parser de consultas
- **localização**: `src/nlp/parser.py`
- **funcionalidade**: extrai intenções e parâmetros de consultas em linguagem natural
- **exemplo**: "estou com fome e preciso dos 5 melhores restaurantes perto de mim"

### dicionários de sinônimos
- **localização**: `src/nlp/synonyms.py`
- **categorias**: culinária, preço, distância, avaliação
- **uso**: mapeamento de termos coloquiais para parâmetros técnicos

## sistema de cache

### cache redis
- **propósito**: melhorar performance e reduzir chamadas à api
- **estratégia**: cache por localização e parâmetros de busca
- **ttl**: 1 hora por padrão
- **invalidação**: automática por tempo ou manual por localização

### cache local (frontend)
- **propósito**: armazenar localização do usuário
- **estratégia**: localStorage
- **dados**: coordenadas, timestamp, precisão

## integração com google maps

### apis utilizadas
- **places api**: busca de restaurantes próximos
- **geocoding api**: conversão de endereços em coordenadas
- **distance matrix api**: cálculo de distâncias (futuro)

### parâmetros de busca
- **raio**: 25km por padrão
- **tipo**: restaurant
- **keyword**: opcional, baseado na consulta do usuário

## validação e tratamento de erros

### validação de entrada
- **localização**: `src/utils/validators.py`
- **regras**: coordenadas válidas, texto não vazio, limites de caracteres
- **erros**: retorna lista de erros de validação

### tratamento de erros
- **api**: retorna códigos http apropriados
- **frontend**: exibe mensagens de erro amigáveis
- **fallback**: dados mockados em caso de falha da api

## segurança

### medidas implementadas
- **cors**: configuração específica para domínios permitidos
- **rate limiting**: limite de requisições por ip (futuro)
- **validação**: sanitização de entrada
- **https**: obrigatório em produção

### variáveis de ambiente
- **google_maps_api_key**: chave da api do google
- **secret_key**: chave secreta do flask
- **redis_url**: url do redis (opcional)

## performance

### otimizações implementadas
- **cache**: redis para reduzir chamadas à api
- **algoritmos**: escolha de algoritmos baseada na complexidade
- **lazy loading**: carregamento sob demanda no frontend
- **compressão**: gzip no backend

### métricas
- **tempo de resposta**: < 2s para consultas simples
- **throughput**: 100+ requisições por minuto
- **disponibilidade**: 99.9% (com fallbacks)

## deploy e infraestrutura

### backend (render)
- **plataforma**: render.com
- **runtime**: python 3.11
- **build**: pip install -r requirements.txt
- **start**: python app.py

### frontend (vercel)
- **plataforma**: vercel.com
- **framework**: react
- **build**: npm run build
- **deploy**: automático via github

### variáveis de ambiente
- **desenvolvimento**: arquivo .env local
- **produção**: variáveis de ambiente nas plataformas

## monitoramento e logs

### logs estruturados
- **níveis**: debug, info, warning, error
- **formato**: json estruturado
- **campos**: timestamp, nível, módulo, mensagem, dados

### métricas coletadas
- **requisições**: contagem e tempo de resposta
- **erros**: tipos e frequência
- **cache**: hit rate e miss rate
- **api externa**: chamadas e latência

## testes

### testes unitários
- **backend**: pytest
- **frontend**: jest + react testing library
- **cobertura**: > 80% (meta)

### testes de integração
- **api**: testes de endpoints
- **frontend**: testes de componentes
- **e2e**: testes de fluxo completo (futuro)

## roadmap técnico

### próximas implementações
- **autenticação**: sistema de login/registro
- **favoritos**: restaurantes favoritos do usuário
- **notificações**: push notifications
- **offline**: funcionalidade offline básica

### melhorias planejadas
- **machine learning**: recomendações personalizadas
- **real-time**: websockets para atualizações em tempo real
- **microserviços**: separação em serviços independentes
- **kubernetes**: orquestração de containers
