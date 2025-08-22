import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useRestaurants } from '../context/RestaurantContext'
import SearchInput from '../components/SearchInput'
import '../styles/responsive.css'

// Dados mockados para demonstração
const MOCK_RESTAURANTS = [
  {
    id: "1",
    name: "Restaurante Janga Praia",
    rating: 5,
    address: "Av. Silvio Carlos Viana, 1731 - Ponta Verde, Maceió - AL",
    distance: "1 km de você",
    rank: 1,
    category: "Frutos do Mar",
    price_level: 3
  },
  {
    id: "2", 
    name: "Piccola Villa",
    rating: 5,
    address: "R. Jangadeiros Alagoanos, 1564 - Pajuçara, Maceió - AL",
    distance: "1 km de você",
    rank: 2,
    category: "Italiana",
    price_level: 4
  },
  {
    id: "3",
    name: "Restaurante Caruva", 
    rating: 5,
    address: "R. Dep. José Lages, 813 - Ponta Verde, Maceió - AL",
    distance: "1 km de você",
    rank: 3,
    category: "Regional",
    price_level: 2
  }
]

const Home = () => {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const [showLocationPrompt, setShowLocationPrompt] = useState(false)
  const navigate = useNavigate()
  const { 
    setRestaurants, 
    setCurrentQuery, 
    clearError,
    permission,
    isSupported,
    requestLocation,
    location,
    locationLoading,
    locationError,
    initializeLocation
  } = useRestaurants()

  // Verificar se devemos mostrar o prompt de localização
  useEffect(() => {
    if (isSupported && permission === 'prompt' && !location) {
      setShowLocationPrompt(true)
    } else if (permission === 'granted' && !location && !locationLoading) {
      // Se temos permissão mas não temos localização, tentar obter
      initializeLocation()
    }
  }, [isSupported, permission, location, locationLoading, initializeLocation])

  // Solicitar localização manualmente
  const handleRequestLocation = async () => {
    try {
      setShowLocationPrompt(false)
      await requestLocation()
    } catch (error) {
      console.error('Erro ao solicitar localização:', error)
    }
  }

  // Dispensar prompt de localização
  const handleDismissLocationPrompt = () => {
    setShowLocationPrompt(false)
  }

  const handleSearch = async () => {
    if (!query.trim()) return

    try {
      clearError()
      setLoading(true)
      setCurrentQuery(query)

      // Simular delay de carregamento
      await new Promise(resolve => setTimeout(resolve, 1000))

      // Usar dados mockados
      setRestaurants(MOCK_RESTAURANTS)
      navigate('/search-results')
      
    } catch (error) {
      console.error('Search error:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-black font-alexandria overflow-hidden">
      {/* Container principal seguindo o design do Figma */}
      <div 
        className="Version2 responsive-container figma-desktop"
        style={{
          background: '#181818',
          overflow: 'hidden'
        }}
      >
        {/* Container principal centralizado */}
        <div 
          className="Principal responsive-absolute mobile-home-layout flex flex-col items-center gap-6"
          style={{
            width: '388px',
            left: '50%',
            top: '50%',
            transform: 'translate(-50%, -50%)',
            justifyContent: 'flex-start',
            alignItems: 'center',
            gap: '25px',
            display: 'inline-flex'
          }}
        >
          {/* Imagem do restaurante */}
          <img 
            className="Image mobile-home-image" 
            style={{width: '112px', height: '112px'}}
            src="/restaurant-icon.png" 
            alt="Restaurant Icon"
            onError={(e) => {
              e.target.src = 'https://placehold.co/112x112/3D3D3D/FAFAFA?text=🍽️'
            }}
          />
          
          {/* Título principal */}
          <div 
            className="Titlr mobile-home-title"
            style={{
              textAlign: 'center',
              color: '#FAFAFA',
              fontSize: '24px',
              fontFamily: 'Alexandria',
              fontWeight: '500',
              lineHeight: '23px',
              wordWrap: 'break-word'
            }}
          >
            O que combina com você hoje?
          </div>

          {/* Status da localização */}
          {isSupported && (
            <div className="location-status w-full max-w-sm">
              {/* Prompt para solicitar localização */}
              {showLocationPrompt && (
                <div 
                  className="bg-blue-600 text-white p-4 rounded-lg mb-4 text-center"
                  style={{
                    background: '#1E40AF',
                    borderRadius: '8px',
                    padding: '16px',
                    marginBottom: '16px'
                  }}
                >
                  <div className="flex items-center justify-center mb-2">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" className="mr-2">
                      <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                    </svg>
                    <span style={{ fontSize: '14px', fontWeight: '500' }}>Localização</span>
                  </div>
                  <p style={{ fontSize: '12px', marginBottom: '12px', opacity: 0.9 }}>
                    Permitir localização para encontrar restaurantes próximos?
                  </p>
                  <div className="flex gap-2 justify-center">
                    <button
                      onClick={handleRequestLocation}
                      className="px-4 py-2 bg-white text-blue-600 rounded-md text-sm font-medium hover:bg-gray-100"
                    >
                      Permitir
                    </button>
                    <button
                      onClick={handleDismissLocationPrompt}
                      className="px-4 py-2 bg-transparent border border-white text-white rounded-md text-sm font-medium hover:bg-white hover:bg-opacity-10"
                    >
                      Agora não
                    </button>
                  </div>
                </div>
              )}

              {/* Status da localização */}
              {!showLocationPrompt && (
                <div className="flex items-center justify-center mb-2">
                  {locationLoading && (
                    <div className="flex items-center text-gray-400 text-sm">
                      <div className="animate-spin w-4 h-4 border-2 border-gray-400 border-t-transparent rounded-full mr-2" />
                      Obtendo localização...
                    </div>
                  )}

                  {location && (
                    <div className="flex items-center text-green-400 text-sm">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" className="mr-2">
                        <path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/>
                      </svg>
                      Localização ativada
                    </div>
                  )}

                  {permission === 'denied' && (
                    <div className="text-center">
                      <div className="flex items-center justify-center text-red-400 text-sm mb-2">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" className="mr-2">
                          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                        </svg>
                        Localização negada
                      </div>
                      <p className="text-xs text-gray-500 mb-2">
                        Para melhor experiência, ative a localização nas configurações do navegador
                      </p>
                      <button
                        onClick={handleRequestLocation}
                        className="text-blue-400 text-xs underline hover:text-blue-300"
                      >
                        Tentar novamente
                      </button>
                    </div>
                  )}

                  {locationError && !location && (
                    <div className="text-center">
                      <div className="flex items-center justify-center text-orange-400 text-sm mb-2">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" className="mr-2">
                          <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
                        </svg>
                        Erro na localização
                      </div>
                      <p className="text-xs text-gray-500 mb-2">{locationError}</p>
                      <button
                        onClick={handleRequestLocation}
                        className="text-blue-400 text-xs underline hover:text-blue-300"
                      >
                        Tentar novamente
                      </button>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}

          {/* Aviso se geolocalização não for suportada */}
          {!isSupported && (
            <div className="bg-gray-600 text-white p-3 rounded-lg text-center text-sm">
              <div className="flex items-center justify-center mb-1">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor" className="mr-2">
                  <path d="M1 21h22L12 2 1 21zm12-3h-2v-2h2v2zm0-4h-2v-4h2v4z"/>
                </svg>
                Geolocalização não suportada
              </div>
              <p className="text-xs opacity-80">
                Seu navegador não suporta geolocalização
              </p>
            </div>
          )}
          
          {/* Container da barra de busca */}
          <div className="relative mobile-home-search">
            {/* Retângulo da barra de busca */}
            <div 
              className="Rectangle7"
              style={{
                width: '388px',
                height: '40px',
                background: '#3D3D3D',
                borderRadius: '999px',
                position: 'relative'
              }}
            />
            
            {/* Input de busca */}
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="Pesquisar"
              disabled={loading}
              className="absolute top-0 left-0 w-full h-full bg-transparent text-white placeholder-gray-400 px-6 rounded-full outline-none"
              style={{
                fontSize: '14px',
                fontFamily: 'Alexandria',
                fontWeight: '400',
                lineHeight: '23px'
              }}
            />
            
            {/* Botão de busca */}
            <button
              onClick={handleSearch}
              disabled={loading || !query.trim()}
              className="Rectangle47 absolute right-1 top-1 flex items-center justify-center"
              style={{
                width: '30px',
                height: '30px',
                background: loading ? '#999999' : 'white',
                borderRadius: '999px',
                border: 'none',
                cursor: loading || !query.trim() ? 'default' : 'pointer'
              }}
            >
              {loading ? (
                <div className="animate-spin w-4 h-4 border-2 border-gray-400 border-t-transparent rounded-full" />
              ) : (
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                  <path d="M21 21L16.514 16.506M19 10.5C19 15.194 15.194 19 10.5 19S2 15.194 2 10.5 5.806 2 10.5 2 19 5.806 19 10.5Z" stroke="#3D3D3D" strokeWidth="2"/>
                </svg>
              )}
            </button>
          </div>
        </div>
        
        {/* Logo sabora na parte inferior */}
        <div 
          className="Logo responsive-absolute mobile-home-logo"
          style={{
            left: '50%',
            top: '890px',
            transform: 'translateX(-50%)',
            textAlign: 'center',
            color: '#2D2D2D',
            fontSize: '24px',
            fontFamily: 'Alexandria',
            fontWeight: '500',
            lineHeight: '23px',
            wordWrap: 'break-word'
          }}
        >
          sabora
        </div>
      </div>
    </div>
  )
}

export default Home
