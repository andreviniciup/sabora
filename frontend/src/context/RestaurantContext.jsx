import { createContext, useContext, useState } from 'react'

const RestaurantContext = createContext()

export const useRestaurants = () => {
  const context = useContext(RestaurantContext)
  if (!context) {
    throw new Error('useRestaurants must be used within a RestaurantProvider')
  }
  return context
}

export const RestaurantProvider = ({ children }) => {
  const [restaurants, setRestaurants] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [currentQuery, setCurrentQuery] = useState('')
  const [location, setLocation] = useState(null)

  const clearError = () => setError(null)
  
  const clearRestaurants = () => setRestaurants([])

  const value = {
    restaurants,
    setRestaurants,
    loading,
    setLoading,
    error,
    setError,
    clearError,
    currentQuery,
    setCurrentQuery,
    location,
    setLocation,
    clearRestaurants
  }

  return (
    <RestaurantContext.Provider value={value}>
      {children}
    </RestaurantContext.Provider>
  )
}
