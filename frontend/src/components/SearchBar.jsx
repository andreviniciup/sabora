import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useRestaurants } from '../context/RestaurantContext'
import { restaurantAPI } from '../services/api'

const SearchBar = ({ 
  placeholder = "Nova busca...", 
  className = "",
  onSearch 
}) => {
  const [query, setQuery] = useState('')
  const navigate = useNavigate()
  const { setRestaurants, setLoading, setError, setCurrentQuery, clearError } = useRestaurants()

  const handleSearch = async () => {
    if (!query.trim()) return

    try {
      clearError()
      setLoading(true)
      setCurrentQuery(query)

      const result = await restaurantAPI.searchRestaurants({
        query: query.trim(),
        maxResults: 5
      })

      setRestaurants(result.restaurants || [])
      
      // Se tem callback customizado, usa ele, senão navega para resultados
      if (onSearch) {
        onSearch(query)
      } else {
        navigate('/search-results')
      }
      
    } catch (error) {
      console.error('Search error:', error)
      setError(error.message || 'Erro ao buscar restaurantes')
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
    <div className={`relative ${className}`}>
      <input 
        type="text" 
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        onKeyPress={handleKeyPress}
        placeholder={placeholder}
        className="w-full px-6 py-4 bg-figma-gray text-figma-text placeholder-figma-placeholder rounded-2xl border-2 border-figma-gray-light focus:border-figma-placeholder focus:outline-none transition-colors"
      />
      <button 
        onClick={handleSearch}
        disabled={!query.trim()}
        className="absolute right-2 top-2 search-button text-figma-text px-6 py-2 rounded-xl disabled:opacity-50 disabled:cursor-not-allowed"
      >
        Buscar
      </button>
    </div>
  )
}

export default SearchBar
