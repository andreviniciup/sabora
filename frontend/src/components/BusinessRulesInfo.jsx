import { useState, useEffect } from 'react'
import { BusinessRulesService, BUSINESS_RULES } from '../services/businessRules'

const BusinessRulesInfo = () => {
  const [rules, setRules] = useState(BUSINESS_RULES)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    const loadRules = async () => {
      setLoading(true)
      try {
        const backendRules = await BusinessRulesService.getBusinessRules()
        setRules(backendRules)
      } catch (err) {
        setError('erro ao carregar regras do backend')
      } finally {
        setLoading(false)
      }
    }

    loadRules()
  }, [])

  if (loading) {
    return (
      <div className="p-4 bg-neutral-800 rounded-lg">
        <p className="text-neutral-400">carregando regras de negócio...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-lg">
        <p className="text-red-400">{error}</p>
      </div>
    )
  }

  return (
    <div className="p-4 bg-neutral-800 rounded-lg space-y-4">
      <h3 className="text-white font-medium text-lg">regras de negócio</h3>
      
      {/* limites */}
      <div>
        <h4 className="text-neutral-300 font-medium mb-2">limites do sistema</h4>
        <div className="grid grid-cols-2 gap-2 text-sm">
          <div className="text-neutral-400">
            <span className="font-medium">texto da consulta:</span> {rules.limits?.minQueryLength || 1} - {rules.limits?.maxQueryLength || 500} caracteres
          </div>
          <div className="text-neutral-400">
            <span className="font-medium">raio máximo:</span> {rules.limits?.maxRadiusKm || 50} km
          </div>
          <div className="text-neutral-400">
            <span className="font-medium">resultados máximos:</span> {rules.limits?.maxResults || 20}
          </div>
          <div className="text-neutral-400">
            <span className="font-medium">nota:</span> {rules.limits?.minRating || 0} - {rules.limits?.maxRating || 5}
          </div>
        </div>
      </div>

      {/* tipos de culinária */}
      <div>
        <h4 className="text-neutral-300 font-medium mb-2">tipos de culinária ({rules.valid_cuisine_types?.length || rules.validCuisineTypes?.length || 0})</h4>
        <div className="flex flex-wrap gap-1">
          {(rules.valid_cuisine_types || rules.validCuisineTypes || []).map((cuisine, index) => (
            <span 
              key={index}
              className="px-2 py-1 bg-neutral-700 text-neutral-300 text-xs rounded"
            >
              {cuisine}
            </span>
          ))}
        </div>
      </div>

      {/* faixas de preço */}
      <div>
        <h4 className="text-neutral-300 font-medium mb-2">faixas de preço</h4>
        <div className="flex flex-wrap gap-1">
          {(rules.valid_price_ranges || rules.validPriceRanges || []).map((price, index) => (
            <span 
              key={index}
              className="px-2 py-1 bg-neutral-700 text-neutral-300 text-xs rounded"
            >
              {price}
            </span>
          ))}
        </div>
      </div>

      {/* algoritmo de recomendação */}
      <div>
        <h4 className="text-neutral-300 font-medium mb-2">algoritmo de recomendação</h4>
        <div className="text-sm text-neutral-400 space-y-1">
          <p>1. busca restaurantes próximos (raio configurável)</p>
          <p>2. calcula distância do usuário</p>
          <p>3. aplica filtros (culinária, preço, nota)</p>
          <p>4. ordena por distância (menor primeiro)</p>
          <p>5. filtra por raio especificado</p>
          <p>6. reordena por nota (maior primeiro)</p>
          <p>7. calcula score de recomendação</p>
        </div>
      </div>

      {/* cache */}
      <div>
        <h4 className="text-neutral-300 font-medium mb-2">sistema de cache</h4>
        <div className="text-sm text-neutral-400">
          <p>• ttl padrão: 1 hora (3600 segundos)</p>
          <p>• chave: hash md5 dos parâmetros</p>
          <p>• fallback: cache em memória</p>
          <p>• invalidação: por localização ou manual</p>
        </div>
      </div>

      {/* nlp */}
      <div>
        <h4 className="text-neutral-300 font-medium mb-2">processamento de linguagem natural</h4>
        <div className="text-sm text-neutral-400">
          <p>• reconhece sinônimos automaticamente</p>
          <p>• extrai filtros de consultas naturais</p>
          <p>• suporta distâncias numéricas (ex: "3 km")</p>
          <p>• reconhece avaliações por nota (ex: "nota 4")</p>
          <p>• detecta status de abertura ("aberto agora")</p>
        </div>
      </div>
    </div>
  )
}

export default BusinessRulesInfo
