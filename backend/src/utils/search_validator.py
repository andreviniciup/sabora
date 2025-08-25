"""
Validador inteligente para buscas de restaurantes
Valida se a busca faz sentido antes de processar
"""

import re
from typing import Dict, Any, List, Tuple, Optional
from dataclasses import dataclass

@dataclass
class SearchValidationResult:
    """Resultado da validação de busca"""
    is_valid: bool
    errors: List[str]
    sanitized_query: str

class IntelligentSearchValidator:
    """Validador inteligente para buscas de restaurantes"""
    
    # Palavras-chave relacionadas a restaurantes e comida (EXPANDIDO)
    FOOD_KEYWORDS = {
        # Tipos de culinária
        'japonesa', 'japonês', 'japones', 'japa', 'italiana', 'italiano', 'chinesa', 'chinês', 'chines',
        'brasileira', 'brasileiro', 'mexicana', 'mexicano', 'indiana', 'indiano',
        'árabe', 'arabe', 'mediterrânea', 'mediterranea', 'mediterrâneo', 'francesa', 'francês', 'frances',
        'portuguesa', 'português', 'portugues', 'peruana', 'peruano', 'nordestina', 'nordestino', 'regional',
        'vegana', 'vegano', 'vegetariana', 'vegetariano', 'saudável', 'saudavel', 'fit', 'light',
        
        # Pratos específicos
        'pizza', 'pizzaria', 'sushi', 'suchi', 'hambúrguer', 'hamburger', 'hamburguer', 'lasanha', 'macarrão', 'macarrao',
        'macarronada', 'massa', 'feijoada', 'churrasco', 'churrascaria', 'temaki', 'yakisoba',
        'sashimi', 'yakimeshi', 'pad thai', 'curry', 'kebab', 'shawarma', 'kibe', 'quibe', 'esfiha', 'esfirra',
        'paella', 'risoto', 'strogonoff', 'moqueca', 'acaraje', 'vatapa', 'ceviche', 'tacos', 'burrito',
        'quesadilla', 'nachos', 'fajita', 'ramen', 'lamen', 'gyoza', 'tempura', 'tenpura',
        'carne de sol', 'cuscuz', 'baiao de dois', 'sarapatel', 'tapioca', 'pastel', 'coxinha',
        'pão de açúcar', 'croissant', 'crepe', 'quiche', 'empada', 'torta', 'bolo', 'doces', 'salgados',
        
        # Estabelecimentos famosos (ADICIONADO)
        'mcdonalds', "mcdonald's", 'mc donalds', "mc donald's", 'mequi', 'burger king', 'bk', 'burguer king',
        'subway', 'kfc', 'kentucky', 'pizza hut', 'pizzahut', 'dominos', "domino's", 'starbucks', 'star bucks',
        "bob's", 'bobs', 'giraffas', 'girafas', "habib's", 'habibs', 'habib', 'spoleto',
        'china in box', 'china inbox', 'chinainbox', 'outback', 'tgi fridays', "tgi friday's", 'fridays',
        'ragazzo', 'pizza ranch', 'si señor', 'si senor', 'américa', 'america', "applebee's", 'applebees',
        'madero', 'the fifties', 'fifties', 'degree', 'z deli', 'zdeli', 'jerônimo', 'jeronimo',
        'fogo de chão', 'fogo de chao', 'espetus', 'galeto sat', 'costelão', 'costelao',
        
        # Tipos de estabelecimento
        'restaurante', 'lanchonete', 'pizzaria', 'churrascaria', 'sushi bar', 'hamburgueria',
        'café', 'cafe', 'cafeteria', 'coffee shop', 'bar', 'pub', 'boteco', 'botequim',
        'padaria', 'confeitaria', 'doceria', 'sorveteria', 'fast food', 'delivery', 'self service', 'buffet',
        'cantina', 'casa', 'cozinha', 'gastronomia', 'gastronômico', 'chef', 'rodizio', 'rodízio',
        
        # Características e qualificadores
        'vegetariano', 'vegano', 'vegetariana', 'vegana', 'saudável', 'saudavel',
        'orgânico', 'organico', 'natural', 'gourmet', 'tradicional', 'caseiro', 'artesanal',
        'contemporâneo', 'contemporaneo', 'fusion', 'regional', 'típico', 'tipico', 'autêntico', 'autentico',
        
        # Palavras de busca relacionadas à comida
        'comida', 'almoço', 'almoco', 'jantar', 'café da manhã', 'cafe da manha', 'brunch',
        'lanche', 'sobremesa', 'doce', 'salgado', 'bebida', 'refeição', 'refeicao',
        'prato', 'menu', 'cardápio', 'cardapio', 'especialidade', 'receita', 'tempero',
        'sabor', 'saboroso', 'delicioso', 'gostoso', 'apetitoso',
        
        # Palavras de localização (relacionadas a estabelecimentos)
        'próximo', 'proximo', 'perto', 'perto de', 'ao lado', 'vizinho', 'aqui perto',
        'na rua', 'no bairro', 'no centro', 'na praça', 'na praca', 'no shopping',
        'no mall', 'no centro comercial', 'na avenida', 'nas redondezas',
        
        # Qualificadores de qualidade e preço
        'bom', 'boa', 'melhor', 'melhores', 'ótimo', 'otimo', 'excelente', 'delicioso', 'saboroso',
        'famoso', 'popular', 'recomendado', 'indicado', 'conhecido', 'tradicional', 'clássico', 'classico',
        'barato', 'baratos', 'econômico', 'economico', 'caro', 'caros', 'luxuoso', 'elegante', 'sofisticado',
        'premium', 'fino', 'requintado', 'chique', 'em conta', 'acessível', 'acessivel',
        
        # Tipos de serviço
        'delivery', 'entrega', 'balcão', 'balcao', 'drive thru', 'para viagem', 'no local',
        'mesa', 'reserva', 'buffet', 'self service', 'à la carte', 'executivo', 'comercial',
        'rodízio', 'rodizio', 'livre', 'aberto', 'funcionando', 'horário', 'horario',
        
        # Ingredientes e características especiais
        'fresco', 'caseiro', 'artesanal', 'temperado', 'apimentado', 'doce', 'salgado', 'azedo',
        'sem lactose', 'sem glúten', 'sem glutem', 'diet', 'light', 'zero açúcar', 'zero acucar',
        'integral', 'orgânico', 'organico', 'funcional', 'proteína', 'proteina', 'fibra',
        
        # Bebidas
        'cerveja', 'chopp', 'vinho', 'caipirinha', 'drinks', 'suco', 'refrigerante', 'água', 'agua',
        'café', 'cafe', 'cappuccino', 'espresso', 'chá', 'cha', 'mate', 'açaí', 'acai', 'vitamina'
    }

    # Palavras que NÃO fazem sentido para busca de restaurantes (EXPANDIDO)
    INVALID_KEYWORDS = {
        # Números aleatórios ou códigos sem contexto
        '1344', '123', '456', '789', '000', '999', '111', '222', '333', '444', '555', '666', '777', '888',
        
        # Palavras técnicas/informáticas
        'javascript', 'python', 'html', 'css', 'react', 'node', 'api', 'json', 'xml', 'sql',
        'database', 'server', 'client', 'frontend', 'backend', 'code', 'coding', 'script',
        'programming', 'software', 'hardware', 'computer', 'laptop', 'desktop', 'mobile',
        'mysql', 'postgresql', 'mongodb', 'redis', 'docker', 'kubernetes', 'linux', 'windows',
        'framework', 'library', 'function', 'variable', 'array', 'object', 'class', 'method',
        'algorithm', 'debug', 'bug', 'error', 'exception', 'syntax', 'compiler', 'interpreter',
        
        # Palavras não relacionadas a comida/estabelecimentos
        'carro', 'moto', 'bicicleta', 'avião', 'aviao', 'trem', 'ônibus', 'onibus', 'barco', 'navio',
        'hotel', 'pousada', 'motel', 'cinema', 'teatro', 'museu', 'biblioteca', 'livraria',
        'escola', 'universidade', 'faculdade', 'colégio', 'creche', 'hospital', 'clínica', 'clinica',
        'farmácia', 'farmacia', 'drogaria', 'supermercado', 'mercado', 'loja', 'shopping', 'mall',
        'banco', 'caixa eletrônico', 'correio', 'cartório', 'cartorio', 'fórum', 'forum',
        'delegacia', 'posto de gasolina', 'oficina', 'mecânica', 'mecanica', 'lava-jato',
        'consultório', 'consultorio', 'escritório', 'escritorio', 'empresa', 'firma',
        
        # Palavras abstratas/conceituais
        'amor', 'felicidade', 'tristeza', 'alegria', 'esperança', 'esperanca', 'medo', 'raiva',
        'liberdade', 'justiça', 'justica', 'paz', 'guerra', 'política', 'politica', 'religião', 'religiao',
        'economia', 'filosofia', 'psicologia', 'sociologia', 'antropologia', 'história', 'historia',
        'geografia', 'matemática', 'matematica', 'física', 'fisica', 'química', 'quimica', 'biologia',
        
        # Palavras muito genéricas sem contexto
        'coisa', 'coisas', 'objeto', 'objetos', 'item', 'itens', 'produto', 'produtos',
        'serviço', 'servico', 'serviços', 'servicos', 'informação', 'informacao', 'informações', 'informacoes',
        'dado', 'dados', 'arquivo', 'arquivos', 'documento', 'documentos', 'papel', 'papéis', 'papeis',
        'pessoa', 'pessoas', 'gente', 'homem', 'mulher', 'criança', 'crianca', 'adulto', 'idoso',
        
        # Saudações e palavras de teste
        'oi', 'olá', 'ola', 'ei', 'eai', 'e ai', 'hello', 'hi', 'hey', 'yo',
        'teste', 'test', 'testing', 'testando', 'exemplo', 'sample', 'demo',
        'ok', 'okay', 'sim', 'não', 'nao', 'yes', 'no', 'maybe', 'talvez', 'quem sabe',
        
        # Palavras genéricas demais
        'qualquer', 'qualquer coisa', 'algo', 'alguma coisa', 'nada', 'tudo', 'nenhum', 'nenhuma',
        'algum', 'alguma', 'cada', 'todo', 'toda', 'todos', 'todas', 'varios', 'vários',
        'muitos', 'muitas', 'poucos', 'poucas', 'alguns', 'algumas', 'varios tipos', 'vários tipos',
        
        # Expressões muito vagas
        'sei la', 'sei lá', 'tanto faz', 'qualquer um', 'qualquer uma', 'o que for',
        'não sei', 'nao sei', 'sei não', 'sei nao', 'vai que', 'pode ser',
        
        # Palavras de entretenimento não relacionadas
        'jogo', 'jogos', 'game', 'games', 'filme', 'filmes', 'série', 'series', 'anime', 'manga',
        'música', 'musica', 'canção', 'cancao', 'banda', 'artista', 'show', 'concerto',
        'festa', 'balada', 'clube', 'boate', 'danceteria',
        
        # Esportes
        'futebol', 'basquete', 'vôlei', 'volei', 'tênis', 'tenis', 'natação', 'natacao',
        'corrida', 'caminhada', 'academia', 'ginástica', 'ginastica', 'pilates', 'yoga',
        
        # Roupas e acessórios
        'roupa', 'roupas', 'camisa', 'calça', 'calca', 'sapato', 'sapatos', 'tênis', 'tenis',
        'bolsa', 'bolsas', 'mochila', 'carteira', 'relógio', 'relogio', 'óculos', 'oculos',
        
        # Eletrônicos
        'celular', 'telefone', 'smartphone', 'tablet', 'computador', 'notebook', 'tv', 'televisão', 'televisao',
        'rádio', 'radio', 'fone', 'fones', 'headphone', 'mouse', 'teclado', 'monitor',
        
        # Animais
        'cachorro', 'gato', 'pássaro', 'passaro', 'peixe', 'hamster', 'coelho', 'tartaruga',
        'cavalo', 'vaca', 'porco', 'galinha', 'pato', 'carneiro', 'cabra'
    }

    # Padrões que indicam busca válida (MELHORADO)
    VALID_PATTERNS = [
        # Padrões de culinária básicos
        re.compile(r'(restaurante|comida|lanche|jantar|almoço|almoco|café da manhã|cafe da manha|brunch)\s+(japonês|japonesa|italiano|italiana|chinesa|chines|chinês|brasileira|brasileiro|mexicana|mexicano|árabe|arabe|nordestina|nordestino)', re.IGNORECASE),
        
        # Pratos específicos
        re.compile(r'\b(pizza|sushi|hambúrguer|hamburger|hamburguer|lasanha|macarrão|macarrao|feijoada|churrasco|temaki|yakisoba|ceviche|tacos|burrito|risoto|moqueca|acaraje|vatapa|coxinha|pastel)\b', re.IGNORECASE),
        
        # Estabelecimentos famosos
        re.compile(r'\b(mcdonalds|mcdonald\'s|mc\s*donalds|burger\s*king|bk|subway|kfc|pizza\s*hut|dominos|starbucks|bob\'s|bobs|giraffas|habib\'s|habibs|spoleto|outback|madero)\b', re.IGNORECASE),
        
        # Tipos de estabelecimento
        re.compile(r'\b(pizzaria|churrascaria|hamburgueria|sushi\s*bar|lanchonete|padaria|cafeteria|café|cafe|bar|boteco|doceria|sorveteria)\b', re.IGNORECASE),
        
        # Características alimentares
        re.compile(r'\b(vegetariano|vegano|vegetariana|vegana|saudável|saudavel|fit|light|gourmet|caseiro|artesanal|tradicional)\b', re.IGNORECASE),
        
        # Padrões de localização + comida
        re.compile(r'(próximo|proximo|perto|aqui perto|ao lado)\s+(de|do|da|dos|das)?\s*(restaurante|comida|pizza|lanche)', re.IGNORECASE),
        re.compile(r'(no|na|em)\s+(centro|bairro|shopping|mall|praça|praca)\s*(restaurante|comida|pizza|lanche)', re.IGNORECASE),
        
        # Padrões de qualidade + comida
        re.compile(r'(bom|boa|melhor|melhores|ótimo|otimo|excelente|delicioso|saboroso)\s+(restaurante|comida|lanche|pizza|hambúrguer|hamburger)', re.IGNORECASE),
        re.compile(r'(recomendado|indicado|famoso|popular|conhecido)\s*(restaurante|comida|lanche)', re.IGNORECASE),
        
        # Padrões de preço + comida
        re.compile(r'(barato|baratos|econômico|economico|em conta|acessível|acessivel)\s*(restaurante|comida|lanche|pizza)', re.IGNORECASE),
        re.compile(r'(caro|caros|luxuoso|elegante|sofisticado|premium|fino)\s*(restaurante|comida|lanche)', re.IGNORECASE),
        
        # Padrões de busca por tipo de refeição
        re.compile(r'(onde|quero|procuro|busco)\s+(almoçar|jantar|lanchar|tomar café|cafe da manhã)', re.IGNORECASE),
        re.compile(r'(lugar|local)\s+para\s+(comer|almoçar|jantar|lanchar)', re.IGNORECASE),
        
        # Padrões com "comida" + tipo
        re.compile(r'comida\s+(japonesa|italiana|chinesa|brasileira|mexicana|árabe|arabe|indiana|nordestina)', re.IGNORECASE),
        
        # Padrões regionais específicos
        re.compile(r'\b(regional|nordestino|nordestina|baiano|baiana|mineiro|mineira|gaúcho|gaucho|paulista|carioca)\b', re.IGNORECASE),
        
        # Delivery e entrega
        re.compile(r'\b(delivery|entrega|para casa|em casa|ifood|uber eats|rappi)\b', re.IGNORECASE)
    ]

    # Padrões que indicam busca inválida (MELHORADO)
    INVALID_PATTERNS = [
        # Tecnologia
        re.compile(r'\b(javascript|python|html|css|react|node|api|database|server|framework|library|code|programming|software|hardware)\b', re.IGNORECASE),
        
        # Transportes e lugares não relacionados a comida
        re.compile(r'\b(carro|moto|avião|hotel|cinema|escola|hospital|banco|farmácia|farmacia)\b(?!\s+(restaurante|comida|lanche))', re.IGNORECASE),
        
        # Conceitos abstratos
        re.compile(r'\b(amor|felicidade|tristeza|paz|guerra|política|politica|filosofia|psicologia)\b', re.IGNORECASE),
        
        # Apenas números sem contexto
        re.compile(r'^\d+$', re.IGNORECASE),
        
        # Apenas saudações
        re.compile(r'^(oi|olá|ola|hello|hi|hey|teste|test)$', re.IGNORECASE),
        
        # Palavras muito genéricas sozinhas
        re.compile(r'^(coisa|algo|qualquer|nada|tudo)$', re.IGNORECASE),
        
        # Esportes e entretenimento
        re.compile(r'\b(futebol|basquete|filme|jogo|música|musica|show|festa)\b(?!\s+(restaurante|comida|bar))', re.IGNORECASE),
        
        # Eletrônicos
        re.compile(r'\b(celular|computador|tv|smartphone|tablet)\b(?!\s+(restaurante|delivery))', re.IGNORECASE)
    ]

    def validate_search_query(self, query: str) -> SearchValidationResult:
        """
        Valida se a busca faz sentido para restaurantes
        
        Args:
            query: texto da busca
            
        Returns:
            resultado da validação
        """
        errors = []
        
        if not query or not query.strip():
            errors.append('Digite algo para buscar')
            return SearchValidationResult(
                is_valid=False,
                errors=errors,
                sanitized_query=''
            )

        # Sanitizar a query
        sanitized_query = self._sanitize_query(query)
        
        # Verificar comprimento
        if len(sanitized_query) < 2:
            errors.append('Busca muito curta, digite pelo menos 2 caracteres')
        elif len(sanitized_query) > 100:
            errors.append('Busca muito longa, limite de 100 caracteres')

        # Verificar se é apenas números
        if re.match(r'^\d+$', sanitized_query.strip()):
            errors.append('Digite o nome de um restaurante ou tipo de comida')
            return SearchValidationResult(
                is_valid=False,
                errors=errors,
                sanitized_query=sanitized_query
            )

        # Verificar caracteres especiais excessivos
        special_chars = len(re.findall(r'[^a-z0-9\sàáâãäåçèéêëìíîïñòóôõöùúûüýÿ]', sanitized_query.lower()))
        if special_chars > len(sanitized_query) * 0.3:
            errors.append('Muitos caracteres especiais, digite de forma mais simples')

        # Verificar padrões inválidos PRIMEIRO (mais específico)
        for pattern in self.INVALID_PATTERNS:
            if pattern.search(sanitized_query):
                errors.append('Sua busca não parece ser sobre restaurantes ou comida. Tente: "pizza", "japonês", "hamburger", etc.')
                return SearchValidationResult(
                    is_valid=False,
                    errors=errors,
                    sanitized_query=sanitized_query
                )

        # Verificar palavras inválidas
        query_lower = sanitized_query.lower()
        
        # Verificar se é apenas uma palavra inválida
        words = query_lower.split()
        if len(words) == 1 and words[0] in self.INVALID_KEYWORDS:
            errors.append('Digite o nome de um restaurante ou tipo de comida')
            return SearchValidationResult(
                is_valid=False,
                errors=errors,
                sanitized_query=sanitized_query
            )
        
        # Verificar se tem palavras inválidas no contexto
        invalid_words_found = []
        for word in words:
            if word in self.INVALID_KEYWORDS:
                invalid_words_found.append(word)
        
        # Se mais de 50% das palavras são inválidas, rejeitar
        if len(invalid_words_found) > len(words) * 0.5:
            errors.append('Sua busca não parece ser sobre restaurantes. Tente: "pizza", "sushi", "hamburger", etc.')
            return SearchValidationResult(
                is_valid=False,
                errors=errors,
                sanitized_query=sanitized_query
            )

        # Verificar se contém palavras relacionadas a comida
        food_keywords_found = []
        for word in self.FOOD_KEYWORDS:
            if word in query_lower:
                food_keywords_found.append(word)
        
        has_food_keywords = len(food_keywords_found) > 0

        # Verificar se segue padrões válidos
        has_valid_pattern = any(pattern.search(sanitized_query) for pattern in self.VALID_PATTERNS)

        # REGRA PRINCIPAL: Deve ter pelo menos uma palavra de comida OU um padrão válido
        if not has_food_keywords and not has_valid_pattern:
            errors.append('Busque por restaurantes, tipos de comida ou estabelecimentos. Ex: "pizza", "japonês", "McDonald\'s"')

        # Casos especiais: se tem palavras muito genéricas, dar dica mais específica
        generic_words = ['bom', 'boa', 'melhor', 'perto', 'próximo', 'barato', 'caro']
        if any(word in query_lower for word in generic_words) and not has_food_keywords:
            errors.append('Seja mais específico. Ex: "pizza boa", "japonês perto", "hambúrguer barato"')

        # Determinar se é válido
        is_valid = len(errors) == 0

        return SearchValidationResult(
            is_valid=is_valid,
            errors=errors,
            sanitized_query=sanitized_query
        )

    def _sanitize_query(self, query: str) -> str:
        """
        Sanitiza a query removendo caracteres problemáticos
        
        Args:
            query: query original
            
        Returns:
            query sanitizada
        """
        if not query:
            return ''
        
        # Remover caracteres especiais excessivos, mas manter acentos e apostrofes
        sanitized = re.sub(r'[^\w\s\'\-àáâãäåçèéêëìíîïñòóôõöùúûüýÿ]', ' ', query)
        
        # Remover espaços múltiplos
        sanitized = re.sub(r'\s+', ' ', sanitized)
        
        # Limitar comprimento
        sanitized = sanitized.strip()[:100]
        
        return sanitized

# Instância global do validador
search_validator = IntelligentSearchValidator()