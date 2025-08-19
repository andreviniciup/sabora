import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Home from './pages/Home'
import SearchResults from './pages/SearchResults'
import CompleteList from './pages/CompleteList'
import { RestaurantProvider } from './context/RestaurantContext'

function App() {
  return (
    <RestaurantProvider>
      <Router>
        <div className="min-h-screen bg-figma-bg font-alexandria">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/search-results" element={<SearchResults />} />
            <Route path="/complete-list" element={<CompleteList />} />
          </Routes>
        </div>
      </Router>
    </RestaurantProvider>
  )
}

export default App