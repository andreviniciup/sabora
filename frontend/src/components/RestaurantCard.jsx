const RestaurantCard = ({ restaurant, className = "" }) => {
  const renderStars = (rating) => {
    return '⭐'.repeat(rating)
  }

  const formatPrice = (priceLevel) => {
    if (!priceLevel) return 'N/A'
    return '$'.repeat(priceLevel)
  }

  return (
    <div className={`bg-figma-gray rounded-2xl p-6 mb-4 border-l-4 border-orange-500 restaurant-card ${className}`}>
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center space-x-3">
          <div className="ranking-badge text-figma-text rounded-full w-8 h-8 flex items-center justify-center text-sm font-medium">
            {restaurant.rank}
          </div>
          <div>
            <h3 className="text-figma-text text-lg font-medium">{restaurant.name}</h3>
            {restaurant.category && (
              <p className="text-figma-placeholder text-xs">{restaurant.category}</p>
            )}
          </div>
        </div>
        <div className="flex flex-col items-end">
          <div className="flex items-center space-x-1 star-rating text-sm">
            {renderStars(restaurant.rating)}
          </div>
          {restaurant.price_level && (
            <p className="text-figma-placeholder text-xs mt-1">
              {formatPrice(restaurant.price_level)}
            </p>
          )}
        </div>
      </div>
      
      <p className="text-figma-placeholder text-sm mb-2">{restaurant.address}</p>
      
      {restaurant.distance && (
        <p className="text-orange-400 text-sm">{restaurant.distance}</p>
      )}
    </div>
  )
}

export default RestaurantCard
