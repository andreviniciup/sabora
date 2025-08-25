import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useRestaurants } from '../context/RestaurantContext'
import LoadingSpinner from '../components/LoadingSpinner'
import SearchBar from '../components/SearchBar'
import ErrorNotification from '../components/ErrorNotification'
import ApiTest from '../components/ApiTest'

const Home = () => {
  const [query, setQuery] = useState('')
  const navigate = useNavigate()
  const { 
    searchRestaurants, 
    loading, 
    error, 
    clearError, 
    requestLocation,
    location,
    restaurants
  } = useRestaurants()

  // Solicitar localização automaticamente quando a página carregar
  useEffect(() => {
    const getLocation = async () => {
      try {
        const location = await requestLocation()
        console.log('Localização obtida:', location)
        console.log('Latitude:', location?.latitude)
        console.log('Longitude:', location?.longitude)
        console.log('Precisão:', location?.accuracy, 'metros')
      } catch (error) {
        console.log('Erro ao obter localização:', error.message)
      }
    }
    getLocation()
  }, [requestLocation])

  const [searchAttempted, setSearchAttempted] = useState(false)

  // Monitorar quando a busca é bem-sucedida
  useEffect(() => {
    if (searchAttempted && !loading && !error && restaurants.length > 0) {
      console.log('Busca concluída com sucesso, navegando para resultados')
      navigate('/search-results')
      setSearchAttempted(false)
    }
  }, [loading, error, restaurants, searchAttempted, navigate])

  const handleSearch = async () => {
    if (!query.trim()) return

    console.log('Iniciando busca com query:', query)
    console.log('Localização disponível:', location)

    try {
      clearError()
      setSearchAttempted(true)
      
      // Usar a função de busca real do contexto
      await searchRestaurants(query)
      
    } catch (error) {
      console.error('Search error:', error)
      setSearchAttempted(false)
      // O erro já é tratado no contexto, não precisa fazer nada aqui
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  return (
    <div className="min-h-screen bg-figma-bg font-alexandria overflow-hidden">
      {/* Notificação de erro */}
      <ErrorNotification 
        error={error} 
        onClose={clearError}
      />
      
      {/* Desktop Layout */}
      <div className="hidden lg:block">
        <div className="Version2 relative w-full h-full max-w-screen-xl max-h-screen mx-auto" style={{width: '1512px', height: '982px'}}>
          
          {/* Container principal centralizado */}
          <div className="Principal absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 flex flex-col items-center gap-6" style={{width: '388px'}}>
            
            {/* Imagem do restaurante */}
            <img 
              className="w-28 h-28" 
              src="/restaurant-icon.png" 
              alt="Restaurant Icon"
              onError={(e) => {
                e.target.src = 'https://placehold.co/112x112/3D3D3D/FAFAFA?text=🍽️'
              }}
              style={{width: '112px', height: '112px'}}
            /> 
            
            {/* Título principal */}
            <div className="text-center text-figma-text text-xl font-medium leading-6">
              O que combina com você hoje?
            </div>
            
            {/* Barra de busca */}
            <SearchBar 
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onSearch={handleSearch}
              onKeyPress={handleKeyPress}
              placeholder="Pesquisar"
              loading={loading}
              controlled={true}
              className="w-full"
            />
            

            
            {/* Aviso de localização */}
            {!location && (
              <div className="w-full bg-yellow-500/10 border border-yellow-500/20 rounded-lg p-3 text-yellow-400 text-sm">
                <p>⚠️ Permitindo acesso à localização para melhores resultados...</p>
              </div>
            )}
            
            {/* Componente de teste da API (apenas em desenvolvimento) */}
            {import.meta.env.DEV && (
              <div className="w-full mt-4">
                <ApiTest />
              </div>
            )}
          </div>
          
          {/* Logo sabora na parte inferior */}
          <div className="absolute left-1/2 bottom-8 transform -translate-x-1/2 text-center text-figma-gray-dark text-2xl font-medium leading-6" style={{fontSize: '24px', lineHeight: '23px'}}>
            sabora
          </div>
        </div>
      </div>

      {/* Mobile Layout */}
      <div className="lg:hidden">
        <div className="HomeMobile w-full h-screen py-[22px] bg-neutral-900 inline-flex justify-start items-start gap-2.5 overflow-hidden">
          <div className="Frame36 w-full inline-flex flex-col justify-start items-start gap-[248px]">
            
            {/* Header com logo */}
            <div className="Frame35 self-stretch px-5 py-2.5 inline-flex justify-start items-center gap-2.5">
              <div className="Logo text-center justify-start text-stone-300 text-base font-medium font-['Alexandria'] leading-[23px]">
                sabora
              </div>
            </div>
            
            {/* Container principal mobile */}
            <div className="Principal self-stretch flex flex-col justify-start items-center gap-2.5">
              
              {/* Imagem do restaurante */}
              <img 
                className="Image w-20 h-20" 
                src="/restaurant-icon.png" 
                alt="Restaurant Icon"
                onError={(e) => {
                  e.target.src = 'https://placehold.co/80x80/3D3D3D/FAFAFA?text=🍽️'
                }}
              />
              
              {/* Título principal */}
              <div className="Titlr text-center justify-start text-neutral-50 text-base font-medium font-['Alexandria'] leading-[23px]">
                O que combina com você hoje?
              </div>
              
              {/* Barra de busca mobile */}
              <SearchBar 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onSearch={handleSearch}
                onKeyPress={handleKeyPress}
                placeholder="Pesquisar"
                loading={loading}
                controlled={true}
                className="w-60"
              />
              

              
              {/* Aviso de localização mobile */}
              {!location && (
                <div className="w-60 bg-yellow-500/10 border border-yellow-500/20 rounded-lg p-3 text-yellow-400 text-xs text-center">
                  <p>⚠️ Permitindo acesso à localização...</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home