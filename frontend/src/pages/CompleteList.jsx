import { Link } from 'react-router-dom'
import { useRestaurants } from '../context/RestaurantContext'
import LoadingSpinner from '../components/LoadingSpinner'

// Dados mockados para demonstração
const MOCK_RESTAURANTS = [
  {
    id: "1",
    name: "Restaurante Janga Praia",
    rating: 5,
    address: "Ponta Verde, Maceió - AL",
    distance: "1 km de você",
    rank: 1,
    category: "Frutos do Mar",
    price_level: 3
  },
  {
    id: "2", 
    name: "Piccola Villa",
    rating: 5,
    address: "Pajuçara, Maceió - AL",
    distance: "1 km de você",
    rank: 2,
    category: "Italiana",
    price_level: 4
  },
  {
    id: "3",
    name: "Restaurante Caruva", 
    rating: 5,
    address: "Ponta Verde, Maceió - AL",
    distance: "1 km de você",
    rank: 3,
    category: "Regional",
    price_level: 2
  },
  {
    id: "4",
    name: "Villa Gourmet",
    rating: 4,
    address: "Centro, Maceió - AL",
    distance: "2 km de você", 
    rank: 4,
    category: "Internacional",
    price_level: 4
  },
  {
    id: "5",
    name: "Sabor da Terra",
    rating: 4,
    address: "Farol, Maceió - AL",
    distance: "3 km de você",
    rank: 5,
    category: "Regional",
    price_level: 2
  },
  {
    id: "6",
    name: "Cantinho do Mar",
    rating: 4,
    address: "Pajuçara, Maceió - AL",
    distance: "4 km de você",
    rank: 6,
    category: "Frutos do Mar",
    price_level: 3
  },
  {
    id: "7",
    name: "Pizzaria Bella Vista",
    rating: 4,
    address: "Ponta Verde, Maceió - AL",
    distance: "5 km de você",
    rank: 7,
    category: "Pizza",
    price_level: 2
  },
  {
    id: "8",
    name: "Restaurante Sabor Caseiro",
    rating: 3,
    address: "Centro, Maceió - AL",
    distance: "6 km de você",
    rank: 8,
    category: "Regional",
    price_level: 1
  },
  {
    id: "9",
    name: "Sushi Bar Premium",
    rating: 5,
    address: "Ponta Verde, Maceió - AL",
    distance: "7 km de você",
    rank: 9,
    category: "Japonesa",
    price_level: 5
  },
  {
    id: "10",
    name: "Churrascaria Gaúcha",
    rating: 4,
    address: "Farol, Maceió - AL",
    distance: "8 km de você",
    rank: 10,
    category: "Churrasco",
    price_level: 4
  }
]

