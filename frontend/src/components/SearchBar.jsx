import React from 'react'
import LoadingSpinner from './LoadingSpinner'

const SearchBar = ({ 
  value, 
  onChange, 
  onFocus, 
  onBlur, 
  onKeyPress, 
  onSearch, 
  placeholder = "Pesquisar", 
  loading = false,
  disabled = false 
}) => {
  return (
    <div className="relative w-full h-10 bg-figma-gray rounded-full">
      <input 
        type="text" 
        value={value}
        onChange={onChange}
        onFocus={onFocus}
        onBlur={onBlur}
        onKeyPress={onKeyPress}
        placeholder=""
        disabled={disabled || loading}
        className="w-full h-full bg-transparent text-figma-text placeholder-figma-placeholder rounded-full focus:outline-none font-alexandria text-sm disabled:opacity-50"
        style={{padding: '0 60px 0 20px', fontSize: '14px'}}
      />
      
      {/* Texto "Pesquisar" no lado esquerdo */}
      {!value.trim() && (
        <div className="absolute left-5 top-1/2 transform -translate-y-1/2 text-figma-placeholder text-xs font-normal leading-6 cursor-pointer">
          {placeholder}
        </div>
      )}
      
      {/* Botão circular no lado direito */}
      {value.trim() && (
        <button 
          onClick={onSearch}
          disabled={!value.trim() || loading || disabled}
          className="absolute right-2 top-1/2 transform -translate-y-1/2 w-6 h-6 bg-stone-400 hover:bg-stone-50 rounded-full flex items-center justify-center transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {loading ? (
            <LoadingSpinner size="sm" />
          ) : (
            <svg className="w-3 h-3 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
          )}
        </button>
      )}
    </div>
  )
}

export default SearchBar
