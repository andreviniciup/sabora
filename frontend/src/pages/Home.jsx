import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useRestaurants } from '../context/RestaurantContext'
import LoadingSpinner from '../components/LoadingSpinner'
import SearchBar from '../components/SearchBar'

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
  },
  {
    id: "4",
    name: "Villa Gourmet",
    rating: 4,
    address: "R. das Flores, 123 - Centro, Maceió - AL",
    distance: "2 km de você", 
    rank: 4,
    category: "Internacional",
    price_level: 4
  },
  {
    id: "5",
    name: "Sabor da Terra",
    rating: 4,
    address: "Av. Brasil, 456 - Farol, Maceió - AL",
    distance: "3 km de você",
    rank: 5,
    category: "Regional",
    price_level: 2
  }
]

const Home = () => {
  const [query, setQuery] = useState('')
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { setRestaurants, setCurrentQuery, clearError, requestLocation } = useRestaurants()

  // Solicitar localização automaticamente quando a página carregar
  useEffect(() => {
    const getLocation = async () => {
      try {
        const location = await requestLocation()
        console.log(' Localização obtida:', location)
        console.log('Latitude:', location?.latitude)
        console.log('Longitude:', location?.longitude)
        console.log('Precisão:', location?.accuracy, 'metros')
      } catch (error) {
        console.log('Erro ao obter localização:', error.message)
      }
    }
    getLocation()
  }, [requestLocation])

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

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  return (
    <div className="min-h-screen bg-figma-bg font-alexandria overflow-hidden">
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
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Home