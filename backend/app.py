"""
servidor flask principal do projeto sabora
configuracao basica com cors e endpoint de health check
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os
from dotenv import load_dotenv

# carregar variaveis de ambiente do arquivo .env
load_dotenv()

# adicionar o diretorio src ao path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.nlp.parser import QueryParser
from src.nlp.synonyms import CULINARIA, PRECO, DISTANCIA, AVALIACAO
from src.processors.recommendation_engine import RecommendationEngine
from src.models.restaurant import Restaurant, restaurants_to_dicts
from src.services.cache_service import cache_service
from src.utils.validators import business_validator

# configuracao do app
app = Flask(__name__)

# configurar cors para permitir comunicacao com frontend
CORS(app, origins=[
    'http://localhost:3000', 
    'http://127.0.0.1:3000', 
    'http://localhost:5173', 
    'http://127.0.0.1:5173',
    'https://sabora.vercel.app',  # URL do seu frontend na Vercel
    'https://*.vercel.app'  # Permite qualquer subdomínio da Vercel
])

# instancias globais
query_parser = QueryParser()
recommendation_engine = RecommendationEngine()

# configurar dicionarios de sinonimos no parser
query_parser.set_cuisine_synonyms(CULINARIA)
query_parser.set_price_synonyms(PRECO)
query_parser.set_distance_synonyms(DISTANCIA)
query_parser.set_rating_synonyms(AVALIACAO)


@app.route('/')
def home():
    """
    endpoint raiz para verificar se o servidor esta funcionando
    """
    return jsonify({
        'message': 'servidor sabora funcionando',
        'version': '1.0.0',
        'status': 'online'
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """
    endpoint de health check para verificar status do servidor
    """
    return jsonify({
        'status': 'healthy',
        'message': 'servidor funcionando corretamente',
        'timestamp': '2024-01-01T00:00:00Z'
    }), 200


@app.route('/api/config', methods=['GET'])
def get_config():
    """
    endpoint para verificar configurações carregadas
    """
    return jsonify({
        'google_maps_api_key_configured': bool(os.getenv('GOOGLE_MAPS_API_KEY')),
        'redis_host': os.getenv('REDIS_HOST', 'localhost'),
        'redis_port': os.getenv('REDIS_PORT', '6379'),
        'flask_env': os.getenv('FLASK_ENV', 'development')
    }), 200


@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    """
    endpoint para obter recomendacoes baseado em texto e localizacao
    
    espera json com:
    {
        "text": string (consulta em portugues natural),
        "latitude": float,
        "longitude": float
    }
    """
    try:
        # obter dados da requisicao
        data = request.get_json()
        
        if not data:
            return jsonify({
                'error': 'dados nao fornecidos',
                'message': 'envie text, latitude e longitude no corpo da requisicao'
            }), 400
        
        # validar entrada usando regras de negócio
        validation_errors = business_validator.validate_search_query(data)
        if validation_errors:
            return jsonify({
                'error': 'dados invalidos',
                'message': 'erros de validacao encontrados',
                'validation_errors': [
                    {
                        'field': error.field,
                        'message': error.message,
                        'code': error.code
                    }
                    for error in validation_errors
                ]
            }), 400
        
        # extrair dados validados
        text = business_validator.sanitize_query_text(data.get('text', ''))
        latitude = float(data.get('latitude'))
        longitude = float(data.get('longitude'))
        
        # extrair filtros do texto usando parser
        filters = query_parser.parse_query(text)
        
        # obter recomendacoes usando engine com cache
        recommendations = recommendation_engine.get_recommendations_with_cache(
            latitude,
            longitude,
            text,
            filters,
            use_cache=True
        )
        
        # converter para dicionarios para json
        recommendations_dict = restaurants_to_dicts(recommendations)
        
        # Gerar título dinâmico
        dynamic_title = query_parser.generate_dynamic_title(text)
        
        response_data = {
            'status': 'success',
            'message': f'encontrados {len(recommendations)} restaurantes',
            'data': {
                'recommendations': recommendations_dict,
                'user_location': {
                    'latitude': latitude,
                    'longitude': longitude
                },
                'filters_extracted': filters,
                'original_query': text,
                'dynamic_title': dynamic_title
            }
        }
        
        return jsonify(response_data), 200
        
    except Exception as e:
        return jsonify({
            'error': 'erro interno do servidor',
            'message': str(e)
        }), 500


@app.route('/api/business-rules', methods=['GET'])
def get_business_rules():
    """
    endpoint para obter regras de negócio do sistema
    """
    try:
        rules = business_validator.get_business_rules_summary()
        return jsonify({
            'status': 'success',
            'data': rules
        }), 200
    except Exception as e:
        return jsonify({
            'error': 'erro ao obter regras de negócio',
            'message': str(e)
        }), 500


@app.route('/api/cache/stats', methods=['GET'])
def get_cache_stats():
    """
    endpoint para obter estatísticas do cache
    """
    try:
        stats = cache_service.get_stats()
        return jsonify({
            'status': 'success',
            'data': stats
        }), 200
    except Exception as e:
        return jsonify({
            'error': 'erro ao obter estatísticas do cache',
            'message': str(e)
        }), 500


@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """
    endpoint para limpar todo o cache
    """
    try:
        success = cache_service.clear_all()
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Cache limpo com sucesso'
            }), 200
        else:
            return jsonify({
                'error': 'erro ao limpar cache',
                'message': 'Não foi possível limpar o cache'
            }), 500
    except Exception as e:
        return jsonify({
            'error': 'erro ao limpar cache',
            'message': str(e)
        }), 500


@app.route('/api/cache/invalidate', methods=['POST'])
def invalidate_cache_by_location():
    """
    endpoint para invalidar cache por localização
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({
                'error': 'dados não fornecidos',
                'message': 'envie latitude e longitude no corpo da requisição'
            }), 400
        
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        radius_km = data.get('radius_km', 5.0)
        
        if latitude is None or longitude is None:
            return jsonify({
                'error': 'campos obrigatórios faltando',
                'message': 'latitude e longitude são obrigatórios'
            }), 400
        
        invalidated_count = cache_service.invalidate_by_location(
            float(latitude), 
            float(longitude), 
            float(radius_km)
        )
        
        return jsonify({
            'status': 'success',
            'message': f'Cache invalidado com sucesso',
            'data': {
                'invalidated_keys': invalidated_count,
                'location': {
                    'latitude': latitude,
                    'longitude': longitude,
                    'radius_km': radius_km
                }
            }
        }), 200
    except Exception as e:
        return jsonify({
            'error': 'erro ao invalidar cache',
            'message': str(e)
        }), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    )
