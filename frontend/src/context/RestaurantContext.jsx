import { createContext, useContext, useState } from 'react'
import useGeolocation from '../hooks/useGeolocation'
import locationService from '../services/locationService'

const RestaurantContext = createContext()

export const useRestaurants = () => {
  const context = useContext(RestaurantContext)
  if (!context) {
    throw new Error('useRestaurants deve ser usado dentro de um RestaurantProvider')
  }
  return context
}

export const RestaurantProvider = ({ children }) => {
  const [restaurants, setRestaurants] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [currentQuery, setCurrentQuery] = useState('')
  const [locationSent, setLocationSent] = useState(false)

  // Hook de geolocalização
  const {
    location,
    loading: locationLoading,
    error: locationError,
    permission,
    isSupported,
    requestLocation,
    loadCachedLocation,
    clearLocationCache
  } = useGeolocation()

  // Enviar localização para o backend
  const sendLocationToBackend = async (locationData) => {
    if (!locationData || locationSent) return

    try {
      setLoading(true)
      console.log('Enviando localização para o backend:', locationData)
      
      const response = await locationService.sendLocationToBackend(locationData)
      console.log('Resposta do backend:', response)
      
      setLocationSent(true)
      
      // Obter recomendações baseadas na localização
      await getRecommendations(locationData)
      
    } catch (error) {
      console.error('Erro ao enviar localização:', error)
      setError('Erro ao enviar localização para o servidor')
    } finally {
      setLoading(false)
    }
  }

  // Obter recomendações baseadas na localização
  const getRecommendations = async (locationData) => {
    try {
      setLoading(true)
      console.log('Obtendo recomendações para:', locationData)
      
      const response = await locationService.getRecommendations(locationData, {
        maxResults: 5,
        maxDistance: 2.0
      })
      
      console.log('Recomendações obtidas:', response)
      
      if (response.restaurants) {
        setRestaurants(response.restaurants)
      }
      
    } catch (error) {
      console.error('Erro ao obter recomendações:', error)
      setError('Erro ao obter recomendações')
    } finally {
      setLoading(false)
    }
  }

  // Buscar restaurantes
  const searchRestaurants = async (query) => {
    try {
      setLoading(true)
      setCurrentQuery(query)
      setError(null)

      // Simular busca (por enquanto)
      setTimeout(() => {
        setRestaurants([])
        setLoading(false)
      }, 1000)

    } catch (error) {
      setError('Erro ao buscar restaurantes')
      setLoading(false)
    }
  }

  // Limpar erro
  const clearError = () => {
    setError(null)
  }

  // Forçar nova localização
  const refreshLocation = async () => {
    try {
      clearLocationCache()
      setLocationSent(false)
      setError(null)
      
      const newLocation = await requestLocation()
      if (newLocation) {
        await sendLocationToBackend(newLocation)
      }
    } catch (error) {
      console.error('Erro ao atualizar localização:', error)
      setError('Erro ao atualizar localização')
    }
  }

  // Obter informações da localização atual
  const getLocationInfo = () => {
    if (!location) return null
    return locationService.getLocationInfo(location)
  }

  // Inicializar localização manualmente (não automático)
  const initializeLocation = async () => {
    try {
      // Primeiro, tentar carregar do cache
      const cachedLocation = loadCachedLocation()
      
      if (cachedLocation) {
        console.log('Localização carregada do cache:', cachedLocation)
        await sendLocationToBackend(cachedLocation)
        return
      }

      // Se não há cache, solicitar nova localização
      if (isSupported) {
        console.log('Solicitando nova localização...')
        const newLocation = await requestLocation()
        
        if (newLocation) {
          console.log('Nova localização obtida:', newLocation)
          await sendLocationToBackend(newLocation)
        }
      }
    } catch (error) {
      console.error('Erro ao inicializar localização:', error)
    }
  }

  const value = {
    // Estado dos restaurantes
    restaurants,
    loading,
    error,
    currentQuery,
    
    // Estado da localização
    location,
    locationLoading,
    locationError,
    permission,
    isSupported,
    locationSent,
    
    // Funções
    setRestaurants,
    setLoading,
    setError,
    setCurrentQuery,
    clearError,
    searchRestaurants,
    
    // Funções de localização
    requestLocation,
    refreshLocation,
    getLocationInfo,
    sendLocationToBackend,
    initializeLocation
  }

  return (
    <RestaurantContext.Provider value={value}>
      {children}
    </RestaurantContext.Provider>
  )
}
