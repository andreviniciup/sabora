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
    
    # Palavras-chave relacionadas a restaurantes e comida
    FOOD_KEYWORDS = {
        # Tipos de culinária
        'japonesa', 'japonês', 'italiana', 'italiano', 'chinesa', 'chinês',
        'brasileira', 'brasileiro', 'mexicana', 'mexicano', 'indiana', 'indiano',
        'árabe', 'árabe', 'mediterrânea', 'mediterrâneo', 'francesa', 'francês',
        'portuguesa', 'português', 'peruana', 'peruano', 'nordestina', 'nordestino',
        
        # Pratos específicos
        'pizza', 'sushi', 'hambúrguer', 'hamburger', 'lasanha', 'macarrão',
        'macarronada', 'feijoada', 'churrasco', 'churrascaria', 'temaki',
        'sashimi', 'yakisoba', 'pad thai', 'curry', 'kebab', 'shawarma',
        'paella', 'risoto', 'strogonoff', 'moqueca', 'acaraje', 'vatapa',
        
        # Tipos de estabelecimento
        'restaurante', 'lanchonete', 'pizzaria', 'churrascaria', 'sushi bar',
        'café', 'cafe', 'bar', 'pub', 'padaria', 'confeitaria', 'doceria',
        'sorveteria', 'fast food', 'delivery', 'self service', 'buffet',
        
        # Características
        'vegetariano', 'vegano', 'vegetariana', 'vegana', 'saudável',
        'orgânico', 'organico', 'natural', 'gourmet', 'tradicional',
        'contemporâneo', 'contemporaneo', 'fusion', 'caseiro', 'artesanal',
        
        # Palavras de busca
        'comida', 'almoço', 'almoco', 'jantar', 'café da manhã', 'cafe da manha',
        'lanche', 'sobremesa', 'doce', 'salgado', 'bebida', 'refeição', 'refeicao',
        'prato', 'menu', 'cardápio', 'cardapio', 'especialidade', 'chef',
        
        # Localização
        'próximo', 'proximo', 'perto', 'perto de', 'ao lado', 'na rua',
        'no bairro', 'no centro', 'na praça', 'na praca', 'no shopping',
        'no mall', 'no centro comercial', 'na avenida', 'na rua',
        
        # Qualificadores
        'bom', 'boa', 'melhor', 'ótimo', 'otimo', 'excelente', 'delicioso',
        'saboroso', 'famoso', 'popular', 'recomendado', 'indicado',
        'barato', 'econômico', 'economico', 'caro', 'luxuoso', 'elegante'
    }

    # Palavras que NÃO fazem sentido para busca de restaurantes
    INVALID_KEYWORDS = {
        # Palavras técnicas/informáticas
        'javascript', 'python', 'html', 'css', 'react', 'node', 'api',
        'database', 'server', 'client', 'frontend', 'backend', 'code',
        'programming', 'software', 'hardware', 'computer', 'laptop',
        'mysql', 'postgresql', 'mongodb', 'redis', 'docker', 'kubernetes',
        
        # Palavras não relacionadas a comida
        'carro', 'moto', 'bicicleta', 'avião', 'aviao', 'trem', 'ônibus',
        'onibus', 'hotel', 'pousada', 'cinema', 'teatro', 'museu',
        'escola', 'universidade', 'hospital', 'farmácia', 'farmacia',
        'loja', 'supermercado', 'shopping', 'mall', 'banco', 'correio',
        'posto de gasolina', 'oficina', 'consultório', 'consultorio',
        
        # Palavras abstratas
        'amor', 'felicidade', 'tristeza', 'alegria', 'esperança', 'esperanca',
        'liberdade', 'justiça', 'justica', 'paz', 'guerra', 'política',
        'politica', 'economia', 'cultura', 'arte', 'música', 'musica',
        
        # Palavras muito genéricas
        'coisa', 'objeto', 'item', 'produto', 'serviço', 'servico',
        'informação', 'informacao', 'dado', 'arquivo', 'documento',
        'pessoa', 'gente', 'homem', 'mulher', 'criança', 'crianca',
        
        # Palavras de teste/genéricas
        'oi', 'olá', 'ola', 'teste', 'test', 'hello', 'hi', 'hey',
        'ok', 'sim', 'não', 'nao', 'yes', 'no', 'talvez', 'quem sabe',
        'qualquer', 'qualquer coisa', 'algo', 'nada', 'tudo', 'nenhum',
        'algum', 'alguma', 'cada', 'todo', 'toda', 'varios', 'vários',
        'muitos', 'muitas', 'poucos', 'poucas', 'alguns', 'algumas'
    }

    # Padrões que indicam busca válida
    VALID_PATTERNS = [
        # Padrões de culinária
        re.compile(r'(restaurante|comida|lanche|jantar|almoço|almoco)\s+(japonês|japonesa|italiano|italiana|chinesa|chines|brasileira|brasileiro)', re.IGNORECASE),
        re.compile(r'(pizza|sushi|hambúrguer|hamburger|lasanha|macarrão|macarronada|feijoada)', re.IGNORECASE),
        re.compile(r'(vegetariano|vegano|vegetariana|vegana|saudável|saudavel)', re.IGNORECASE),
        
        # Padrões de localização
        re.compile(r'(próximo|proximo|perto)\s+(de|do|da|dos|das)', re.IGNORECASE),
        re.compile(r'(no|na|em)\s+(centro|bairro|shopping|mall|praça|praca)', re.IGNORECASE),
        
        # Padrões de qualidade
        re.compile(r'(bom|boa|melhor|ótimo|otimo|excelente)\s+(restaurante|comida|lanche)', re.IGNORECASE),
        re.compile(r'(recomendado|indicado|famoso|popular)', re.IGNORECASE),
        
        # Padrões de preço
        re.compile(r'(barato|econômico|economico|caro|luxuoso)', re.IGNORECASE)
    ]

    # Padrões que indicam busca inválida
    INVALID_PATTERNS = [
        re.compile(r'\b(javascript|python|html|css|react|node|api|database|server)\b', re.IGNORECASE),
        re.compile(r'\b(carro|moto|avião|hotel|cinema|escola|hospital|banco)\b', re.IGNORECASE),
        re.compile(r'\b(amor|felicidade|tristeza|paz|guerra|política)\b', re.IGNORECASE),
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
            errors.append('Busca muito curta')
        elif len(sanitized_query) > 100:
            errors.append('Busca muito longa')

        # Verificar caracteres especiais excessivos
        special_chars = len(re.findall(r'[^a-z0-9\sàáâãäåçèéêëìíîïñòóôõöùúûüýÿ]', sanitized_query.lower()))
        if special_chars > len(sanitized_query) * 0.3:
            errors.append('Muitos caracteres especiais')

        # Verificar palavras inválidas
        query_lower = sanitized_query.lower()
        invalid_words = [word for word in self.INVALID_KEYWORDS if word in query_lower]
        
        if invalid_words:
            errors.append(f'"{invalid_words[0]}" não é relacionado a restaurantes')
            # Se encontrou palavras inválidas, não precisa verificar mais
            return SearchValidationResult(
                is_valid=False,
                errors=errors,
                sanitized_query=sanitized_query
            )

        # Verificar padrões inválidos
        for pattern in self.INVALID_PATTERNS:
            if pattern.search(sanitized_query):
                errors.append('Sua busca não parece ser sobre restaurantes')
                return SearchValidationResult(
                    is_valid=False,
                    errors=errors,
                    sanitized_query=sanitized_query
                )

        # Verificar se contém palavras relacionadas a comida
        food_keywords_found = [word for word in self.FOOD_KEYWORDS if word in query_lower]
        has_food_keywords = len(food_keywords_found) > 0

        # Verificar se segue padrões válidos
        has_valid_pattern = any(pattern.search(sanitized_query) for pattern in self.VALID_PATTERNS)

        # Se não tem palavras de comida nem padrões válidos, é inválido
        if not has_food_keywords and not has_valid_pattern:
            errors.append('Sua busca não parece ser sobre restaurantes ou comida')

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
        
        # Remover caracteres especiais excessivos, mas manter acentos
        sanitized = re.sub(r'[^\w\sàáâãäåçèéêëìíîïñòóôõöùúûüýÿ]', ' ', query)
        
        # Remover espaços múltiplos
        sanitized = re.sub(r'\s+', ' ', sanitized)
        
        # Limitar comprimento
        sanitized = sanitized.strip()[:100]
        
        return sanitized



# Instância global do validador
search_validator = IntelligentSearchValidator()
