import { createContext, useContext, useState, useEffect } from 'react'
import useGeolocation from '../hooks/useGeolocation'
import locationService from '../services/locationService'
import { restaurantAPI } from '../services/api'
import { FrontendValidator, BusinessRulesService } from '../services/businessRules'

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
  const [dynamicTitle, setDynamicTitle] = useState('')
  const [locationSent, setLocationSent] = useState(false)
  const [businessRulesLoaded, setBusinessRulesLoaded] = useState(false)

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

  // sincronizar regras de negócio com o backend
  useEffect(() => {
    const syncRules = async () => {
      try {
        await BusinessRulesService.syncBusinessRules()
        setBusinessRulesLoaded(true)
      } catch (error) {
        setBusinessRulesLoaded(true) // continuar mesmo com erro
      }
    }
    
    syncRules()
  }, [])

  // Enviar localização para o backend
  const sendLocationToBackend = async (locationData) => {
    if (!locationData || locationSent) return

    try {
      setLoading(true)
      
      const response = await locationService.sendLocationToBackend(locationData)
      
      setLocationSent(true)
      
      // Obter recomendações baseadas na localização
      await getRecommendations(locationData)
      
    } catch (error) {
      setError('Erro ao enviar localização para o servidor')
    } finally {
      setLoading(false)
    }
  }

  // Obter recomendações baseadas na localização
  const getRecommendations = async (locationData) => {
    try {
      setLoading(true)
      
      const response = await locationService.getRecommendations(locationData, {
        maxResults: 5,
        maxDistance: 2.0
      })
      
      if (response.restaurants) {
        setRestaurants(response.restaurants)
      }
      
    } catch (error) {
      setError('Erro ao obter recomendações')
    } finally {
      setLoading(false)
    }
  }

  // Buscar restaurantes com API real
  const searchRestaurants = async (query) => {
    try {
      setLoading(true)
      setCurrentQuery(query)
      setError(null)

      // validar entrada usando regras de negócio
      const validationErrors = FrontendValidator.validateSearchData({
        text: query,
        latitude: location?.latitude,
        longitude: location?.longitude
      })

      if (validationErrors.length > 0) {
        throw new Error(`erros de validação: ${validationErrors.join(', ')}`)
      }

      // Verificar se temos localização
      if (!location) {
        throw new Error('Localização não disponível. Por favor, permita o acesso à localização.')
      }

      // sanitizar texto da consulta
      const sanitizedQuery = FrontendValidator.sanitizeQueryText(query)

      // Chamar API real do backend
      const response = await restaurantAPI.getRecommendations(
        sanitizedQuery,
        location.latitude,
        location.longitude
      )

      if (response.data && response.data.recommendations) {
        const recommendations = response.data.recommendations
        const title = response.data.dynamic_title || 'Restaurantes Encontrados'
        
        setRestaurants(recommendations)
        setDynamicTitle(title)
      } else {
        setRestaurants([])
        setDynamicTitle('Restaurantes Encontrados')
      }

    } catch (error) {
      setError(error.message || 'Erro ao buscar restaurantes')
      setRestaurants([])
    } finally {
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
        await sendLocationToBackend(cachedLocation)
        return
      }

      // Se não há cache, solicitar nova localização
      if (isSupported) {
        const newLocation = await requestLocation()
        
        if (newLocation) {
          await sendLocationToBackend(newLocation)
        }
      }
    } catch (error) {
      // Silenciar erro de inicialização
    }
  }

  const value = {
    // Estado dos restaurantes
    restaurants,
    loading,
    error,
    currentQuery,
    dynamicTitle,
    
    // Estado da localização
    location,
    locationLoading,
    locationError,
    permission,
    isSupported,
    locationSent,
    
    // Estado das regras de negócio
    businessRulesLoaded,
    
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
