const LoadingSpinner = ({ size = "md", className = "" }) => {
  const sizes = {
    sm: "w-4 h-4",
    md: "w-8 h-8", 
    lg: "w-12 h-12"
  }

  return (
    <div className={`flex justify-center items-center ${className}`}>
      <div className={`${sizes[size]} animate-spin`}>
        <div className="w-full h-full border-3 border-figma-gray-light border-t-orange-500 rounded-full"></div>
      </div>
    </div>
  )
}

export default LoadingSpinner

