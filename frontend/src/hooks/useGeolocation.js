import { useState, useEffect, useCallback } from 'react'

const useGeolocation = () => {
  const [location, setLocation] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [permission, setPermission] = useState('prompt')
  const [isSupported, setIsSupported] = useState(false)

  // Verificar se a geolocalização é suportada
  useEffect(() => {
    setIsSupported('geolocation' in navigator)
  }, [])

  // Verificar permissão
  useEffect(() => {
    if (!isSupported) return

    const checkPermission = async () => {
      try {
        const result = await navigator.permissions.query({ name: 'geolocation' })
        setPermission(result.state)
        
        result.addEventListener('change', () => {
          setPermission(result.state)
        })
      } catch (error) {
        setPermission('prompt')
      }
    }

    checkPermission()
  }, [isSupported])

  // Carregar localização do cache
  const loadCachedLocation = useCallback(() => {
    try {
      const cached = localStorage.getItem('userLocation')
      if (cached) {
        const locationData = JSON.parse(cached)
        setLocation(locationData)
        return locationData
      }
    } catch (error) {
      // Silenciar erro de cache
    }
    return null
  }, [])

  // Limpar cache de localização
  const clearLocationCache = useCallback(() => {
    try {
      localStorage.removeItem('userLocation')
      setLocation(null)
    } catch (error) {
      // Silenciar erro de cache
    }
  }, [])

  // Salvar localização no cache
  const saveLocationToCache = useCallback((locationData) => {
    try {
      localStorage.setItem('userLocation', JSON.stringify(locationData))
    } catch (error) {
      // Silenciar erro de cache
    }
  }, [])

  // Solicitar localização
  const requestLocation = useCallback(async () => {
    if (!isSupported) {
      setError('Geolocalização não é suportada neste navegador')
      return null
    }

    setLoading(true)
    setError(null)

    try {
      const position = await new Promise((resolve, reject) => {
        navigator.geolocation.getCurrentPosition(resolve, reject, {
          enableHighAccuracy: true,
          timeout: 10000,
          maximumAge: 300000 // 5 minutos
        })
      })

      const locationData = {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
        accuracy: position.coords.accuracy,
        timestamp: position.timestamp
      }

      setLocation(locationData)
      saveLocationToCache(locationData)
      
      return locationData
    } catch (error) {
      let errorMessage = 'Erro ao obter localização'
      
      switch (error.code) {
        case error.PERMISSION_DENIED:
          errorMessage = 'Permissão de localização negada'
          setPermission('denied')
          break
        case error.POSITION_UNAVAILABLE:
          errorMessage = 'Informação de localização indisponível'
          break
        case error.TIMEOUT:
          errorMessage = 'Tempo limite excedido ao obter localização'
          break
        default:
          errorMessage = 'Erro desconhecido ao obter localização'
      }
      
      setError(errorMessage)
      return null
    } finally {
      setLoading(false)
    }
  }, [isSupported, saveLocationToCache])

  return {
    location,
    loading,
    error,
    permission,
    isSupported,
    requestLocation,
    loadCachedLocation,
    clearLocationCache,
    setLocation
  }
}

export default useGeolocation
