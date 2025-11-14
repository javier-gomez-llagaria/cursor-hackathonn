from database import get_db, update_user_xp, update_user_coins, update_streak
from datetime import datetime
import json

class GamificationSystem:
    """Sistema completo de gamificación: XP, badges, misiones, etc."""
    
    # Fórmulas de XP
    BASE_XP_CORRECT = 20
    BASE_XP_WRONG = 5
    XP_PER_DIFFICULTY = 5  # XP adicional por nivel de dificultad
    
    # Fórmulas de monedas
    COINS_CORRECT = 10
    COINS_WRONG = 2
    COINS_PER_DIFFICULTY = 2
    
    # Penalizaciones por usar ayudas
    HINT_XP_PENALTY = 0.5  # 50% menos XP
    HINT_COINS_PENALTY = 0.5
    
    @staticmethod
    def calculate_rewards(correct, difficulty, time_taken=None, used_hint=False, streak=0):
        """Calcula XP y monedas ganadas"""
        if correct:
            base_xp = GamificationSystem.BASE_XP_CORRECT
            base_coins = GamificationSystem.COINS_CORRECT
        else:
            base_xp = GamificationSystem.BASE_XP_WRONG
            base_coins = GamificationSystem.COINS_WRONG
        
        # Bonus por dificultad
        xp = base_xp + (difficulty * GamificationSystem.XP_PER_DIFFICULTY)
        coins = base_coins + (difficulty * GamificationSystem.COINS_PER_DIFFICULTY)
        
        # Bonus por racha
        if correct and streak > 0:
            streak_bonus = 1 + (streak * 0.1)  # 10% por día de racha
            xp = int(xp * streak_bonus)
            coins = int(coins * streak_bonus)
        
        # Penalización por usar pista
        if used_hint:
            xp = int(xp * GamificationSystem.HINT_XP_PENALTY)
            coins = int(coins * GamificationSystem.HINT_COINS_PENALTY)
        
        # Bonus por velocidad (si se resolvió en menos de 30 segundos)
        if correct and time_taken and time_taken < 30:
            speed_bonus = 1.2
            xp = int(xp * speed_bonus)
            coins = int(coins * speed_bonus)
        
        return max(1, xp), max(1, coins)
    
    @staticmethod
    def process_problem_result(user_id, correct, difficulty, topic, time_taken=None, used_hint=False):
        """Procesa el resultado de un problema y actualiza todo el sistema"""
        conn = get_db()
        cursor = conn.cursor()
        
        # Obtener racha actual
        user = cursor.execute('SELECT streak FROM users WHERE id = ?', (user_id,)).fetchone()
        streak = user['streak'] if user else 0
        
        # Calcular recompensas
        xp_earned, coins_earned = GamificationSystem.calculate_rewards(
            correct, difficulty, time_taken, used_hint, streak
        )
        
        # Actualizar XP y nivel
        new_level, new_xp = update_user_xp(user_id, xp_earned)
        
        # Actualizar monedas
        update_user_coins(user_id, coins_earned)
        
        # Actualizar racha si es correcto
        if correct:
            new_streak = update_streak(user_id)
        else:
            new_streak = streak
        
        # Guardar intento
        cursor.execute('''
            INSERT INTO user_problems 
            (user_id, topic, subtopic, difficulty, correct, time_taken, xp_earned, coins_earned, used_hint)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, topic, 'subtopic', difficulty, 1 if correct else 0, 
              time_taken, xp_earned, coins_earned, 1 if used_hint else 0))
        
        conn.commit()
        conn.close()
        
        # Verificar badges
        badges_earned = GamificationSystem.check_badges(user_id, correct, topic, difficulty, time_taken)
        
        # Verificar misiones
        missions_completed = GamificationSystem.check_missions(user_id, correct, topic, difficulty)
        
        return {
            'xp_earned': xp_earned,
            'coins_earned': coins_earned,
            'new_level': new_level,
            'new_xp': new_xp,
            'new_streak': new_streak,
            'leveled_up': new_level > (user['level'] if user else 0),
            'badges_earned': badges_earned,
            'missions_completed': missions_completed
        }
    
    @staticmethod
    def check_badges(user_id, correct, topic, difficulty, time_taken=None):
        """Verifica y otorga badges según el progreso"""
        conn = get_db()
        cursor = conn.cursor()
        
        badges_earned = []
        
        # Obtener estadísticas del usuario
        total_problems = cursor.execute(
            'SELECT COUNT(*) as count FROM user_problems WHERE user_id = ?', (user_id,)
        ).fetchone()['count']
        
        correct_problems = cursor.execute(
            'SELECT COUNT(*) as count FROM user_problems WHERE user_id = ? AND correct = 1', (user_id,)
        ).fetchone()['count']
        
        topic_problems = cursor.execute(
            'SELECT COUNT(*) as count FROM user_problems WHERE user_id = ? AND topic = ? AND correct = 1',
            (user_id, topic)
        ).fetchone()['count']
        
        user = cursor.execute('SELECT level, streak FROM users WHERE id = ?', (user_id,)).fetchone()
        level = user['level'] if user else 1
        streak = user['streak'] if user else 0
        
        # Verificar racha reciente (últimos 10 problemas)
        recent_streak = cursor.execute('''
            SELECT COUNT(*) as count FROM (
                SELECT correct FROM user_problems
                WHERE user_id = ? AND correct = 1
                ORDER BY timestamp DESC
                LIMIT 10
            )
        ''', (user_id,)).fetchone()['count']
        
        # Badge: Primer Paso
        if total_problems == 1 and correct:
            badge = GamificationSystem._award_badge(cursor, user_id, 'Primer Paso')
            if badge:
                badges_earned.append(badge)
        
        # Badge: Racha de Fuego
        if recent_streak >= 10:
            badge = GamificationSystem._award_badge(cursor, user_id, 'Racha de Fuego')
            if badge:
                badges_earned.append(badge)
        
        # Badge: Maestro del Álgebra
        if topic == 'algebra' and topic_problems >= 100:
            badge = GamificationSystem._award_badge(cursor, user_id, 'Maestro del Álgebra')
            if badge:
                badges_earned.append(badge)
        
        # Badge: Maestro de Geometría
        if topic == 'geometria' and topic_problems >= 100:
            badge = GamificationSystem._award_badge(cursor, user_id, 'Maestro de Geometría')
            if badge:
                badges_earned.append(badge)
        
        # Badge: Maestro de Aritmética
        if topic == 'aritmetica' and topic_problems >= 100:
            badge = GamificationSystem._award_badge(cursor, user_id, 'Maestro de Aritmética')
            if badge:
                badges_earned.append(badge)
        
        # Badge: Perfeccionista
        if recent_streak >= 10:
            badge = GamificationSystem._award_badge(cursor, user_id, 'Perfeccionista')
            if badge:
                badges_earned.append(badge)
        
        # Badge: Velocidad
        if correct and time_taken and time_taken < 30:
            badge = GamificationSystem._award_badge(cursor, user_id, 'Velocidad')
            if badge:
                badges_earned.append(badge)
        
        # Badge: Persistente (50 problemas en un día)
        today = datetime.now().date().isoformat()
        today_problems = cursor.execute('''
            SELECT COUNT(*) as count FROM user_problems
            WHERE user_id = ? AND date(timestamp) = date('now')
        ''', (user_id,)).fetchone()['count']
        
        if today_problems >= 50:
            badge = GamificationSystem._award_badge(cursor, user_id, 'Persistente')
            if badge:
                badges_earned.append(badge)
        
        # Badge: Racha Semanal
        if streak >= 7:
            badge = GamificationSystem._award_badge(cursor, user_id, 'Racha Semanal')
            if badge:
                badges_earned.append(badge)
        
        # Badges de nivel
        if level >= 10:
            badge = GamificationSystem._award_badge(cursor, user_id, 'Nivel 10')
            if badge:
                badges_earned.append(badge)
        
        if level >= 25:
            badge = GamificationSystem._award_badge(cursor, user_id, 'Nivel 25')
            if badge:
                badges_earned.append(badge)
        
        if level >= 50:
            badge = GamificationSystem._award_badge(cursor, user_id, 'Nivel 50')
            if badge:
                badges_earned.append(badge)
        
        conn.commit()
        conn.close()
        
        return badges_earned
    
    @staticmethod
    def _award_badge(cursor, user_id, badge_name):
        """Otorga un badge si no lo tiene ya"""
        # Obtener badge
        badge = cursor.execute(
            'SELECT * FROM badges WHERE name = ?', (badge_name,)
        ).fetchone()
        
        if not badge:
            return None
        
        # Verificar si ya lo tiene
        existing = cursor.execute(
            'SELECT * FROM user_badges WHERE user_id = ? AND badge_id = ?',
            (user_id, badge['id'])
        ).fetchone()
        
        if existing:
            return None
        
        # Otorgar badge
        cursor.execute('''
            INSERT INTO user_badges (user_id, badge_id)
            VALUES (?, ?)
        ''', (user_id, badge['id']))
        
        return {
            'id': badge['id'],
            'name': badge['name'],
            'description': badge['description'],
            'icon': badge['icon']
        }
    
    @staticmethod
    def check_missions(user_id, correct, topic, difficulty):
        """Verifica y completa misiones"""
        conn = get_db()
        cursor = conn.cursor()
        
        missions_completed = []
        
        # Obtener misiones activas del usuario
        missions = cursor.execute('''
            SELECT m.*, um.progress, um.completed
            FROM missions m
            LEFT JOIN user_missions um ON m.id = um.mission_id AND um.user_id = ?
            WHERE um.completed = 0 OR um.completed IS NULL
        ''', (user_id,)).fetchall()
        
        for mission in missions:
            progress = mission['progress'] or 0
            mission_id = mission['id']
            mission_type = mission['type']
            requirement = mission['requirement']
            
            # Actualizar progreso según el tipo de misión
            new_progress = progress
            
            if mission_type == 'problems_topic' and topic == requirement:
                if correct:
                    new_progress += 1
            elif mission_type == 'problems_difficulty' and difficulty >= int(requirement):
                if correct:
                    new_progress += 1
            elif mission_type == 'streak':
                user = cursor.execute('SELECT streak FROM users WHERE id = ?', (user_id,)).fetchone()
                if user:
                    new_progress = user['streak']
            
            # Actualizar o crear progreso de misión
            if new_progress > progress:
                if progress == 0:
                    # Crear nuevo registro
                    cursor.execute('''
                        INSERT INTO user_missions (user_id, mission_id, progress)
                        VALUES (?, ?, ?)
                    ''', (user_id, mission_id, new_progress))
                else:
                    # Actualizar progreso
                    cursor.execute('''
                        UPDATE user_missions SET progress = ?
                        WHERE user_id = ? AND mission_id = ?
                    ''', (new_progress, user_id, mission_id))
                
                # Verificar si se completó
                required = int(mission['requirement'].split('_')[-1]) if '_' in mission['requirement'] else int(mission['requirement'])
                if new_progress >= required:
                    # Completar misión
                    cursor.execute('''
                        UPDATE user_missions
                        SET completed = 1, completed_at = CURRENT_TIMESTAMP
                        WHERE user_id = ? AND mission_id = ?
                    ''', (user_id, mission_id))
                    
                    # Otorgar recompensas
                    if mission['reward_xp']:
                        update_user_xp(user_id, mission['reward_xp'])
                    if mission['reward_coins']:
                        update_user_coins(user_id, mission['reward_coins'])
                    
                    missions_completed.append({
                        'id': mission_id,
                        'name': mission['name'],
                        'xp': mission['reward_xp'],
                        'coins': mission['reward_coins']
                    })
        
        conn.commit()
        conn.close()
        
        return missions_completed
    
    @staticmethod
    def get_user_stats(user_id):
        """Obtiene estadísticas completas del usuario"""
        conn = get_db()
        cursor = conn.cursor()
        
        user = cursor.execute('''
            SELECT * FROM users WHERE id = ?
        ''', (user_id,)).fetchone()
        
        total_problems = cursor.execute(
            'SELECT COUNT(*) as count FROM user_problems WHERE user_id = ?', (user_id,)
        ).fetchone()['count']
        
        correct_problems = cursor.execute(
            'SELECT COUNT(*) as count FROM user_problems WHERE user_id = ? AND correct = 1', (user_id,)
        ).fetchone()['count']
        
        total_badges = cursor.execute(
            'SELECT COUNT(*) as count FROM user_badges WHERE user_id = ?', (user_id,)
        ).fetchone()['count']
        
        completed_missions = cursor.execute(
            'SELECT COUNT(*) as count FROM user_missions WHERE user_id = ? AND completed = 1', (user_id,)
        ).fetchone()['count']
        
        conn.close()
        
        accuracy = (correct_problems / total_problems * 100) if total_problems > 0 else 0
        
        return {
            'level': user['level'],
            'xp': user['xp'],
            'coins': user['coins'],
            'streak': user['streak'],
            'total_problems': total_problems,
            'correct_problems': correct_problems,
            'accuracy': round(accuracy, 1),
            'total_badges': total_badges,
            'completed_missions': completed_missions,
            'xp_for_next_level': user['level'] * 100,
            'xp_progress': user['xp'] % (user['level'] * 100)
        }
    
    @staticmethod
    def get_user_badges(user_id):
        """Obtiene todos los badges del usuario"""
        conn = get_db()
        cursor = conn.cursor()
        
        badges = cursor.execute('''
            SELECT b.*, ub.earned_at
            FROM badges b
            INNER JOIN user_badges ub ON b.id = ub.badge_id
            WHERE ub.user_id = ?
            ORDER BY ub.earned_at DESC
        ''', (user_id,)).fetchall()
        
        conn.close()
        return [dict(badge) for badge in badges]
    
    @staticmethod
    def get_active_missions(user_id):
        """Obtiene misiones activas del usuario"""
        conn = get_db()
        cursor = conn.cursor()
        
        missions = cursor.execute('''
            SELECT m.*, COALESCE(um.progress, 0) as progress, COALESCE(um.completed, 0) as completed
            FROM missions m
            LEFT JOIN user_missions um ON m.id = um.mission_id AND um.user_id = ?
            WHERE COALESCE(um.completed, 0) = 0
            ORDER BY m.id
            LIMIT 5
        ''', (user_id,)).fetchall()
        
        conn.close()
        return [dict(mission) for mission in missions]
    
    @staticmethod
    def initialize_daily_missions():
        """Initialize daily missions (should be called daily)"""
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if daily missions already exist by checking for specific mission names
        existing = cursor.execute('''
            SELECT COUNT(*) as count FROM missions
            WHERE name IN ('Resuelve 5 problemas de álgebra', 'Resuelve un problema nivel 5+', 'Mantén tu racha')
        ''').fetchone()['count']
        
        # Only create if they don't exist
        if existing >= 3:
            conn.close()
            return
        
        # Crear misiones diarias
        daily_missions = [
            ('Resuelve 5 problemas de álgebra', 'Resuelve 5 problemas de álgebra hoy', 'problems_topic', 'algebra', 50, 20, None),
            ('Resuelve un problema nivel 5+', 'Completa un problema de dificultad 5 o mayor', 'problems_difficulty', '5', 30, 15, None),
            ('Mantén tu racha', 'Resuelve al menos un problema hoy para mantener tu racha', 'streak', '1', 20, 10, None),
        ]
        
        cursor.executemany('''
            INSERT INTO missions (name, description, type, requirement, reward_xp, reward_coins, badge_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', daily_missions)
        
        conn.commit()
        conn.close()

