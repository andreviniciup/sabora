import api from './api'

const locationService = {
  // Enviar localização para o backend
  sendLocationToBackend: async (locationData) => {
    try {
      const response = await api.post('/api/location', {
        latitude: locationData.latitude,
        longitude: locationData.longitude,
        accuracy: locationData.accuracy,
        timestamp: locationData.timestamp
      })
      return response.data
    } catch (error) {
      throw new Error('Falha ao enviar localização para o servidor')
    }
  },

  // Obter recomendações baseadas na localização
  getRecommendations: async (locationData, options = {}) => {
    try {
      const { maxResults = 5, maxDistance = 2.0 } = options
      
      const response = await api.post('/api/recommendations', {
        location: {
          latitude: locationData.latitude,
          longitude: locationData.longitude
        },
        max_results: maxResults,
        max_distance: maxDistance
      })
      
      return response.data
    } catch (error) {
      throw new Error('Falha ao obter recomendações')
    }
  },

  // Obter informações da localização (formatação, endereço, etc.)
  getLocationInfo: (locationData) => {
    if (!locationData) return null
    
    return {
      coordinates: {
        lat: locationData.latitude,
        lng: locationData.longitude
      },
      accuracy: locationData.accuracy,
      timestamp: new Date(locationData.timestamp),
      formatted: `${locationData.latitude.toFixed(6)}, ${locationData.longitude.toFixed(6)}`
    }
  },

  // Calcular distância entre duas coordenadas (fórmula de Haversine)
  calculateDistance: (lat1, lon1, lat2, lon2) => {
    const R = 6371 // Raio da Terra em km
    const dLat = (lat2 - lat1) * Math.PI / 180
    const dLon = (lon2 - lon1) * Math.PI / 180
    const a = 
      Math.sin(dLat/2) * Math.sin(dLat/2) +
      Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
      Math.sin(dLon/2) * Math.sin(dLon/2)
    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a))
    const distance = R * c
    return distance
  },

  // Verificar se uma localização está dentro de um raio
  isWithinRadius: (centerLat, centerLon, targetLat, targetLon, radiusKm) => {
    const distance = locationService.calculateDistance(centerLat, centerLon, targetLat, targetLon)
    return distance <= radiusKm
  },

  // Obter endereço a partir de coordenadas (usando API de geocoding)
  getAddressFromCoordinates: async (latitude, longitude) => {
    try {
      const response = await api.get('/api/geocode', {
        params: { lat: latitude, lng: longitude }
      })
      return response.data
    } catch (error) {
      return null
    }
  },

  // Obter coordenadas a partir de endereço (usando API de geocoding)
  getCoordinatesFromAddress: async (address) => {
    try {
      const response = await api.get('/api/geocode', {
        params: { address }
      })
      return response.data
    } catch (error) {
      return null
    }
  }
}

export default locationService
