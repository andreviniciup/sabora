# guia de desenvolvimento - sabora

## configuração do ambiente

### pré-requisitos
- python 3.11+
- node.js 16+
- git
- editor de código (vscode recomendado)

### extensões recomendadas (vscode)
- python
- react snippets
- tailwind css intellisense
- gitlens
- auto rename tag

## estrutura de desenvolvimento

### convenções de código

#### python (backend)
- **indentação**: 4 espaços
- **naming**: snake_case para variáveis e funções
- **classes**: PascalCase
- **constantes**: UPPER_CASE
- **docstrings**: formato google style

```python
def calcular_distancia(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    calcula a distância entre dois pontos geográficos.
    
    Args:
        lat1: latitude do primeiro ponto
        lon1: longitude do primeiro ponto
        lat2: latitude do segundo ponto
        lon2: longitude do segundo ponto
        
    Returns:
        float: distância em quilômetros
    """
    pass
```

#### javascript/react (frontend)
- **indentação**: 2 espaços
- **naming**: camelCase para variáveis e funções
- **componentes**: PascalCase
- **constantes**: UPPER_CASE
- **jsdoc**: para documentação de funções

```javascript
/**
 * calcula a distância entre dois pontos
 * @param {number} lat1 - latitude do primeiro ponto
 * @param {number} lon1 - longitude do primeiro ponto
 * @param {number} lat2 - latitude do segundo ponto
 * @param {number} lon2 - longitude do segundo ponto
 * @returns {number} distância em quilômetros
 */
const calcularDistancia = (lat1, lon1, lat2, lon2) => {
  // implementação
}
```

### estrutura de commits

usando conventional commits:

```
tipo(escopo): descrição

feat: nova funcionalidade
fix: correção de bug
docs: documentação
style: formatação
refactor: refatoração
test: testes
chore: tarefas de manutenção
```

exemplos:
- `feat: adicionar sistema de cache redis`
- `fix: corrigir erro de cors no frontend`
- `docs: atualizar readme com instruções de deploy`
- `refactor: otimizar algoritmo de busca binária`

## fluxo de desenvolvimento

### 1. setup inicial

```bash
# clone o repositório
git clone https://github.com/andreviniciup/sabora.git
cd sabora

# setup backend
cd backend
python -m venv venv
source venv/bin/activate  # linux/mac
# ou venv\Scripts\activate  # windows
pip install -r requirements.txt

# setup frontend
cd ../frontend
npm install
```

### 2. desenvolvimento local

```bash
# terminal 1 - backend
cd backend
source venv/bin/activate
python app.py

# terminal 2 - frontend
cd frontend
npm run dev
```

### 3. testes

```bash
# backend
cd backend
python -m pytest tests/

# frontend
cd frontend
npm test
```

### 4. linting e formatação

```bash
# backend (usando black)
cd backend
black src/
flake8 src/

# frontend (usando eslint)
cd frontend
npm run lint
npm run format
```

## debugging

### backend

#### logs estruturados
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("dados de debug")
logger.info("informação geral")
logger.warning("aviso")
logger.error("erro")
```

#### debugger
```python
import pdb; pdb.set_trace()  # breakpoint
```

### frontend

#### console logs
```javascript
console.log("dados:", data);
console.error("erro:", error);
console.warn("aviso:", warning);
```

#### react devtools
- instalar extensão do navegador
- inspecionar componentes e estado

## testes

### backend

#### estrutura de testes
```
backend/
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_algorithms.py
│   ├── test_services.py
│   └── test_utils.py
```

#### exemplo de teste
```python
import pytest
from src.algorithms.sorting_algorithms import bubble_sort

def test_bubble_sort():
    """testa o algoritmo bubble sort"""
    data = [3, 1, 4, 1, 5, 9, 2, 6]
    expected = [1, 1, 2, 3, 4, 5, 6, 9]
    
    result = bubble_sort(data)
    assert result == expected
```

### frontend

#### estrutura de testes
```
frontend/
├── src/
│   ├── __components__/
│   │   └── __tests__/
│   └── __services__/
│       └── __tests__/
```

#### exemplo de teste
```javascript
import { render, screen } from '@testing-library/react';
import SearchBar from '../SearchBar';

test('renderiza barra de busca', () => {
  render(<SearchBar />);
  const searchInput = screen.getByPlaceholderText(/pesquisar/i);
  expect(searchInput).toBeInTheDocument();
});
```

## performance

### backend

#### profiling
```python
import cProfile
import pstats

def profile_function():
    profiler = cProfile.Profile()
    profiler.enable()
    
    # código a ser analisado
    result = some_function()
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumulative')
    stats.print_stats()
```

#### otimizações
- usar cache redis
- limitar chamadas à api externa
- otimizar algoritmos
- usar índices no banco de dados

### frontend

#### profiling
- react devtools profiler
- chrome devtools performance tab
- lighthouse para métricas

#### otimizações
- lazy loading de componentes
- memoização com useMemo/useCallback
- code splitting
- otimização de imagens

## deploy

### ambiente de desenvolvimento

```bash
# backend
cd backend
python app.py

# frontend
cd frontend
npm run dev
```

### ambiente de produção

#### backend (render)
1. push para branch main
2. render faz deploy automático
3. verificar logs no dashboard

#### frontend (vercel)
1. push para branch main
2. vercel faz deploy automático
3. verificar preview no dashboard

## monitoramento

### logs
- backend: logs estruturados em json
- frontend: console logs e error tracking
- produção: centralização de logs

### métricas
- tempo de resposta
- taxa de erro
- uso de recursos
- cache hit rate

## troubleshooting

### problemas comuns

#### cors errors
- verificar configuração de cors no backend
- adicionar domínio à lista de origins permitidos

#### api key errors
- verificar se a chave está configurada
- verificar restrições da chave no google cloud

#### cache issues
- verificar conexão com redis
- limpar cache se necessário

#### build errors
- verificar dependências
- verificar versões de node/python
- limpar cache de build

### comandos úteis

```bash
# limpar cache
npm cache clean --force
pip cache purge

# reinstalar dependências
rm -rf node_modules package-lock.json
npm install

# resetar banco de dados
rm -rf *.db
python init_db.py

# verificar logs
docker logs container_name
```

## recursos úteis

### documentação
- [flask documentation](https://flask.palletsprojects.com/)
- [react documentation](https://react.dev/)
- [tailwind css](https://tailwindcss.com/docs)
- [google maps api](https://developers.google.com/maps)

### ferramentas
- [postman](https://www.postman.com/) - teste de apis
- [insomnia](https://insomnia.rest/) - alternativa ao postman
- [redis cli](https://redis.io/topics/rediscli) - cliente redis
- [chrome devtools](https://developers.google.com/web/tools/chrome-devtools)

### comunidades
- stack overflow
- github discussions
- discord/slack de tecnologias
