from database import get_db
from adaptive_algorithm import AdaptiveAlgorithm

class MapSystem:
    """Sistema de mapa de niveles por reinos"""
    
    REALMS = {
        'aritmetica': {
            'name': 'Reino de la Aritmética',
            'icon': '🔢',
            'color': '#3b82f6',
            'description': 'Domina las operaciones básicas'
        },
        'algebra': {
            'name': 'Reino del Álgebra',
            'icon': '📐',
            'color': '#8b5cf6',
            'description': 'Resuelve ecuaciones y sistemas'
        },
        'geometria': {
            'name': 'Reino de la Geometría',
            'icon': '📏',
            'color': '#10b981',
            'description': 'Calcula áreas y volúmenes'
        },
        'trigonometria': {
            'name': 'Reino de la Trigonometría',
            'icon': '📊',
            'color': '#f59e0b',
            'description': 'Domina senos y cosenos'
        },
        'calculo': {
            'name': 'Reino del Cálculo',
            'icon': '📈',
            'color': '#ef4444',
            'description': 'Derivadas e integrales'
        }
    }
    
    LEVELS_PER_REALM = 10
    TASKS_PER_LEVEL = 5  # Tareas azules
    EXAM_PER_LEVEL = 1   # Examen rojo al final de cada nivel
    
    @staticmethod
    def get_realm_progress(user_id, realm):
        """Obtiene el progreso del usuario en un reino"""
        conn = get_db()
        cursor = conn.cursor()
        
        # Obtener estadísticas del tema
        topic_data = cursor.execute('''
            SELECT total_attempts, correct_attempts, current_difficulty
            FROM user_topics
            WHERE user_id = ? AND topic = ?
        ''', (user_id, realm)).fetchone()
        
        conn.close()
        
        if not topic_data:
            return {
                'level': 1,
                'tasks_completed': 0,
                'tasks_total': MapSystem.TASKS_PER_LEVEL,
                'exams_completed': 0,
                'exams_total': 1,
                'difficulty': 1,
                'unlocked': True  # Primer reino siempre desbloqueado
            }
        
        # Calcular nivel basado en dificultad
        difficulty = topic_data['current_difficulty']
        level = min((difficulty // 2) + 1, MapSystem.LEVELS_PER_REALM)
        
        # Calcular tareas completadas (basado en problemas resueltos)
        total_attempts = topic_data['total_attempts']
        correct_attempts = topic_data['correct_attempts']
        
        # Cada 5 problemas correctos = 1 tarea completada
        tasks_completed = min(correct_attempts // 5, MapSystem.TASKS_PER_LEVEL)
        
        # Examen completado si completó todas las tareas del nivel
        exams_completed = 1 if tasks_completed >= MapSystem.TASKS_PER_LEVEL else 0
        
        return {
            'level': level,
            'tasks_completed': tasks_completed,
            'tasks_total': MapSystem.TASKS_PER_LEVEL,
            'exams_completed': exams_completed,
            'exams_total': 1,
            'difficulty': difficulty,
            'unlocked': True
        }
    
    @staticmethod
    def get_all_realms_progress(user_id):
        """Obtiene el progreso en todos los reinos"""
        realms_progress = {}
        
        for realm_id, realm_info in MapSystem.REALMS.items():
            progress = MapSystem.get_realm_progress(user_id, realm_id)
            realms_progress[realm_id] = {
                **realm_info,
                **progress
            }
        
        return realms_progress
    
    @staticmethod
    def get_level_details(user_id, realm, level):
        """Obtiene detalles de un nivel específico"""
        progress = MapSystem.get_realm_progress(user_id, realm)
        
        # Calcular qué tareas están completadas
        tasks = []
        for i in range(MapSystem.TASKS_PER_LEVEL):
            tasks.append({
                'id': i + 1,
                'completed': i < progress['tasks_completed'],
                'type': 'task'
            })
        
        # Examen
        exam = {
            'id': 'exam',
            'completed': progress['exams_completed'] > 0,
            'type': 'exam',
            'unlocked': progress['tasks_completed'] >= MapSystem.TASKS_PER_LEVEL
        }
        
        return {
            'level': level,
            'tasks': tasks,
            'exam': exam,
            'realm': realm
        }

