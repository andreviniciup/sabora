import React, { useState } from 'react'
import LoadingSpinner from './LoadingSpinner'

const SearchBar = ({ 
  value: externalValue, 
  onChange: externalOnChange, 
  onFocus, 
  onBlur, 
  onKeyPress, 
  onSearch, 
  placeholder = "Pesquisar", 
  loading = false,
  disabled = false,
  className = "",
  style = {},
  controlled = false // Se true, usa value/onChange externos, senão gerencia internamente
}) => {
  const [internalValue, setInternalValue] = useState('')
  const [isFocused, setIsFocused] = useState(false)
  
  // Decide se usa valor externo ou interno
  const value = controlled ? externalValue : internalValue
  const setValue = controlled ? externalOnChange : setInternalValue

  const handleChange = (e) => {
    const newValue = e.target.value
    if (controlled && externalOnChange) {
      externalOnChange(e)
    } else {
      setInternalValue(newValue)
    }
  }

  const handleSearch = () => {
    if (!value.trim() || disabled || loading) return
    if (onSearch) {
      onSearch(controlled ? value : value)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch()
    }
    if (onKeyPress) {
      onKeyPress(e)
    }
  }

  const handleFocus = (e) => {
    setIsFocused(true)
    if (onFocus) {
      onFocus(e)
    }
  }

  const handleBlur = (e) => {
    setIsFocused(false)
    if (onBlur) {
      onBlur(e)
    }
  }

  return (
    <div 
      className={`Searchinput h-10 px-1 py-[5px] rounded-[999px] inline-flex justify-between items-center ${className}`} 
      style={{
        backgroundColor: style?.backgroundColor || '#525252', // bg-neutral-700 como fallback
        ...style
      }}
    >
      {/* Container do input */}
      <div className="Frame37 px-2.5 flex justify-center items-center gap-2.5 flex-1 relative">
        <input 
          type="text" 
          value={value}
          onChange={handleChange}
          onFocus={handleFocus}
          onBlur={handleBlur}
          onKeyPress={handleKeyPress}
          placeholder=""
          disabled={disabled || loading}
          className="w-full bg-transparent text-white placeholder-gray-400 focus:outline-none font-alexandria text-sm disabled:opacity-50"
          style={{fontSize: '14px', fontFamily: 'Alexandria', fontWeight: '400', lineHeight: '23px'}}
        />
        
        {/* Texto "Pesquisar" quando vazio e não focado */}
        {!value.trim() && !isFocused && (
          <div className="Pesquisar absolute left-2.5 top-1/2 transform -translate-y-1/2 text-neutral-400 text-sm font-normal font-['Alexandria'] leading-[23px] pointer-events-none">
            {placeholder}
          </div>
        )}
      </div>
      
      {/* Botão de ação */}
      <button 
        onClick={handleSearch}
        disabled={!value.trim() || loading || disabled}
                  className={`ButtonSend w-[30px] h-[30px] p-2.5 rounded-full flex justify-center items-center disabled:opacity-50 disabled:cursor-not-allowed bg-white`}
      >
                  {loading ? (
            <LoadingSpinner size="sm" />
          ) : (
            <img
              src="/arrow-vector.svg"
              alt="arrow"
              className="ArrowVector w-3 h-3"
              style={{
                transform: isFocused ? 'rotate(-90deg)' : 'rotate(0deg)', 
                transition: 'transform 0.3s ease',
                filter: isFocused ? 'brightness(0.3)' : 'brightness(1)'
              }}
            />
          )}
      </button>
    </div>
  )
}

export default SearchBar
