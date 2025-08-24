// sistema de logging para debug no frontend
class Logger {
  constructor() {
    this.isDevelopment = import.meta.env.DEV;
    this.isProduction = import.meta.env.PROD;
    this.logLevel = import.meta.env.VITE_LOG_LEVEL || 'info';
    
    // níveis de log: debug, info, warn, error
    this.levels = {
      debug: 0,
      info: 1,
      warn: 2,
      error: 3
    };
  }

  // verifica se deve logar baseado no nível
  shouldLog(level) {
    return this.levels[level] >= this.levels[this.logLevel];
  }

  // formata a mensagem de log
  formatMessage(level, message, data = null) {
    const timestamp = new Date().toISOString();
    const prefix = `[${timestamp}] [${level.toUpperCase()}]`;
    
    let formattedMessage = `${prefix} ${message}`;
    
    if (data) {
      formattedMessage += ` | Data: ${JSON.stringify(data, null, 2)}`;
    }
    
    return formattedMessage;
  }

  // log de debug (apenas em desenvolvimento)
  debug(message, data = null) {
    if (this.isDevelopment && this.shouldLog('debug')) {
      console.log(this.formatMessage('debug', message, data));
    }
  }

  // log de informação
  info(message, data = null) {
    if (this.shouldLog('info')) {
      console.info(this.formatMessage('info', message, data));
    }
  }

  // log de aviso
  warn(message, data = null) {
    if (this.shouldLog('warn')) {
      console.warn(this.formatMessage('warn', message, data));
    }
  }

  // log de erro
  error(message, error = null, data = null) {
    if (this.shouldLog('error')) {
      const errorInfo = error ? {
        message: error.message,
        stack: error.stack,
        name: error.name
      } : null;
      
      console.error(this.formatMessage('error', message, {
        error: errorInfo,
        data: data
      }));
    }
  }

  // log de performance
  performance(operation, duration, data = null) {
    if (this.shouldLog('info')) {
      this.info(`Performance: ${operation} took ${duration}ms`, data);
    }
  }

  // log de api calls
  apiCall(method, url, requestData = null, responseData = null, duration = null) {
    const logData = {
      method,
      url,
      requestData,
      responseData,
      duration: duration ? `${duration}ms` : null
    };
    
    this.info(`API Call: ${method} ${url}`, logData);
  }

  // log de erro de api
  apiError(method, url, error, requestData = null) {
    const logData = {
      method,
      url,
      requestData,
      error: {
        message: error.message,
        status: error.response?.status,
        statusText: error.response?.statusText,
        data: error.response?.data
      }
    };
    
    this.error(`API Error: ${method} ${url}`, error, logData);
  }

  // log de estado da aplicação
  appState(component, action, state = null) {
    this.debug(`App State: ${component} - ${action}`, state);
  }

  // log de geolocalização
  geolocation(action, data = null, error = null) {
    if (error) {
      this.error(`Geolocation Error: ${action}`, error, data);
    } else {
      this.info(`Geolocation: ${action}`, data);
    }
  }

  // log de cache
  cache(action, key = null, data = null) {
    this.debug(`Cache: ${action}`, { key, data });
  }

  // log de renderização de componentes
  render(component, props = null) {
    this.debug(`Render: ${component}`, props);
  }

  // log de eventos do usuário
  userEvent(event, data = null) {
    this.info(`User Event: ${event}`, data);
  }

  // log de navegação
  navigation(from, to) {
    this.info(`Navigation: ${from} → ${to}`);
  }

  // log de erro de build/deploy
  buildError(error, context = null) {
    this.error(`Build Error: ${error.message}`, error, context);
  }

  // log de configuração
  config(config) {
    this.info('App Configuration', {
      environment: import.meta.env.MODE,
      apiUrl: import.meta.env.VITE_API_URL,
      logLevel: this.logLevel,
      isDevelopment: this.isDevelopment,
      isProduction: this.isProduction,
      ...config
    });
  }

  // log de inicialização
  init() {
    this.info('Logger initialized', {
      level: this.logLevel,
      environment: import.meta.env.MODE,
      timestamp: new Date().toISOString()
    });
  }

  // método para enviar logs para um serviço externo (opcional)
  sendToExternalService(level, message, data) {
    // implementar envio para serviço de logs (sentry, logrocket, etc.)
    if (this.isProduction) {
      // exemplo: enviar para sentry ou outro serviço
      // Sentry.captureMessage(message, level);
    }
  }
}

// instância global do logger
const logger = new Logger();

// inicializa o logger
logger.init();

export default logger;
