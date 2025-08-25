import { createContext, useContext, useState, useEffect, useCallback } from 'react'
import useGeolocation from '../hooks/useGeolocation'
import locationService from '../services/locationService'
import { restaurantAPI } from '../services/api'
import { FrontendValidator, BusinessRulesService } from '../services/businessRules'
import logger from '../services/logger.js'

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
  const [dynamicResponseText, setDynamicResponseText] = useState({
    title: 'Sua lista está pronta!',
    subtitle: 'Estes são os restaurantes mais interessantes e saborosos perto de você.',
    description: 'Prepare-se para se surpreender a cada prato.'
  })
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
    clearLocationCache,
    setLocation
  } = useGeolocation()

  // Inicializar localização manualmente (não automático) - useCallback para evitar dependência circular
  const initializeLocation = useCallback(async () => {
    try {
      // Primeiro, tentar carregar do cache
      const cachedLocation = loadCachedLocation()
      
      if (cachedLocation) {
        setLocation(cachedLocation)
        return
      }

      // Se não há cache, solicitar nova localização
      if (isSupported) {
        const newLocation = await requestLocation()
        
        if (newLocation) {
          setLocation(newLocation)
        }
      }
    } catch (error) {
      // Silenciar erro de inicialização
    }
  }, [isSupported, requestLocation, loadCachedLocation, setLocation])

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

  // Inicializar localização automaticamente - FIX: remover dependência circular
  useEffect(() => {
    const initLocation = async () => {
      if (isSupported && !location && !locationLoading) {
        await initializeLocation()
      }
    }
    
    initLocation()
  }, [isSupported, location, locationLoading]) // Remover initializeLocation da dependência

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
      logger.userEvent('search_restaurants', { query, location })
      logger.appState('RestaurantContext', 'search_started', { query })
      
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
        logger.warn('Validation errors in search', validationErrors)
        throw new Error(`erros de validação: ${validationErrors.join(', ')}`)
      }

      // Verificar se temos localização
      if (!location) {
        logger.error('Location not available for search', null, { query })
        
        // Tentar obter localização automaticamente
        const newLocation = await requestLocation()
        
        if (newLocation) {
          setLocation(newLocation)
        } else {
          throw new Error('Para buscar restaurantes, precisamos da sua localização. Por favor, permita o acesso à localização no seu navegador.')
        }
      }

      // sanitizar texto da consulta
      const sanitizedQuery = FrontendValidator.sanitizeQueryText(query)
      logger.debug('Sanitized query', { original: query, sanitized: sanitizedQuery })

      // Chamar API real do backend
      logger.info('Calling backend API', {
        query: sanitizedQuery,
        latitude: location.latitude,
        longitude: location.longitude
      })
      
      const response = await restaurantAPI.getRecommendations(
        sanitizedQuery,
        location.latitude,
        location.longitude
      )

      // FIX: Estrutura correta da resposta - response.data (não response.data.data)
      if (response.data && response.data.recommendations) {
        const recommendations = response.data.recommendations
        const title = response.data.dynamic_title || 'Restaurantes Encontrados'
        const responseText = response.data.dynamic_response_text || {
          title: 'Sua lista está pronta!',
          subtitle: 'Estes são os restaurantes mais interessantes e saborosos perto de você.',
          description: 'Prepare-se para se surpreender a cada prato.'
        }
        
        logger.info('Search successful', {
          resultsCount: recommendations.length,
          title: title,
          responseText: responseText
        })
        
        // Definir os dados no estado
        setRestaurants(recommendations || [])
        setDynamicTitle(title)
        setDynamicResponseText(responseText)
        
      } else {
        logger.warn('No recommendations found', response.data)
        
        // Se não há dados válidos, definir array vazio
        setRestaurants([])
        setDynamicTitle('Restaurantes Encontrados')
        setDynamicResponseText({
          title: 'Sua lista está pronta!',
          subtitle: 'Estes são os restaurantes mais interessantes e saborosos perto de você.',
          description: 'Prepare-se para se surpreender a cada prato.'
        })
      }

    } catch (error) {
      logger.error('Search failed', error, {
        query,
        location,
        errorMessage: error.message
      })
      
      // Verificar se é um erro de validação (400)
      if (error.response && error.response.status === 400) {
        setError(error.response.data?.message || 'Sua busca não parece ser sobre restaurantes')
      } else {
        setError(error.message || 'Erro ao buscar restaurantes')
      }
      
      // Só limpar restaurantes se for um erro real, não de validação ou rede
      if (!error.response || error.response.status >= 500) {
        setRestaurants([])
      }
      
    } finally {
      setLoading(false)
      logger.appState('RestaurantContext', 'search_completed', { 
        query, 
        resultsCount: restaurants.length 
      })
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

  const value = {
    // Estado dos restaurantes
    restaurants,
    loading,
    error,
    currentQuery,
    dynamicTitle,
    dynamicResponseText,
    
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