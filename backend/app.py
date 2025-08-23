"""
servidor flask principal do projeto sabora
configuracao basica com cors e endpoint de health check
"""

from flask import Flask, jsonify
from flask_cors import CORS

# configuracao do app
app = Flask(__name__)

# configurar cors para permitir comunicacao com frontend
CORS(app, origins=['http://localhost:3000', 'http://127.0.0.1:3000'])


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


if __name__ == '__main__':
    print("🚀 iniciando servidor sabora...")
    print("📍 endpoints disponiveis:")
    print("   GET  / - pagina inicial")
    print("   GET  /api/health - health check")
    print("🌐 servidor rodando em: http://localhost:5000")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
