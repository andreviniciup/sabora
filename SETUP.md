# 🚀 Guia de Configuração - Sabora

Este guia vai te ajudar a configurar o projeto Sabora para funcionar com dados reais da Google Maps API.

## 📋 Pré-requisitos

- Python 3.8+
- Node.js 16+
- Conta no Google Cloud Platform

## 🔧 Configuração Rápida

### 1. Clone e Instale Dependências

```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

### 1.1 Configurar Redis (Opcional - para Cache)

```bash
# Opção 1: Instalar Redis localmente
sudo apt-get install redis-server  # Ubuntu/Debian
brew install redis                 # macOS

# Opção 2: Usar Docker
docker run -d -p 6379:6379 redis:alpine

# Opção 3: Redis Cloud (gratuito)
# https://redis.com/try-free/
```

### 2. Configure a Google Maps API

#### 2.1 Obter Chave da API

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Ative as seguintes APIs:
   - **Places API**
   - **Geocoding API**
4. Crie credenciais (API Key):
   - Vá em "APIs & Services" > "Credentials"
   - Clique em "Create Credentials" > "API Key"
   - Copie a chave gerada

#### 2.2 Configurar Variáveis de Ambiente

```bash
# No diretório backend
cp env.example .env
```

Edite o arquivo `.env`:
```env
GOOGLE_MAPS_API_KEY=sua_chave_aqui
FLASK_DEBUG=True
PORT=5000
```

### 3. Testar Configuração

```bash
# No diretório backend
python test_api.py
python test_cache.py  # Teste do sistema de cache
```

### 4. Executar Aplicação

```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

## 🧪 Testes

### Teste Automático
```bash
cd backend
python test_api.py
```

### Teste Manual
1. Acesse: http://localhost:5173
2. Digite uma busca como "restaurantes italianos"
3. Verifique se os resultados aparecem

## 🔍 Verificação de Funcionamento

### Com API Key Configurada
- ✅ Dados reais da Google Maps
- ✅ Restaurantes próximos à sua localização
- ✅ Informações atualizadas (avaliações, horários, etc.)

### Sem API Key
- ⚠️ Dados mockados (funciona para desenvolvimento)
- ⚠️ Restaurantes fixos de Maceió-AL
- ⚠️ Informações estáticas

## 🚀 Sistema de Cache

O Sabora inclui um sistema de cache inteligente que melhora significativamente a performance:

### 📊 Benefícios do Cache
- **Performance**: Respostas até 10x mais rápidas
- **Redução de custos**: Menos chamadas para a Google Maps API
- **Experiência do usuário**: Carregamento instantâneo para consultas repetidas
- **Fallback**: Funciona mesmo sem Redis (cache em memória)

### 🔧 Configuração do Cache

#### Com Redis (Recomendado)
```bash
# Configurar URL do Redis no .env
REDIS_URL=redis://localhost:6379/0
CACHE_ENABLED=true
CACHE_TTL_SECONDS=3600
```

#### Sem Redis (Fallback)
O sistema automaticamente usa cache em memória se o Redis não estiver disponível.

### 📈 Monitoramento do Cache

#### Endpoints de Gerenciamento
```bash
# Ver estatísticas do cache
curl http://localhost:5000/api/cache/stats

# Limpar todo o cache
curl -X POST http://localhost:5000/api/cache/clear

# Invalidar cache por localização
curl -X POST http://localhost:5000/api/cache/invalidate \
  -H "Content-Type: application/json" \
  -d '{"latitude": -23.5505, "longitude": -46.6333, "radius_km": 5.0}'
```

#### Teste de Performance
```bash
cd backend
python test_cache.py
```

## 🐛 Solução de Problemas

### Erro: "Google Maps API Key não configurada"
```bash
# Verifique se o arquivo .env existe
ls -la backend/.env

# Verifique se a chave está correta
cat backend/.env
```

### Erro: "API quota exceeded"
- Verifique o uso da API no Google Cloud Console
- Considere aumentar o limite de quota

### Erro: "CORS policy"
- Verifique se o frontend está rodando na porta 5173
- Verifique as configurações de CORS no backend

## 📊 Status dos Componentes

| Componente | Status | Descrição |
|------------|--------|-----------|
| **Backend** | ✅ Pronto | API Flask funcionando |
| **Frontend** | ✅ Pronto | React + Vite funcionando |
| **Google Maps** | ⚠️ Configurar | Precisa de API Key |
| **Algoritmos** | ✅ Pronto | Bubble Sort, Busca Binária |
| **Geolocalização** | ✅ Pronto | Funcionando no navegador |

## 🎯 Próximos Passos

1. **Configure a API Key** seguindo o passo 2
2. **Execute os testes** com `python test_api.py`
3. **Teste a aplicação** no navegador
4. **Personalize** conforme necessário

## 📞 Suporte

Se encontrar problemas:
1. Verifique os logs do console
2. Execute `python test_api.py` para diagnóstico
3. Verifique se todas as dependências estão instaladas

---

**🎉 Pronto! Agora é só inserir a chave da API e testar!**
