import { Link } from 'react-router-dom'
import { useState } from 'react'
import { useRestaurants } from '../context/RestaurantContext'
import LoadingSpinner from '../components/LoadingSpinner'
import SearchBar from '../components/SearchBar'

// dados mockados removidos - agora usando apenas dados da api

const CompleteList = () => {
  const { restaurants, loading, error, searchRestaurants } = useRestaurants()
  const [searchQuery, setSearchQuery] = useState('')
  
  // usar apenas dados da api - se não houver dados, mostrar mensagem
  const displayRestaurants = restaurants || []

  // Calcular largura dinâmica baseada no texto
  const getSearchBarWidth = () => {
    const baseWidth = 280 // largura mínima
    const maxWidth = 280 // largura máxima antes de crescer verticalmente
    const charWidth = 12 // largura aproximada por caractere
    
    const calculatedWidth = baseWidth + (searchQuery.length * charWidth)
    return Math.min(calculatedWidth, maxWidth)
  }

  // Calcular altura dinâmica baseada no texto
  const getSearchBarHeight = () => {
    const baseHeight = 40 // altura base
    const maxWidth = 280 // largura máxima antes de crescer verticalmente
    const charWidth = 12 // largura aproximada por caractere
    
    const calculatedWidth = 280 + (searchQuery.length * charWidth)
    
    if (calculatedWidth > maxWidth) {
      const extraChars = Math.ceil((calculatedWidth - maxWidth) / charWidth)
      const extraLines = Math.ceil(extraChars / 50) // aproximadamente 50 caracteres por linha
      return baseHeight + (extraLines * 20) // 20px por linha extra
    }
    
    return baseHeight
  }

  return (
    <div className="relative">
      {/* Desktop Layout */}
      <div className="hidden lg:flex w-full min-h-screen px-10 bg-neutral-900 font-alexandria items-start overflow-y-auto">
        {/* Logo */}
        <div className="absolute top-6 left-6 text-stone-300 text-lg font-medium">
          sabora
        </div>

        {/* Main Container - ajustado para dar espaço ao SearchBar flutuante */}
        <div className="mx-auto px-8 py-10 pb-28 bg-neutral-700 rounded-tl-[30px] rounded-tr-[30px] flex justify-center items-start shadow-lg min-h-fit">
          <div 
            className={`${
              displayRestaurants.length >= 8 
                ? "grid grid-cols-2 gap-8 w-full max-w-5xl" // duas colunas
                : "w-[600px] flex flex-col justify-start items-center"
            }`}
          >
            {/* Header */}
            <div className={`${displayRestaurants.length >= 8 ? "col-span-2" : "w-full"} flex justify-between items-center pb-6`}>
              <div className="text-white text-2xl font-semibold">Top {Math.min(displayRestaurants.length, 15)}</div>
              <div className="text-white text-lg font-normal">Restaurantes 5 estrelas</div>
            </div>

            {/* Restaurant List */}
                            {displayRestaurants.map((restaurant, index) => (
                  <div 
                    key={restaurant.id || index} 
                    className="w-full pb-4 flex flex-col gap-3"
                  >
                    {/* Distance */}
                    <div className="w-full flex justify-end">
                      <div className="text-zinc-500 text-xs font-medium">
                        {restaurant.distance_formatted || restaurant.distance || 'distância não disponível'}
                      </div>
                    </div>

                    {/* Main Item */}
                    <div className="flex items-center gap-4">
                      <div className="text-white text-6xl font-bold">
                        {restaurant.rank || (index + 1)}.
                      </div>
                      <div className="flex flex-col gap-1">
                        <div className="text-white text-sm font-medium">
                          {restaurant.name}
                        </div>
                        {/* Stars */}
                        <div className="flex gap-1">
                          {[...Array(Math.floor(restaurant.rating || 0))].map((_, starIndex) => (
                            <img
                              key={starIndex}
                              src="/Star-vector.svg"
                              alt="star"
                              width="14"
                              height="13"
                            />
                          ))}
                        </div>
                        <div className="text-neutral-400 text-xs">
                          {restaurant.address}
                        </div>
                        {restaurant.cuisine_type && (
                          <div className="text-neutral-500 text-xs">
                            {restaurant.cuisine_type}
                          </div>
                        )}
                      </div>
                    </div>

                    {/* Divider */}
                    {index < displayRestaurants.length - 1 && (
                      <div className="w-full border-t border-zinc-600" />
                    )}
                  </div>
                ))}
          </div>
        </div>

      </div>

      {/* Mobile Layout */}
      <div 
        className="flex lg:hidden w-full min-h-screen font-alexandria"
        style={{
          paddingTop: '20px',
          paddingLeft: '20px',
          paddingRight: '20px',
          background: '#181818',
          overflow: 'hidden',
          justifyContent: 'center',
          alignItems: 'flex-start',
          gap: '10px'
        }}
      >
        <div style={{
          width: '353px',
          flexDirection: 'column',
          justifyContent: 'flex-start',
          alignItems: 'flex-start',
          gap: '20px',
          display: 'inline-flex'
        }}>
          {/* Logo */}
          <div style={{
            alignSelf: 'stretch',
            color: '#BCBCBC',
            fontSize: '16px',
            fontFamily: 'Alexandria',
            fontWeight: '500',
            lineHeight: '23px',
            wordWrap: 'break-word'
          }}>
            sabora
          </div>

          {/* Main Container - ajustado para conteúdo dinâmico */}
          <div style={{
            alignSelf: 'stretch',
            minHeight: 'fit-content',
            paddingTop: '15px',
            paddingBottom: '100px', // espaço para o SearchBar flutuante
            background: '#3D3D3D',
            borderTopLeftRadius: '20px',
            borderTopRightRadius: '20px',
            justifyContent: 'flex-start',
            alignItems: 'center',
            gap: '10px',
            display: 'inline-flex'
          }}>
            <div style={{
              width: '353px',
              flexDirection: 'column',
              justifyContent: 'flex-start',
              alignItems: 'center',
              gap: '29px',
              display: 'inline-flex'
            }}>
              <div style={{
                alignSelf: 'stretch',
                flexDirection: 'column',
                justifyContent: 'flex-start',
                alignItems: 'center',
                gap: '25px',
                display: 'flex'
              }}>
                {/* Header */}
                <div style={{
                  alignSelf: 'stretch',
                  paddingLeft: '20px',
                  paddingRight: '20px',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  display: 'inline-flex'
                }}>
                  <div style={{
                    textAlign: 'justify',
                    color: 'white',
                    fontSize: '14px',
                    fontFamily: 'Alexandria',
                    fontWeight: '400',
                    lineHeight: '18px',
                    wordWrap: 'break-word'
                  }}>
                    Top 5
                  </div>
                  <div style={{
                    textAlign: 'justify',
                    color: 'white',
                    fontSize: '14px',
                    fontFamily: 'Alexandria',
                    fontWeight: '400',
                    lineHeight: '18px',
                    wordWrap: 'break-word'
                  }}>
                    Restaurantes 5 estrelas
                  </div>
                </div>

                {/* Restaurant Cards */}
                <div style={{
                  width: '340px',
                  flexDirection: 'column',
                  justifyContent: 'flex-start',
                  alignItems: 'center',
                  gap: '10px',
                  display: 'flex'
                }}>
                  {displayRestaurants.slice(0, 5).map((restaurant, index) => (
                    <div key={restaurant.id || index}>
                      <div style={{
                        width: '313px',
                        height: '127px',
                        flexDirection: 'column',
                        justifyContent: 'flex-start',
                        alignItems: 'flex-start',
                        display: 'flex'
                      }}>
                        {/* Distance */}
                        <div style={{
                          alignSelf: 'stretch',
                          justifyContent: 'flex-end',
                          alignItems: 'center',
                          gap: '10px',
                          display: 'inline-flex'
                        }}>
                          <div style={{
                            textAlign: 'justify',
                            color: '#575757',
                            fontSize: '12px',
                            fontFamily: 'Alexandria',
                            fontWeight: '500',
                            lineHeight: '23px',
                            wordWrap: 'break-word'
                          }}>
                            {restaurant.distance_formatted || restaurant.distance || 'distância não disponível'}
                          </div>
                        </div>

                        {/* Main Item */}
                        <div style={{
                          alignSelf: 'stretch',
                          justifyContent: 'flex-start',
                          alignItems: 'center',
                          gap: '10px',
                          display: 'inline-flex'
                        }}>
                          {/* Number */}
                          <div style={{
                            textAlign: 'justify',
                            color: 'white',
                            fontSize: '60px',
                            fontFamily: 'Alexandria',
                            fontWeight: '600',
                            lineHeight: '55px',
                            wordWrap: 'break-word'
                          }}>
                            {restaurant.rank || (index + 1)}.
                          </div>

                          {/* Info */}
                          <div style={{
                            width: '223px',
                            flexDirection: 'column',
                            justifyContent: 'flex-start',
                            alignItems: 'flex-start',
                            gap: '10px',
                            display: 'inline-flex'
                          }}>
                            <div style={{
                              width: '185px',
                              flexDirection: 'column',
                              justifyContent: 'flex-start',
                              alignItems: 'flex-start',
                              gap: '5px',
                              display: 'flex'
                            }}>
                              <div style={{
                                alignSelf: 'stretch',
                                textAlign: 'justify',
                                color: 'white',
                                fontSize: '14px',
                                fontFamily: 'Alexandria',
                                fontWeight: '500',
                                lineHeight: '18px',
                                wordWrap: 'break-word'
                              }}>
                                {restaurant.name}
                              </div>
                              {/* Stars */}
                              <div style={{
                                display: 'flex',
                                gap: '2px',
                                alignItems: 'center'
                              }}>
                                {[...Array(Math.floor(restaurant.rating || 0))].map((_, starIndex) => (
                                  <img 
                                    key={starIndex}
                                    src="/Star-vector.svg" 
                                    alt="star" 
                                    width="14" 
                                    height="13"
                                    style={{ display: 'block' }}
                                  />
                                ))}
                              </div>
                            </div>
                            <div style={{
                              alignSelf: 'stretch',
                              textAlign: 'justify',
                              color: '#919191',
                              fontSize: '12px',
                              fontFamily: 'Alexandria',
                              fontWeight: '400',
                              lineHeight: '23px',
                              wordWrap: 'break-word'
                            }}>
                              {restaurant.address}
                            </div>
                            {restaurant.cuisine_type && (
                              <div style={{
                                alignSelf: 'stretch',
                                textAlign: 'justify',
                                color: '#575757',
                                fontSize: '10px',
                                fontFamily: 'Alexandria',
                                fontWeight: '400',
                                lineHeight: '18px',
                                wordWrap: 'break-word'
                              }}>
                                {restaurant.cuisine_type}
                              </div>
                            )}
                          </div>
                        </div>
                      </div>
                      {index < displayRestaurants.slice(0, 5).length - 1 && (
                        <div style={{
                          alignSelf: 'stretch',
                          height: '0px',
                          outline: '1px #575757 solid',
                          outlineOffset: '-0.50px'
                        }} />
                      )}
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* SearchBar Flutuante - Responsivo */}
      <div className="fixed bottom-8 lg:bottom-8 left-1/2 transform -translate-x-1/2 z-50">
        <SearchBar 
          onSearch={async (query) => {
            console.log('Pesquisando:', query)
            setSearchQuery(query)
            if (query.trim()) {
              await searchRestaurants(query)
            }
          }}
          placeholder="Pesquisar"
          loading={loading}
          className="transition-all duration-300 ease-in-out"
          style={{ 
            backgroundColor: '#181818',
            width: `${getSearchBarWidth()}px`,
            minHeight: `${getSearchBarHeight()}px`,
            maxWidth: '280px'
          }}
        />
      </div>

      {/* Loading state */}
      {loading && (
        <div className="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2">
          <LoadingSpinner size="lg" />
        </div>
      )}

      {/* Error state */}
      {error && (
        <div className="absolute left-5 top-5 bg-red-500/10 border border-red-500/20 rounded-lg p-4 text-red-400">
          <p className="font-medium">Erro ao carregar restaurantes</p>
          <p className="text-sm">{error}</p>
        </div>
      )}

      {/* Empty state */}
      {!loading && displayRestaurants.length === 0 && (
        <div className="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-1/2 text-center">
          <p className="text-neutral-400 text-lg">Nenhum restaurante encontrado</p>
          <p className="text-neutral-500 text-sm">Faça uma busca para ver os restaurantes</p>
        </div>
      )}
    </div>
  )
}

export default CompleteList