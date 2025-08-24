import { useState } from 'react'
import { restaurantAPI } from '../services/api'

const ApiTest = () => {
  const [testResult, setTestResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const testConnection = async () => {
    setLoading(true)
    try {
      const result = await restaurantAPI.testConnection()
      setTestResult(result)
    } catch (error) {
      setTestResult({
        success: false,
        error: error.message
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-4 bg-gray-100 rounded-lg">
      <h3 className="text-lg font-semibold mb-4">🔗 Teste de Conectividade da API</h3>
      
      <button
        onClick={testConnection}
        disabled={loading}
        className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
      >
        {loading ? 'Testando...' : 'Testar Conexão'}
      </button>

      {testResult && (
        <div className="mt-4">
          {testResult.success ? (
            <div className="p-4 bg-green-100 border border-green-400 rounded">
              <h4 className="font-semibold text-green-800">✅ Conexão OK</h4>
              <p className="text-green-700">URL: {testResult.apiUrl}</p>
              <details className="mt-2">
                <summary className="cursor-pointer text-green-700">Ver detalhes</summary>
                <pre className="mt-2 text-sm bg-white p-2 rounded overflow-auto">
                  {JSON.stringify(testResult, null, 2)}
                </pre>
              </details>
            </div>
          ) : (
            <div className="p-4 bg-red-100 border border-red-400 rounded">
              <h4 className="font-semibold text-red-800">❌ Falha na Conexão</h4>
              <p className="text-red-700">Erro: {testResult.error}</p>
              <p className="text-red-700">URL: {testResult.apiUrl}</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default ApiTest
