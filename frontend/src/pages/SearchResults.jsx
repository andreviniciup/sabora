import { Link } from 'react-router-dom'
import { useRestaurants } from '../context/RestaurantContext'
import LoadingSpinner from '../components/LoadingSpinner'
import SearchBar from '../components/SearchBar'

// dados mockados removidos - agora usando apenas dados da api

const SearchResults = () => {
  const { restaurants, loading, error, currentQuery, searchRestaurants } = useRestaurants()
  
  // usar apenas dados da api
  const displayRestaurants = restaurants || []
  const displayLoading = loading

  return (
    <div className="min-h-screen bg-neutral-900 font-alexandria overflow-hidden">
      {/* Layout Mobile */}
      <div className="lg:hidden px-[19px] py-[35px] inline-flex justify-start items-center gap-2.5 overflow-hidden">
        <div className="w-[353px] inline-flex flex-col justify-start items-start gap-8">
          {/* Logo */}
          <div className="self-stretch justify-start text-stone-300 text-base font-medium font-['Alexandria'] leading-[23px]">
            sabora
          </div>
          
          {/* Texto de resposta */}
          <div className="w-[343px] h-[156px] text-justify justify-start">
            <span className="text-zinc-300 text-2xl font-medium font-['Alexandria'] leading-[23px]">
              Sua lista está pronta! <br/><br/>
            </span>
            <span className="text-zinc-300 text-base font-medium font-['Alexandria'] leading-[23px]">
              Estes são os restaurantes mais interessantes e saborosos perto de você. <br/>
            </span>
            <span className="text-zinc-300 text-2xl font-medium font-['Alexandria'] leading-[23px]">
              <br/>
            </span>
            <span className="text-zinc-300 text-sm font-medium font-['Alexandria'] leading-[23px]">
              Prepare-se para se surpreender a cada prato.
            </span>
          </div>
          
          {/* Frame 33 */}
          <div className="self-stretch flex flex-col justify-start items-start gap-[19px]">
            {/* Título */}
            <div className="self-stretch p-2.5 inline-flex justify-start items-center gap-2.5">
              <div className="text-justify justify-start text-white text-2xl font-medium font-['Alexandria'] leading-[23px]">
                Restaurantes 5 estrelas
              </div>
            </div>
            
            {/* Frame 31 */}
            <div className="self-stretch flex flex-col justify-start items-center gap-[13px]">
              {/* Frame 30 - Lista de restaurantes */}
              <div className="self-stretch flex flex-col justify-start items-start gap-[13px]">
                {displayLoading ? (
                  <div className="flex justify-center py-12">
                    <LoadingSpinner size="lg" />
                  </div>
                ) : displayRestaurants.length > 0 ? (
                  displayRestaurants.slice(0, 3).map((restaurant, index) => (
                    <div key={restaurant.id || index} className="self-stretch p-5 bg-neutral-700 rounded-[20px] flex flex-col justify-start items-start gap-2.5">
                      <div className="self-stretch flex flex-col justify-start items-start">
                        {/* Distância */}
                        <div className="self-stretch inline-flex justify-end items-center gap-2.5">
                          <div className="text-justify justify-start text-zinc-600 text-xs font-medium font-['Alexandria'] leading-[23px]">
                            {restaurant.distance_formatted || restaurant.distance || 'distância não disponível'}
                          </div>
                        </div>
                        
                        {/* Conteúdo principal */}
                        <div className="self-stretch inline-flex justify-start items-center gap-2.5">
                          <div className="text-justify justify-start text-white text-8xl font-semibold font-['Alexandria'] leading-[23px]">
                            {restaurant.rank || (index + 1)}.
                          </div>
                          <div className="w-[223px] inline-flex flex-col justify-start items-start gap-2.5">
                            <div className="w-[185px] flex flex-col justify-start items-start gap-[5px]">
                              <div className="self-stretch text-justify justify-start text-white text-base font-medium font-['Alexandria'] leading-[23px]">
                                {restaurant.name}
                              </div>
                              {/* Stars */}
                              <div className="flex items-center gap-1">
                                {[...Array(Math.floor(restaurant.rating || 0))].map((_, starIndex) => (
                                  <svg 
                                    key={starIndex}
                                    width="16" 
                                    height="15" 
                                    viewBox="0 0 20 19" 
                                    fill="none" 
                                    xmlns="http://www.w3.org/2000/svg"
                                  >
                                    <path 
                                      d="M10 0L12.2451 6.90983H19.5106L13.6327 11.1803L15.8779 18.0902L10 13.8197L4.12215 18.0902L6.36729 11.1803L0.489435 6.90983H7.75486L10 0Z" 
                                      fill="#C5AA50"
                                    />
                                  </svg>
                                ))}
                              </div>
                            </div>
                            <div className="self-stretch text-justify justify-start text-neutral-400 text-xs font-normal font-['Alexandria'] leading-[23px]">
                              {restaurant.address}
                            </div>
                            {restaurant.cuisine_type && (
                              <div className="self-stretch text-justify justify-start text-neutral-500 text-xs font-normal font-['Alexandria'] leading-[18px]">
                                {restaurant.cuisine_type}
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-12">
                    <p className="text-neutral-400 text-lg">
                      {currentQuery ? 
                        'Nenhum restaurante encontrado. Tente uma busca diferente.' :
                        'Faça uma busca para ver os restaurantes.'
                      }
                    </p>
                  </div>
                )}
              </div>
              
              {/* Botão Ver Completo */}
              {displayRestaurants.length > 0 && (
                <div className="w-[353px] h-8 p-2.5 inline-flex justify-center items-center gap-2.5">
                  <Link 
                    to="/complete-list"
                    className="text-justify justify-start text-white text-xs font-normal font-['Alexandria'] underline leading-[23px] hover:text-neutral-400 transition-colors"
                  >
                    Ver Completo
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Layout Desktop */}
      <div className="hidden lg:block w-full max-w-[1200px] h-screen px-[80px] py-[60px] bg-neutral-900 inline-flex flex-col justify-center items-center gap-2.5 overflow-hidden mx-auto">
        <div className="w-full max-w-[1040px] flex flex-col justify-start items-start gap-[40px]">
          {/* Logo */}
          <div className="p-2.5 inline-flex justify-center items-center gap-2.5">
            <div className="text-center justify-start text-stone-300 text-xl font-medium font-['Alexandria'] leading-[23px]">
              sabora
            </div>
          </div>
          
          {/* Frame 19 */}
          <div className="self-stretch inline-flex justify-start items-start gap-[150px]">
            {/* Frame 18 - Texto de resposta */}
            <div className="p-2.5 flex justify-center items-center gap-2.5">
              <div className="w-[320px] text-justify justify-start">
                <span className="text-zinc-300 text-[24px] font-medium font-['Alexandria'] leading-[20px]">
                  Sua lista está pronta! <br/>
                </span>
                <span className="text-zinc-300 text-lg font-medium font-['Alexandria'] leading-[18px]">
                  <br/>Estes são os restaurantes mais interessantes e saborosos perto de você. <br/><br/>
                </span>
                <span className="text-zinc-300 text-base font-medium font-['Alexandria'] leading-[16px]">
                  Prepare-se para se surpreender a cada prato.
                </span>
              </div>
            </div>
            
            {/* Frame 16 - Lista de restaurantes */}
            <div className="w-[450px] inline-flex flex-col justify-center items-center gap-[8px]">
              {/* Título */}
              <div className="self-stretch p-2.5 inline-flex justify-start items-center gap-2.5">
                <div className="text-justify justify-start text-white text-xl font-medium font-['Alexandria'] leading-[18px]">
                  Restaurantes 5 estrelas
                </div>
              </div>
              
              {/* Frame 14 - Lista */}
              <div className="w-[440px] flex flex-col justify-start items-start gap-2.5">
                {displayLoading ? (
                  <div className="flex justify-center py-12">
                    <LoadingSpinner size="lg" />
                  </div>
                ) : displayRestaurants.length > 0 ? (
                  displayRestaurants.slice(0, 3).map((restaurant, index) => (
                    <div key={restaurant.id || index} className="self-stretch px-6 py-3 bg-neutral-700 rounded-[16px] flex flex-col justify-start items-start gap-2">
                      <div className="self-stretch flex flex-col justify-start items-start gap-2">
                        {/* Distância */}
                        <div className="self-stretch p-1 inline-flex justify-end items-center gap-2">
                          <div className="text-justify justify-start text-zinc-600 text-xs font-medium font-['Alexandria'] leading-[16px]">
                            {restaurant.distance_formatted || restaurant.distance || 'distância não disponível'}
                          </div>
                        </div>
                        
                        {/* Item principal */}
                        <div className="inline-flex justify-start items-center gap-2">
                          <div className="text-justify justify-start text-white text-6xl font-semibold font-['Alexandria'] leading-[16px]">
                            {restaurant.rank || (index + 1)}.
                          </div>
                          <div className="w-[240px] inline-flex flex-col justify-start items-start gap-2">
                            <div className="w-[140px] flex flex-col justify-start items-start gap-1">
                              <div className="self-stretch text-justify justify-start text-white text-sm font-medium font-['Alexandria'] leading-[16px]">
                                {restaurant.name}
                              </div>
                              {/* Stars */}
                              <div className="flex items-center gap-1">
                                {[...Array(Math.floor(restaurant.rating || 0))].map((_, starIndex) => (
                                  <svg 
                                    key={starIndex}
                                    width="14" 
                                    height="13" 
                                    viewBox="0 0 20 19" 
                                    fill="none" 
                                    xmlns="http://www.w3.org/2000/svg"
                                  >
                                    <path 
                                      d="M10 0L12.2451 6.90983H19.5106L13.6327 11.1803L15.8779 18.0902L10 13.8197L4.12215 18.0902L6.36729 11.1803L0.489435 6.90983H7.75486L10 0Z" 
                                      fill="#C5AA50"
                                    />
                                  </svg>
                                ))}
                              </div>
                            </div>
                            <div className="self-stretch text-justify justify-start text-neutral-400 text-xs font-normal font-['Alexandria'] leading-[14px]">
                              {restaurant.address}
                            </div>
                            {restaurant.cuisine_type && (
                              <div className="self-stretch text-justify justify-start text-neutral-500 text-xs font-normal font-['Alexandria'] leading-[12px]">
                                {restaurant.cuisine_type}
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-12">
                    <p className="text-neutral-400 text-lg">
                      {currentQuery ? 
                        'Nenhum restaurante encontrado. Tente uma busca diferente.' :
                        'Faça uma busca para ver os restaurantes.'
                      }
                    </p>
                  </div>
                )}
              </div>
              
              {/* Botão Ver Completo */}
              {displayRestaurants.length > 0 && (
                <div className="w-[440px] p-2 inline-flex justify-center items-center gap-2">
                  <Link 
                    to="/complete-list"
                    className="text-justify justify-start text-white text-sm font-normal font-['Alexandria'] underline leading-[18px] hover:text-neutral-400 transition-colors"
                  >
                    Ver Completo
                  </Link>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* SearchBar Flutuante - Responsivo */}
      <div className="fixed bottom-8 lg:bottom-8 left-1/2 transform -translate-x-1/2 z-50">
        <SearchBar 
          onSearch={async (query) => {
            console.log('Nova pesquisa:', query)
            if (query.trim()) {
              await searchRestaurants(query)
            }
          }}
          placeholder="Pesquisar"
          loading={loading}
          className="w-[240px] lg:w-[200px] transition-all duration-300 ease-in-out"
          style={{ backgroundColor: '#181818' }}
        />
      </div>

      {/* Error message */}
      {error && (
        <div className="absolute left-5 top-80 lg:left-[100px] lg:bottom-32 bg-red-500/10 border border-red-500/20 rounded-lg p-4 text-red-400">
          <p className="font-medium">Erro na busca</p>
          <p className="text-sm">{error}</p>
        </div>
      )}
    </div>
  )
}

export default SearchResults