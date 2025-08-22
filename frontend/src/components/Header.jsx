import { Link } from 'react-router-dom'

const Header = () => {
  return (
    <div className="mb-12">
      <Link 
        to="/" 
        className="text-figma-text text-xl font-normal hover:text-figma-placeholder transition-colors brand-link"
      >
        sabora
      </Link>
    </div>
  )
}

export default Header

