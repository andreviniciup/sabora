"""
sistema de logging para debug no backend
"""

import logging
import json
import os
from datetime import datetime
from flask import request

class BackendLogger:
    def __init__(self):
        self.logger = logging.getLogger('sabora_backend')
        self.logger.setLevel(logging.INFO)
        
        # configurar formato do log
        formatter = logging.Formatter(
            '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s'
        )
        
        # handler para console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
        
        # configurar nível baseado em variável de ambiente
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        self.logger.setLevel(getattr(logging, log_level))
    
    def _format_log(self, level, message, data=None, error=None):
        """formata a mensagem de log"""
        log_data = {
            'timestamp': datetime.now().isoformat(),
            'level': level,
            'message': message
        }
        
        # adicionar informações de request apenas se estiver no contexto
        try:
            if request:
                log_data.update({
                    'request_id': getattr(request, 'id', None),
                    'endpoint': request.endpoint if request else None,
                    'method': request.method if request else None,
                    'url': request.url if request else None,
                    'user_agent': request.headers.get('User-Agent') if request else None,
                    'origin': request.headers.get('Origin') if request else None
                })
        except RuntimeError:
            # fora do contexto de request
            pass
        
        if data:
            log_data['data'] = data
        
        if error:
            log_data['error'] = {
                'message': str(error),
                'type': type(error).__name__,
                'traceback': getattr(error, '__traceback__', None)
            }
        
        return json.dumps(log_data, indent=2, default=str)
    
    def info(self, message, data=None):
        """log de informação"""
        log_message = self._format_log('INFO', message, data)
        self.logger.info(log_message)
    
    def warn(self, message, data=None):
        """log de aviso"""
        log_message = self._format_log('WARN', message, data)
        self.logger.warning(log_message)
    
    def error(self, message, error=None, data=None):
        """log de erro"""
        log_message = self._format_log('ERROR', message, data, error)
        self.logger.error(log_message)
    
    def debug(self, message, data=None):
        """log de debug"""
        log_message = self._format_log('DEBUG', message, data)
        self.logger.debug(log_message)
    
    def api_request(self, method, url, data=None):
        """log de requisição da api"""
        log_data = {
            'request_data': data
        }
        
        try:
            if request:
                log_data['headers'] = dict(request.headers)
        except RuntimeError:
            pass
            
        self.info(f'API Request: {method} {url}', log_data)
    
    def api_response(self, method, url, status_code, data=None, duration=None):
        """log de resposta da api"""
        self.info(f'API Response: {method} {url} - {status_code}', {
            'response_data': data,
            'duration_ms': duration
        })
    
    def api_error(self, method, url, error, data=None):
        """log de erro da api"""
        self.error(f'API Error: {method} {url}', error, {
            'request_data': data,
            'error_details': {
                'message': str(error),
                'type': type(error).__name__
            }
        })
    
    def cors_request(self, origin):
        """log de requisição cors"""
        self.info(f'CORS Request from: {origin}', {
            'allowed_origins': [
                'http://localhost:3000',
                'http://localhost:5173',
                'https://sabora-wine.vercel.app',
                'https://sabora-git-main-andreviniciup.vercel.app',
                'https://sabora-andreviniciup.vercel.app'
            ]
        })
    
    def cors_error(self, origin, reason):
        """log de erro cors"""
        self.error(f'CORS Error: {reason}', None, {
            'origin': origin,
            'reason': reason
        })
    
    def google_maps_api(self, operation, data=None, error=None):
        """log de operações da google maps api"""
        if error:
            self.error(f'Google Maps API Error: {operation}', error, data)
        else:
            self.info(f'Google Maps API: {operation}', data)
    
    def cache_operation(self, operation, key=None, data=None):
        """log de operações de cache"""
        self.debug(f'Cache {operation}', {
            'key': key,
            'data_size': len(str(data)) if data else 0
        })
    
    def recommendation_engine(self, operation, data=None):
        """log do motor de recomendações"""
        self.info(f'Recommendation Engine: {operation}', data)
    
    def nlp_processing(self, input_text, parsed_data):
        """log de processamento nlp"""
        self.debug('NLP Processing', {
            'input': input_text,
            'parsed': parsed_data
        })
    
    def performance(self, operation, duration_ms, data=None):
        """log de performance"""
        self.info(f'Performance: {operation} took {duration_ms}ms', data)
    
    def startup(self):
        """log de inicialização"""
        self.info('Backend starting up', {
            'environment': os.getenv('FLASK_ENV', 'development'),
            'google_maps_configured': bool(os.getenv('GOOGLE_MAPS_API_KEY')),
            'redis_configured': bool(os.getenv('REDIS_URL'))
        })

# instância global do logger
backend_logger = BackendLogger()
