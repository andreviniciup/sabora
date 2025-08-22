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
  const [loading, setLoading] = useState(false)
  const navigate = useNavigate()
  const { 
    setRestaurants, 
    setCurrentQuery, 
    clearError,
    requestLocation
  } = useRestaurants()

  // Solicitar localização quando a página carregar
  useEffect(() => {
    const getLocation = async () => {
      try {
        await requestLocation()
      } catch (error) {
        console.log('Erro ao obter localização:', error.message)
      }
    }
    getLocation()
  }, [requestLocation])

  const handleSearch = async (query) => {
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
          
          {/* Container da barra de busca */}
          <div className="mobile-home-search" style={{ width: '388px' }}>
            <SearchInput
              onSearch={handleSearch}
              placeholder="Pesquisar"
              disabled={loading}
            />
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
