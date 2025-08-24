"""
servidor flask principal do projeto sabora
configuracao basica com cors e endpoint de health check
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import sys
import os

# adicionar o diretorio src ao path para imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.nlp.parser import QueryParser
from src.processors.recommendation_engine import RecommendationEngine
from src.models.restaurant import Restaurant, restaurants_to_dicts

# configuracao do app
app = Flask(__name__)

# configurar cors para permitir comunicacao com frontend
CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000', 'http://localhost:5173', 'http://127.0.0.1:5173'])

# instancias globais
query_parser = QueryParser()
recommendation_engine = RecommendationEngine()


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
        
        # validar campos obrigatorios
        text = data.get('text')
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        
        if not text or latitude is None or longitude is None:
            return jsonify({
                'error': 'campos obrigatorios faltando',
                'message': 'text, latitude e longitude sao obrigatorios'
            }), 400
        
        # validar tipos de dados
        try:
            latitude = float(latitude)
            longitude = float(longitude)
        except (ValueError, TypeError):
            return jsonify({
                'error': 'tipo de dados invalido',
                'message': 'latitude e longitude devem ser numeros'
            }), 400
        
        # validar range das coordenadas
        if not (-90 <= latitude <= 90):
            return jsonify({
                'error': 'latitude invalida',
                'message': 'latitude deve estar entre -90 e 90 graus'
            }), 400
        
        if not (-180 <= longitude <= 180):
            return jsonify({
                'error': 'longitude invalida',
                'message': 'longitude deve estar entre -180 e 180 graus'
            }), 400
        
        # passo 1: extrair filtros do texto usando parser
        filters = query_parser.parse_query(text)
        
        # passo 2: obter recomendacoes usando engine
        recommendations = recommendation_engine.get_recommendations_with_filters(
            latitude,
            longitude,
            filters.get('radius_km', 2.0),
            5,
            filters.get('min_rating', 0.0),
            filters.get('cuisine_types'),
            filters.get('price_range')
        )
        
        # passo 3: converter para dicionarios para json
        recommendations_dict = restaurants_to_dicts(recommendations)
        
        return jsonify({
            'status': 'success',
            'message': f'encontrados {len(recommendations)} restaurantes',
            'data': {
                'recommendations': recommendations_dict,
                'user_location': {
                    'latitude': latitude,
                    'longitude': longitude
                },
                'filters_extracted': filters,
                'original_query': text
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'erro interno do servidor',
            'message': str(e)
        }), 500


if __name__ == '__main__':
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
