import { restaurantAPI } from './api'

// constantes das regras de negócio
export const BUSINESS_RULES = {
  // limites de entrada
  limits: {
    maxQueryLength: 500,
    minQueryLength: 1,
    maxRestaurantNameLength: 100,
    minRestaurantNameLength: 3,
    maxRadiusKm: 50.0,
    minRadiusKm: 0.1,
    maxResults: 20,
    minRating: 0.0,
    maxRating: 5.0
  },
  
  // tipos de culinária válidos
  validCuisineTypes: [
    'nordestina', 'italiana', 'japonesa', 'brasileira', 'chinesa',
    'árabe', 'portuguesa', 'peruana', 'mediterrânea', 'mexicana',
    'indiana', 'francesa', 'frutos do mar', 'vegana', 'saudável',
    'fast food', 'padaria'
  ],
  
  // faixas de preço válidas
  validPriceRanges: ['baixo', 'medio', 'alto'],
  
  // valores padrão
  defaults: {
    defaultRadius: 2.0,
    defaultMaxResults: 5,
    defaultMinRating: 0.0,
    cacheTtl: 3600
  }
}

// validador de entrada do frontend
export class FrontendValidator {
  /**
   * valida texto da consulta
   */
  static validateQueryText(text) {
    const errors = []
    
    if (!text || !text.trim()) {
      errors.push('texto da consulta é obrigatório')
    } else if (text.length < BUSINESS_RULES.limits.minQueryLength) {
      errors.push(`texto deve ter pelo menos ${BUSINESS_RULES.limits.minQueryLength} caractere`)
    } else if (text.length > BUSINESS_RULES.limits.maxQueryLength) {
      errors.push(`texto deve ter no máximo ${BUSINESS_RULES.limits.maxQueryLength} caracteres`)
    }
    
    return errors
  }
  
  /**
   * valida localização
   */
  static validateLocation(latitude, longitude) {
    const errors = []
    
    if (latitude === null || latitude === undefined) {
      errors.push('latitude é obrigatória')
    } else if (typeof latitude !== 'number' || isNaN(latitude)) {
      errors.push('latitude deve ser um número')
    } else if (latitude < -90 || latitude > 90) {
      errors.push('latitude deve estar entre -90 e 90 graus')
    }
    
    if (longitude === null || longitude === undefined) {
      errors.push('longitude é obrigatória')
    } else if (typeof longitude !== 'number' || isNaN(longitude)) {
      errors.push('longitude deve ser um número')
    } else if (longitude < -180 || longitude > 180) {
      errors.push('longitude deve estar entre -180 e 180 graus')
    }
    
    return errors
  }
  
  /**
   * valida filtros
   */
  static validateFilters(filters) {
    const errors = []
    
    if (filters.radius_km !== undefined) {
      if (typeof filters.radius_km !== 'number' || isNaN(filters.radius_km)) {
        errors.push('raio deve ser um número')
      } else if (filters.radius_km < BUSINESS_RULES.limits.minRadiusKm || 
                 filters.radius_km > BUSINESS_RULES.limits.maxRadiusKm) {
        errors.push(`raio deve estar entre ${BUSINESS_RULES.limits.minRadiusKm} e ${BUSINESS_RULES.limits.maxRadiusKm} km`)
      }
    }
    
    if (filters.min_rating !== undefined) {
      if (typeof filters.min_rating !== 'number' || isNaN(filters.min_rating)) {
        errors.push('nota mínima deve ser um número')
      } else if (filters.min_rating < BUSINESS_RULES.limits.minRating || 
                 filters.min_rating > BUSINESS_RULES.limits.maxRating) {
        errors.push(`nota mínima deve estar entre ${BUSINESS_RULES.limits.minRating} e ${BUSINESS_RULES.limits.maxRating}`)
      }
    }
    
    if (filters.cuisine_types && Array.isArray(filters.cuisine_types)) {
      for (const cuisine of filters.cuisine_types) {
        if (!BUSINESS_RULES.validCuisineTypes.includes(cuisine.toLowerCase())) {
          errors.push(`tipo de culinária inválido: ${cuisine}`)
        }
      }
    }
    
    if (filters.price_range) {
      if (!BUSINESS_RULES.validPriceRanges.includes(filters.price_range.toLowerCase())) {
        errors.push(`faixa de preço inválida: ${filters.price_range}`)
      }
    }
    
    return errors
  }
  
