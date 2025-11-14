import random
from database import get_db

class AdaptiveAlgorithm:
    """Algoritmo adaptativo que ajusta la dificultad según el rendimiento del usuario"""
    
    WEAK_TOPIC_THRESHOLD = 0.70  # 70% de aciertos para considerar un tema débil
    WEAK_TOPIC_PROBABILITY = 0.70  # 70% probabilidad de elegir tema débil
    
    @staticmethod
    def get_next_problem(user_id):
        """Determina el siguiente problema para el usuario basado en su rendimiento"""
        # 1. Identificar temas débiles
        weak_topics = AdaptiveAlgorithm._get_weak_topics(user_id)
        
        # 2. Elegir tema (priorizar débiles)
        if weak_topics and random.random() < AdaptiveAlgorithm.WEAK_TOPIC_PROBABILITY:
            topic = AdaptiveAlgorithm._weighted_random_topic(weak_topics)
        else:
            topic = AdaptiveAlgorithm._get_random_topic()
        
        # 3. Determinar dificultad
        difficulty = AdaptiveAlgorithm._get_adaptive_difficulty(user_id, topic)
        
        return topic, difficulty
    
    @staticmethod
    def _get_weak_topics(user_id):
        """Identifica temas donde el usuario tiene <70% de aciertos"""
        conn = get_db()
        cursor = conn.cursor()
        
        # Obtener rendimiento por tema
        topics = cursor.execute('''
            SELECT topic, 
                   total_attempts,
                   correct_attempts,
                   CAST(correct_attempts AS FLOAT) / NULLIF(total_attempts, 0) as accuracy
            FROM user_topics
            WHERE user_id = ? AND total_attempts >= 3
        ''', (user_id,)).fetchall()
        
        weak_topics = []
        for topic_data in topics:
            accuracy = topic_data['accuracy'] or 0
            if accuracy < AdaptiveAlgorithm.WEAK_TOPIC_THRESHOLD:
                weak_topics.append({
                    'topic': topic_data['topic'],
                    'accuracy': accuracy,
                    'attempts': topic_data['total_attempts']
                })
        
        conn.close()
        return weak_topics
    
    @staticmethod
    def _weighted_random_topic(weak_topics):
        """Elige un tema débil con probabilidad ponderada por qué tan débil es"""
        if not weak_topics:
            return AdaptiveAlgorithm._get_random_topic()
        
        # Ponderar por (1 - accuracy) * attempts (más débil y más intentos = más peso)
        weights = []
        for topic_data in weak_topics:
            weight = (1 - topic_data['accuracy']) * topic_data['attempts']
            weights.append(weight)
        
        # Normalizar pesos
        total_weight = sum(weights)
        if total_weight == 0:
            return random.choice(weak_topics)['topic']
        
        weights = [w / total_weight for w in weights]
        
        # Seleccionar según pesos
        rand = random.random()
        cumulative = 0
        for i, weight in enumerate(weights):
            cumulative += weight
            if rand <= cumulative:
                return weak_topics[i]['topic']
        
        return weak_topics[0]['topic']
    
    @staticmethod
    def _get_random_topic():
        """Elige un tema aleatorio"""
        from problem_generator import ProblemGenerator
        topics = list(ProblemGenerator.TOPICS.keys())
        return random.choice(topics)
    
    @staticmethod
    def _get_adaptive_difficulty(user_id, topic):
        """Determina la dificultad adaptativa para un tema"""
        conn = get_db()
        cursor = conn.cursor()
        
        # Obtener dificultad actual y rendimiento reciente
        topic_data = cursor.execute('''
            SELECT current_difficulty, correct_attempts, total_attempts
            FROM user_topics
            WHERE user_id = ? AND topic = ?
        ''', (user_id, topic)).fetchone()
        
        if not topic_data:
            # Primer problema de este tema, empezar en dificultad 1
            difficulty = 1
        else:
            difficulty = topic_data['current_difficulty']
            
            # Obtener racha reciente (últimos 5 problemas)
            recent = cursor.execute('''
                SELECT correct FROM user_problems
                WHERE user_id = ? AND topic = ?
                ORDER BY timestamp DESC
                LIMIT 5
            ''', (user_id, topic)).fetchall()
            
            if len(recent) >= 3:
                # Verificar racha de aciertos
                recent_correct = sum(1 for r in recent[:3] if r['correct'] == 1)
                if recent_correct >= 3:
                    # Aumentar dificultad
                    difficulty = min(difficulty + 1, 10)
                elif recent_correct == 0:
                    # Disminuir dificultad
                    difficulty = max(difficulty - 1, 1)
        
        conn.close()
        return difficulty
    
    @staticmethod
    def update_user_topic_performance(user_id, topic, correct, difficulty):
        """Actualiza el rendimiento del usuario en un tema"""
        conn = get_db()
        cursor = conn.cursor()
        
        # Obtener o crear registro de tema
        topic_data = cursor.execute('''
            SELECT * FROM user_topics
            WHERE user_id = ? AND topic = ?
        ''', (user_id, topic)).fetchone()
        
        if topic_data:
            # Actualizar
            new_total = topic_data['total_attempts'] + 1
            new_correct = topic_data['correct_attempts'] + (1 if correct else 0)
            
            # Ajustar dificultad
            new_difficulty = topic_data['current_difficulty']
            if correct:
                # Si acierta 3 seguidos, subir dificultad
                recent = cursor.execute('''
                    SELECT correct FROM user_problems
                    WHERE user_id = ? AND topic = ?
                    ORDER BY timestamp DESC
                    LIMIT 2
                ''', (user_id, topic)).fetchall()
                
                if len(recent) >= 2 and all(r['correct'] == 1 for r in recent):
                    new_difficulty = min(new_difficulty + 1, 10)
            else:
                # Si falla 2 seguidos, bajar dificultad
                recent = cursor.execute('''
                    SELECT correct FROM user_problems
                    WHERE user_id = ? AND topic = ?
                    ORDER BY timestamp DESC
                    LIMIT 1
                ''', (user_id, topic)).fetchall()
                
                if len(recent) >= 1 and recent[0]['correct'] == 0:
                    new_difficulty = max(new_difficulty - 1, 1)
            
            cursor.execute('''
                UPDATE user_topics
                SET total_attempts = ?,
                    correct_attempts = ?,
                    current_difficulty = ?,
                    last_practiced = CURRENT_TIMESTAMP
                WHERE user_id = ? AND topic = ?
            ''', (new_total, new_correct, new_difficulty, user_id, topic))
        else:
            # Crear nuevo registro
            cursor.execute('''
                INSERT INTO user_topics (user_id, topic, total_attempts, correct_attempts, current_difficulty, last_practiced)
                VALUES (?, ?, 1, ?, ?, CURRENT_TIMESTAMP)
            ''', (user_id, topic, 1 if correct else 0, difficulty))
        
        conn.commit()
        conn.close()
    
    @staticmethod
    def get_user_weak_areas(user_id):
        """Obtiene las áreas débiles del usuario para el dashboard"""
        conn = get_db()
        cursor = conn.cursor()
        
        topics = cursor.execute('''
            SELECT topic,
                   total_attempts,
                   correct_attempts,
                   CAST(correct_attempts AS FLOAT) / NULLIF(total_attempts, 0) as accuracy,
                   current_difficulty
            FROM user_topics
            WHERE user_id = ?
            ORDER BY accuracy ASC, total_attempts DESC
            LIMIT 5
        ''', (user_id,)).fetchall()
        
        weak_areas = []
        for topic in topics:
            accuracy = topic['accuracy'] or 0
            if accuracy < AdaptiveAlgorithm.WEAK_TOPIC_THRESHOLD or topic['total_attempts'] < 5:
                weak_areas.append({
                    'topic': topic['topic'],
                    'accuracy': round(accuracy * 100, 1),
                    'attempts': topic['total_attempts'],
                    'difficulty': topic['current_difficulty']
                })
        
        conn.close()
        return weak_areas
    
    @staticmethod
    def get_user_topic_stats(user_id):
        """Obtiene estadísticas completas por tema"""
        conn = get_db()
        cursor = conn.cursor()
        
        stats = cursor.execute('''
            SELECT topic,
                   total_attempts,
                   correct_attempts,
                   CAST(correct_attempts AS FLOAT) / NULLIF(total_attempts, 0) as accuracy,
                   current_difficulty
            FROM user_topics
            WHERE user_id = ?
            ORDER BY topic
        ''', (user_id,)).fetchall()
        
        result = []
        for stat in stats:
            result.append({
                'topic': stat['topic'],
                'total_attempts': stat['total_attempts'],
                'correct_attempts': stat['correct_attempts'],
                'accuracy': round((stat['accuracy'] or 0) * 100, 1),
                'difficulty': stat['current_difficulty']
            })
        
        conn.close()
        return result

