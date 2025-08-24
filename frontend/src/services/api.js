import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Interceptor para request
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to: ${config.url}`)
    return config
  },
  (error) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// Interceptor para response
api.interceptors.response.use(
  (response) => {
    console.log(`Response from ${response.config.url}:`, response.status)
    return response
  },
  (error) => {
    console.error('Response error:', error.response?.status, error.message)
    return Promise.reject(error)
  }
)

// Serviços da API
export const restaurantAPI = {
  // Verificar saúde da API
  healthCheck: async () => {
    try {
      const response = await api.get('/api/health')
      return response.data
    } catch (error) {
      throw new Error(`Health check failed: ${error.message}`)
    }
  },

  // Buscar restaurantes com recomendação baseada em texto e localização
  getRecommendations: async (text, latitude, longitude) => {
    try {
      console.log("🌐 API: Fazendo requisição para /api/recommendations")
      console.log(`   📝 Texto: '${text}'`)
      console.log(`   📍 Latitude: ${latitude}`)
      console.log(`   📍 Longitude: ${longitude}`)
      
      const requestData = {
        text,
        latitude,
        longitude
      }
      
      console.log("📤 Dados enviados:", requestData)
      
      const response = await api.post('/api/recommendations', requestData)
      
      console.log("📥 Resposta recebida:", response.data)
      return response.data
    } catch (error) {
      console.error("❌ API: Erro na requisição:", error)
      if (error.response?.status === 400) {
        console.error("   📄 Detalhes do erro:", error.response.data)
        throw new Error(error.response.data.message || 'Parâmetros de busca inválidos')
      }
      throw new Error(`Falha na busca: ${error.message}`)
    }
  },

  // Buscar restaurantes simples (mantido para compatibilidade)
  getRestaurants: async (query = '', limit = 5) => {
    try {
      const response = await api.get('/api/restaurants', {
        params: { query, limit }
      })
      return response.data
    } catch (error) {
      throw new Error(`Failed to fetch restaurants: ${error.message}`)
    }
  },

  // Busca avançada (mantido para compatibilidade)
  searchRestaurants: async ({ query, location, maxResults = 5 }) => {
    try {
      const response = await api.post('/api/search', {
        query,
        location,
        max_results: maxResults
      })
      return response.data
    } catch (error) {
      if (error.response?.status === 400) {
        throw new Error(error.response.data.message || 'Invalid search parameters')
      }
      throw new Error(`Search failed: ${error.message}`)
    }
  },

  // Processar localização (mantido para compatibilidade)
  processLocation: async (locationInput) => {
    try {
      const response = await api.post('/api/location', {
        input: locationInput
      })
      return response.data
    } catch (error) {
      if (error.response?.status === 400) {
        throw new Error(error.response.data.message || 'Invalid location input')
      }
      throw new Error(`Location processing failed: ${error.message}`)
    }
  }
}

export default api