  /**
   * sanitiza texto da consulta
   */
  static sanitizeQueryText(text) {
    if (!text) return ''
    
    // remover caracteres especiais perigosos
    let sanitized = text.replace(/[<>"']/g, '')
    // remover múltiplos espaços
    sanitized = sanitized.replace(/\s+/g, ' ')
    // trim
    return sanitized.trim()
  }
  
  /**
   * valida dados completos da busca
   */
  static validateSearchData(data) {
    const errors = []
    
    // validar texto
    const textErrors = this.validateQueryText(data.text)
    errors.push(...textErrors)
    
    // validar localização
    const locationErrors = this.validateLocation(data.latitude, data.longitude)
    errors.push(...locationErrors)
    
    // validar filtros se existirem
    if (data.filters) {
      const filterErrors = this.validateFilters(data.filters)
      errors.push(...filterErrors)
    }
    
    return errors
  }
}

// serviço para obter regras do backend
export class BusinessRulesService {
  /**
   * obtém regras de negócio do backend
   */
  static async getBusinessRules() {
    try {
      const API_BASE_URL = import.meta.env.VITE_API_URL || 'https://sabora-backend.onrender.com'
      const response = await fetch(`${API_BASE_URL}/api/business-rules`)
      if (!response.ok) {
        throw new Error('erro ao obter regras de negócio')
      }
      const data = await response.json()
      return data.data
    } catch (error) {
      console.error('erro ao obter regras de negócio:', error)
      // retornar regras padrão em caso de erro
      return BUSINESS_RULES
    }
  }
  
  /**
   * sincroniza regras com o backend
   */
  static async syncBusinessRules() {
    try {
      const backendRules = await this.getBusinessRules()
      
      // atualizar constantes locais com dados do backend
      if (backendRules.limits) {
        Object.assign(BUSINESS_RULES.limits, backendRules.limits)
      }
      
      if (backendRules.valid_cuisine_types) {
        BUSINESS_RULES.validCuisineTypes = backendRules.valid_cuisine_types
      }
      
      if (backendRules.valid_price_ranges) {
        BUSINESS_RULES.validPriceRanges = backendRules.valid_price_ranges
      }
      
      return true
    } catch (error) {
      console.error('erro ao sincronizar regras:', error)
      return false
    }
  }
}

// utilitários para formatação
export class BusinessRulesFormatter {
  /**
   * formata faixa de preço para exibição
   */
  static formatPriceRange(priceRange) {
    const formats = {
      'baixo': 'até r$ 30',
      'medio': 'r$ 30 - r$ 80',
      'alto': 'acima de r$ 80'
    }
    return formats[priceRange] || priceRange
  }
  
  /**
   * formata distância para exibição
   */
  static formatDistance(distanceKm) {
    if (distanceKm < 1) {
      return `${Math.round(distanceKm * 1000)}m`
    } else {
      return `${distanceKm.toFixed(1)}km`
    }
  }
  
  /**
   * formata rating para exibição
   */
  static formatRating(rating) {
    return `${rating.toFixed(1)} ⭐`
  }
  
  /**
   * formata score de recomendação
   */
  static formatRecommendationScore(score) {
    if (score >= 90) return 'excelente'
    if (score >= 80) return 'muito bom'
    if (score >= 70) return 'bom'
    if (score >= 60) return 'regular'
    return 'ruim'
  }
}

// hooks para react
export const useBusinessRules = () => {
  return {
    rules: BUSINESS_RULES,
    validator: FrontendValidator,
    formatter: BusinessRulesFormatter,
    service: BusinessRulesService
  }
}

export default {
  BUSINESS_RULES,
  FrontendValidator,
  BusinessRulesService,
  BusinessRulesFormatter,
  useBusinessRules
}