const CompleteList = () => {
  const { restaurants } = useRestaurants()
  
  // Usar dados mockados se não houver dados do contexto
  const displayRestaurants = restaurants.length > 0 ? restaurants : MOCK_RESTAURANTS

  // Agrupar restaurantes por categoria
  const restaurantsByCategory = displayRestaurants.reduce((acc, restaurant) => {
    if (!acc[restaurant.category]) {
      acc[restaurant.category] = []
    }
    acc[restaurant.category].push(restaurant)
    return acc
  }, {})

  // Ordenar categorias por número de restaurantes
  const sortedCategories = Object.keys(restaurantsByCategory).sort((a, b) => 
    restaurantsByCategory[b].length - restaurantsByCategory[a].length
  )

  return (
    <div className="min-h-screen bg-figma-bg font-alexandria overflow-hidden">
      {/* Container principal seguindo o design do Figma */}
      <div className="Version2Resposta relative w-full h-full max-w-screen-xl max-h-screen mx-auto" style={{width: '1200px', height: '800px', position: 'relative', background: '#181818', boxShadow: '0px 4px 4px rgba(0, 0, 0, 0.25)', overflow: 'hidden'}}>
        
        {/* Logo sabora */}
        <div className="absolute text-center text-figma-placeholder text-lg font-medium leading-6" style={{left: '30px', top: '50px', fontSize: '18px', lineHeight: '20px'}}>
          sabora
        </div>

        {/* Retângulo principal - AUMENTADO */}
        <div className="absolute bg-figma-gray" style={{width: '900px', height: '750px', left: '150px', top: '30px', borderTopLeftRadius: '25px', borderTopRightRadius: '25px'}} />

        {/* Frame com título */}
        <div className="absolute flex justify-between items-center" style={{width: '800px', left: '190px', top: '70px'}}>
          <div className="text-justify text-figma-text text-2xl font-normal leading-6" style={{fontSize: '28px', lineHeight: '20px'}}>
            Top {displayRestaurants.length}
          </div>
          <div className="text-justify text-figma-text text-xl font-normal leading-6" style={{fontSize: '20px', lineHeight: '20px'}}>
            Restaurantes por Categoria
          </div>
        </div>

        {/* Container scrollável para os cards - ORGANIZADO POR CATEGORIA */}
        <div className="absolute overflow-y-auto" style={{
          width: '860px',
          height: '600px',
          left: '165px',
          top: '120px',
          scrollbarWidth: 'none',
          msOverflowStyle: 'none'
        }}>
          <style jsx>{`
            .scrollable-container::-webkit-scrollbar {
              display: none;
            }
          `}</style>
          
          <div className="flex gap-8">
            {/* Coluna Esquerda */}
            <div className="flex-1">
              {sortedCategories.slice(0, Math.ceil(sortedCategories.length / 2)).map((category, categoryIndex) => (
                <div key={category} className="mb-8">
                  {/* Título da Categoria */}
                  <div className="text-justify text-figma-text text-lg font-semibold leading-6 mb-4" style={{fontSize: '18px', lineHeight: '20px', borderBottom: '2px solid #575757', paddingBottom: '8px'}}>
                    {category}
                  </div>
                  
                  {/* Restaurantes da Categoria */}
                  {restaurantsByCategory[category].map((restaurant, index) => (
                    <div 
                      key={restaurant.id}
                      className="flex justify-between items-center mb-3"
                      style={{
                        width: '400px',
                        padding: '8px 0'
                      }}
                    >
                      {/* Nome e Localização */}
                      <div className="flex flex-col justify-start items-start gap-1" style={{width: '280px'}}>
                        <div className="text-justify text-figma-text text-sm font-medium leading-6" style={{fontSize: '14px', lineHeight: '18px'}}>
                          {restaurant.name}
                        </div>
                        <div className="text-justify text-figma-placeholder text-xs font-normal leading-6" style={{fontSize: '10px', lineHeight: '18px'}}>
                          {restaurant.address}
                        </div>
                      </div>
                      
                      {/* Distância e Ranking */}
                      <div className="flex flex-col justify-end items-end gap-1" style={{width: '100px'}}>
                        <div className="text-justify text-figma-placeholder text-xs font-medium leading-6" style={{fontSize: '12px', lineHeight: '18px'}}>
                          {restaurant.distance}
                        </div>
                        <div className="text-justify text-figma-text text-xs font-semibold leading-6" style={{fontSize: '12px', lineHeight: '18px'}}>
                          #{restaurant.rank}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ))}
            </div>

            {/* Coluna Direita */}
            <div className="flex-1">
              {sortedCategories.slice(Math.ceil(sortedCategories.length / 2)).map((category, categoryIndex) => (
                <div key={category} className="mb-8">
                  {/* Título da Categoria */}
                  <div className="text-justify text-figma-text text-lg font-semibold leading-6 mb-4" style={{fontSize: '18px', lineHeight: '20px', borderBottom: '2px solid #575757', paddingBottom: '8px'}}>
                    {category}
                  </div>
                  
                  {/* Restaurantes da Categoria */}
                  {restaurantsByCategory[category].map((restaurant, index) => (
                    <div 
                      key={restaurant.id}
                      className="flex justify-between items-center mb-3"
                      style={{
                        width: '400px',
                        padding: '8px 0'
                      }}
                    >
                      {/* Nome e Localização */}
                      <div className="flex flex-col justify-start items-start gap-1" style={{width: '280px'}}>
                        <div className="text-justify text-figma-text text-sm font-medium leading-6" style={{fontSize: '14px', lineHeight: '18px'}}>
                          {restaurant.name}
                        </div>
                        <div className="text-justify text-figma-placeholder text-xs font-normal leading-6" style={{fontSize: '10px', lineHeight: '18px'}}>
                          {restaurant.address}
                        </div>
                      </div>
                      
                      {/* Distância e Ranking */}
                      <div className="flex flex-col justify-end items-end gap-1" style={{width: '100px'}}>
                        <div className="text-justify text-figma-placeholder text-xs font-medium leading-6" style={{fontSize: '12px', lineHeight: '18px'}}>
                          {restaurant.distance}
                        </div>
                        <div className="text-justify text-figma-text text-xs font-semibold leading-6" style={{fontSize: '12px', lineHeight: '18px'}}>
                          #{restaurant.rank}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Barra de busca */}
        <div className="absolute bg-figma-gray-dark rounded-full" style={{width: '240px', height: '32px', left: '480px', top: '720px'}} />
        <div className="absolute text-center text-figma-placeholder text-xs font-normal leading-6" style={{left: '490px', top: '728px', fontSize: '10px', lineHeight: '18px'}}>
          Pesquisar
        </div>

        {/* Loading state */}
        {displayRestaurants.length === 0 && (
          <div className="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2">
            <LoadingSpinner size="lg" />
          </div>
        )}

        {/* Indicador de scroll */}
        {sortedCategories.length > 4 && (
          <div className="absolute right-4 top-1/2 transform -translate-y-1/2 text-figma-placeholder text-xs opacity-50">
            Scroll para ver mais
          </div>
        )}
      </div>
    </div>
  )
}

export default CompleteList