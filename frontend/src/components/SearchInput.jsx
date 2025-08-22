import { useState } from 'react'

const SearchInput = ({ 
  onSearch, 
  placeholder = "Pesquisar", 
  disabled = false,
  className = "",
  style = {}
}) => {
  const [query, setQuery] = useState('')

  const handleSearch = () => {
    if (!query.trim() || disabled) return
    onSearch(query)
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
  }

  return (
    <div className={`relative ${className}`} style={style}>
      {/* Retângulo da barra de busca */}
      <div 
        className="Rectangle7"
        style={{
          width: '100%',
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
        onKeyPress={handleKeyPress}
        placeholder={placeholder}
        disabled={disabled}
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
        disabled={disabled || !query.trim()}
        className="Rectangle47 absolute right-1 top-1 flex items-center justify-center"
        style={{
          width: '30px',
          height: '30px',
          background: disabled ? '#999999' : 'white',
          borderRadius: '999px',
          border: 'none',
          cursor: disabled || !query.trim() ? 'default' : 'pointer'
        }}
      >
        {disabled ? (
          <div className="animate-spin w-4 h-4 border-2 border-gray-400 border-t-transparent rounded-full" />
        ) : (
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
            <path 
              d="M21 21L16.514 16.506M19 10.5C19 15.194 15.194 19 10.5 19S2 15.194 2 10.5 5.806 2 10.5 2 19 5.806 19 10.5Z" 
              stroke="#3D3D3D" 
              strokeWidth="2"
            />
          </svg>
        )}
      </button>
    </div>
  )
}

export default SearchInput
