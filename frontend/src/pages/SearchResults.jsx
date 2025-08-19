import { Link } from 'react-router-dom'
import { useRestaurants } from '../context/RestaurantContext'
import LoadingSpinner from '../components/LoadingSpinner'

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

const SearchResults = () => {
  const { restaurants, loading, error, currentQuery } = useRestaurants()
  
  // Usar dados mockados se não houver dados do contexto
  const displayRestaurants = restaurants.length > 0 ? restaurants : MOCK_RESTAURANTS
  const displayLoading = loading && restaurants.length === 0

  return (
    <div className="min-h-screen bg-figma-bg font-alexandria overflow-hidden">
      {/* Container principal seguindo o design do Figma */}
      <div className="Version2Resposta relative w-full h-full max-w-screen-xl max-h-screen mx-auto" style={{width: '1200px', height: '800px'}}>
        
        {/* Logo sabora */}
        <div className="absolute left-8 top-12 text-center text-figma-placeholder text-lg font-medium leading-6" style={{left: '30px', top: '50px', fontSize: '18px', lineHeight: '20px'}}>
          sabora
        </div>

        {/* Texto de resposta */}
        <div className="absolute left-30 top-32 text-justify" style={{width: '350px', left: '120px', top: '130px'}}>
          <span className="text-figma-text text-2xl font-medium leading-6" style={{fontSize: '28px', lineHeight: '20px'}}>
            Sua lista está pronta! <br/>
          </span>
          <span className="text-figma-text text-xl font-medium leading-6" style={{fontSize: '20px', lineHeight: '20px'}}>
            <br/>Estes são os restaurantes mais interessantes e saborosos perto de você. <br/><br/>
          </span>
          <span className="text-figma-text text-lg font-medium leading-6" style={{fontSize: '18px', lineHeight: '20px'}}>
            Prepare-se para se surpreender a cada prato.
          </span>
        </div>

        {/* Título dos restaurantes */}
        <div className="absolute left-160 top-32 text-justify text-figma-text text-xl font-medium leading-6" style={{left: '650px', top: '130px', fontSize: '20px', lineHeight: '20px'}}>
          Restaurantes 5 estrelas
        </div>

        {/* Lista de restaurantes */}
        <div className="space-y-6">
          {displayLoading ? (
            <div className="flex justify-center py-12">
              <LoadingSpinner size="lg" />
            </div>
          ) : displayRestaurants.length > 0 ? (
            displayRestaurants.slice(0, 3).map((restaurant, index) => (
              <div 
                key={restaurant.id}
                className="absolute bg-figma-gray rounded-2xl flex flex-col justify-start items-start gap-2.5"
                style={{
                  width: '420px',
                  padding: '16px 32px',
                  left: '650px',
                  top: `${170 + (index * 150)}px`,
                  borderRadius: '16px'
                }}
              >
                <div className="w-full flex flex-col justify-start items-start gap-3">
                  {/* Distância */}
                  <div className="w-full p-2 flex justify-end items-center gap-2">
                    <div className="text-justify text-figma-placeholder text-xs font-medium leading-6" style={{fontSize: '12px', lineHeight: '18px'}}>
                      {restaurant.distance}
                    </div>
                  </div>
                  
                  {/* Conteúdo principal */}
                  <div className="flex justify-start items-center gap-2">
                    {/* Número */}
                    <div className="text-justify text-figma-text font-semibold leading-6" style={{fontSize: '96px', lineHeight: '18px'}}>
                      {index + 1}.
                    </div>
                    
                    {/* Informações */}
                    <div className="w-60 flex flex-col justify-start items-start gap-2" style={{width: '240px'}}>
                      <div className="w-40 flex flex-col justify-start items-start gap-2" style={{width: '160px'}}>
                        <div className="w-full text-justify text-figma-text text-sm font-medium leading-6" style={{fontSize: '14px', lineHeight: '18px'}}>
                          {restaurant.name}
                        </div>
                      </div>
                      <div className="w-full text-justify text-figma-placeholder text-xs font-normal leading-6" style={{fontSize: '10px', lineHeight: '18px'}}>
                        {restaurant.address}
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-12">
              <p className="text-figma-placeholder text-lg">
                {currentQuery ? 
                  'Nenhum restaurante encontrado. Tente uma busca diferente.' :
                  'Faça uma busca para ver os restaurantes.'
                }
              </p>
            </div>
          )}
        </div>

        {/* Barra de busca */}
        <div className="absolute bg-figma-gray rounded-full" style={{width: '330px', height: '32px', left: '120px', top: '600px'}}>
          <div className="absolute text-center text-figma-placeholder text-xs font-normal leading-6" style={{width: '50px', left: '12px', top: '6px', fontSize: '10px', lineHeight: '18px'}}>
            Pesquisar
          </div>
        </div>

        {/* Botão Ver Completo */}
        {displayRestaurants.length > 0 && (
          <div className="absolute p-2 justify-center items-center gap-2" style={{left: '840px', top: '630px'}}>
            <Link 
              to="/complete-list"
              className="text-justify text-figma-text text-xs font-normal underline leading-6 hover:text-figma-placeholder transition-colors" 
              style={{fontSize: '12px', lineHeight: '18px'}}
            >
              Ver Completo
            </Link>
          </div>
        )}

        {/* Error message */}
        {error && (
          <div className="absolute left-30 top-80 bg-red-500/10 border border-red-500/20 rounded-lg p-4 text-red-400" style={{left: '120px', top: '320px'}}>
            <p className="font-medium">Erro na busca</p>
            <p className="text-sm">{error}</p>
          </div>
        )}
      </div>
    </div>
  )
}

export default SearchResults
