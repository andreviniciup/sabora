import React, { useState, useEffect } from 'react'
import logger from '../services/logger.js'

const DebugPanel = () => {
  const [isVisible, setIsVisible] = useState(false)
  const [logs, setLogs] = useState([])
  const [apiStatus, setApiStatus] = useState('unknown')
  const [config, setConfig] = useState({})

  // capturar logs do console
  useEffect(() => {
    const originalLog = console.log
    const originalInfo = console.info
    const originalWarn = console.warn
    const originalError = console.error

    const addLog = (level, ...args) => {
      setLogs(prev => [...prev.slice(-50), {
        timestamp: new Date().toISOString(),
        level,
        message: args.map(arg => 
          typeof arg === 'object' ? JSON.stringify(arg, null, 2) : String(arg)
        ).join(' ')
      }])
    }

    console.log = (...args) => {
      originalLog(...args)
      addLog('log', ...args)
    }

    console.info = (...args) => {
      originalInfo(...args)
      addLog('info', ...args)
    }

    console.warn = (...args) => {
      originalWarn(...args)
      addLog('warn', ...args)
    }

    console.error = (...args) => {
      originalError(...args)
      addLog('error', ...args)
    }

    return () => {
      console.log = originalLog
      console.info = originalInfo
      console.warn = originalWarn
      console.error = originalError
    }
  }, [])

  // verificar status da api
  useEffect(() => {
    const checkApiStatus = async () => {
      try {
        const response = await fetch('https://sabora-backend.onrender.com/api/health')
        setApiStatus(response.ok ? 'online' : 'error')
      } catch (error) {
        setApiStatus('offline')
        logger.error('API health check failed', error)
      }
    }

    checkApiStatus()
    const interval = setInterval(checkApiStatus, 30000) // verificar a cada 30s

    return () => clearInterval(interval)
  }, [])

  // carregar configurações
  useEffect(() => {
    setConfig({
      environment: import.meta.env.MODE,
      apiUrl: import.meta.env.VITE_API_URL,
      logLevel: import.meta.env.VITE_LOG_LEVEL || 'info',
      isDevelopment: import.meta.env.DEV,
      isProduction: import.meta.env.PROD,
      userAgent: navigator.userAgent,
      timestamp: new Date().toISOString()
    })
  }, [])

  const clearLogs = () => {
    setLogs([])
  }

  const testApiConnection = async () => {
    try {
      logger.info('Testing API connection')
      const response = await fetch('https://sabora-backend.onrender.com/api/health')
      const data = await response.json()
      logger.info('API test successful', data)
    } catch (error) {
      logger.error('API test failed', error)
    }
  }

  const testCors = async () => {
    try {
      logger.info('Testing CORS')
      const response = await fetch('https://sabora-backend.onrender.com/api/recommendations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Origin': window.location.origin
        },
        body: JSON.stringify({
          text: 'teste',
          latitude: -23.5505,
          longitude: -46.6333
        })
      })
      
      if (response.ok) {
        logger.info('CORS test successful')
      } else {
        logger.warn('CORS test failed', { status: response.status })
      }
    } catch (error) {
      logger.error('CORS test failed', error)
    }
  }

  if (!isVisible) {
    return (
      <button
        onClick={() => setIsVisible(true)}
        className="fixed bottom-4 right-4 bg-red-500 text-white p-2 rounded-full shadow-lg z-50"
        title="Debug Panel"
      >
        🐛
      </button>
    )
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-4xl h-3/4 flex flex-col">
        {/* Header */}
        <div className="flex justify-between items-center p-4 border-b">
          <h2 className="text-xl font-bold">Debug Panel</h2>
          <button
            onClick={() => setIsVisible(false)}
            className="text-gray-500 hover:text-gray-700"
          >
            ✕
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 flex">
          {/* Sidebar */}
          <div className="w-64 border-r p-4 space-y-4">
            <div>
              <h3 className="font-semibold mb-2">Status</h3>
              <div className="space-y-2">
                <div className="flex items-center">
                  <span className="text-sm">API:</span>
                  <span className={`ml-2 px-2 py-1 rounded text-xs ${
                    apiStatus === 'online' ? 'bg-green-100 text-green-800' :
                    apiStatus === 'offline' ? 'bg-red-100 text-red-800' :
                    'bg-yellow-100 text-yellow-800'
                  }`}>
                    {apiStatus}
                  </span>
                </div>
                <div className="flex items-center">
                  <span className="text-sm">Environment:</span>
                  <span className="ml-2 px-2 py-1 rounded text-xs bg-blue-100 text-blue-800">
                    {config.environment}
                  </span>
                </div>
              </div>
            </div>

            <div>
              <h3 className="font-semibold mb-2">Actions</h3>
              <div className="space-y-2">
                <button
                  onClick={testApiConnection}
                  className="w-full text-left px-3 py-2 text-sm bg-blue-100 hover:bg-blue-200 rounded"
                >
                  Test API Connection
                </button>
                <button
                  onClick={testCors}
                  className="w-full text-left px-3 py-2 text-sm bg-green-100 hover:bg-green-200 rounded"
                >
                  Test CORS
                </button>
                <button
                  onClick={clearLogs}
                  className="w-full text-left px-3 py-2 text-sm bg-red-100 hover:bg-red-200 rounded"
                >
                  Clear Logs
                </button>
              </div>
            </div>

            <div>
              <h3 className="font-semibold mb-2">Configuration</h3>
              <div className="text-xs space-y-1">
                <div>API URL: {config.apiUrl || 'default'}</div>
                <div>Log Level: {config.logLevel}</div>
                <div>Dev Mode: {config.isDevelopment ? 'Yes' : 'No'}</div>
                <div>Prod Mode: {config.isProduction ? 'Yes' : 'No'}</div>
              </div>
            </div>
          </div>

          {/* Logs */}
          <div className="flex-1 flex flex-col">
            <div className="p-4 border-b">
              <h3 className="font-semibold">Logs ({logs.length})</h3>
            </div>
            <div className="flex-1 overflow-auto p-4">
              <div className="space-y-1">
                {logs.map((log, index) => (
                  <div
                    key={index}
                    className={`text-xs font-mono p-2 rounded ${
                      log.level === 'error' ? 'bg-red-50 text-red-800' :
                      log.level === 'warn' ? 'bg-yellow-50 text-yellow-800' :
                      log.level === 'info' ? 'bg-blue-50 text-blue-800' :
                      'bg-gray-50 text-gray-800'
                    }`}
                  >
                    <div className="flex justify-between">
                      <span className="text-gray-500">{log.timestamp}</span>
                      <span className="uppercase font-semibold">{log.level}</span>
                    </div>
                    <div className="mt-1 break-all">{log.message}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default DebugPanel
