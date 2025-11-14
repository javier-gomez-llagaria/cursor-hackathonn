import sqlite3
import hashlib
from datetime import datetime
from functools import wraps
from flask import session, redirect, url_for

DATABASE = 'database.db'

def get_db():
    """Obtiene conexión a la base de datos"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Inicializa la base de datos con todas las tablas"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            level INTEGER DEFAULT 1,
            xp INTEGER DEFAULT 0,
            coins INTEGER DEFAULT 0,
            streak INTEGER DEFAULT 0,
            last_streak_date TEXT,
            avatar_data TEXT DEFAULT '{}',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de problemas (generados dinámicamente, pero guardamos algunos ejemplos)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            topic TEXT NOT NULL,
            subtopic TEXT NOT NULL,
            difficulty INTEGER NOT NULL,
            problem_text TEXT NOT NULL,
            solution TEXT NOT NULL,
            options TEXT,
            explanation TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tabla de intentos de problemas por usuario
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_problems (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            problem_id INTEGER,
            topic TEXT NOT NULL,
            subtopic TEXT NOT NULL,
            difficulty INTEGER NOT NULL,
            correct INTEGER DEFAULT 0,
            time_taken REAL,
            xp_earned INTEGER DEFAULT 0,
            coins_earned INTEGER DEFAULT 0,
            used_hint INTEGER DEFAULT 0,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Tabla de rendimiento por tema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_topics (
            user_id INTEGER NOT NULL,
            topic TEXT NOT NULL,
            total_attempts INTEGER DEFAULT 0,
            correct_attempts INTEGER DEFAULT 0,
            current_difficulty INTEGER DEFAULT 1,
            last_practiced TIMESTAMP,
            PRIMARY KEY (user_id, topic),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Tabla de badges
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS badges (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            description TEXT NOT NULL,
            icon TEXT NOT NULL,
            category TEXT NOT NULL,
            requirement TEXT NOT NULL
        )
    ''')
    
    # Tabla de badges obtenidos por usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_badges (
            user_id INTEGER NOT NULL,
            badge_id INTEGER NOT NULL,
            earned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            PRIMARY KEY (user_id, badge_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (badge_id) REFERENCES badges(id)
        )
    ''')
    
    # Tabla de misiones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS missions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            type TEXT NOT NULL,
            requirement TEXT NOT NULL,
            reward_xp INTEGER DEFAULT 0,
            reward_coins INTEGER DEFAULT 0,
            badge_id INTEGER,
            FOREIGN KEY (badge_id) REFERENCES badges(id)
        )
    ''')
    
    # Tabla de progreso de misiones
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS user_missions (
            user_id INTEGER NOT NULL,
            mission_id INTEGER NOT NULL,
            progress INTEGER DEFAULT 0,
            completed INTEGER DEFAULT 0,
            completed_at TIMESTAMP,
            PRIMARY KEY (user_id, mission_id),
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (mission_id) REFERENCES missions(id)
        )
    ''')
    
    # Tabla de leaderboard
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            user_id INTEGER PRIMARY KEY,
            total_xp INTEGER DEFAULT 0,
            weekly_xp INTEGER DEFAULT 0,
            rank_global INTEGER,
            rank_weekly INTEGER,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    
    # Insertar badges iniciales
    badges = [
        ('Primer Paso', 'Resuelve tu primer problema', '🎯', 'inicio', 'first_problem'),
        ('Racha de Fuego', 'Resuelve 10 problemas seguidos correctamente', '🔥', 'racha', 'streak_10'),
        ('Maestro del Álgebra', 'Resuelve 100 problemas de álgebra', '📐', 'tema', 'algebra_100'),
        ('Maestro de Geometría', 'Resuelve 100 problemas de geometría', '📏', 'tema', 'geometry_100'),
        ('Maestro de Aritmética', 'Resuelve 100 problemas de aritmética', '🔢', 'tema', 'arithmetic_100'),
        ('Perfeccionista', 'Resuelve 10 problemas perfectos seguidos', '⭐', 'precisión', 'perfect_10'),
        ('Velocidad', 'Resuelve un problema en menos de 30 segundos', '⚡', 'velocidad', 'speed_30'),
        ('Persistente', 'Resuelve 50 problemas en un día', '💪', 'dedicación', 'daily_50'),
        ('Racha Semanal', 'Mantén una racha de 7 días', '📅', 'racha', 'weekly_streak'),
        ('Nivel 10', 'Alcanza el nivel 10', '🏆', 'progreso', 'level_10'),
        ('Nivel 25', 'Alcanza el nivel 25', '🥇', 'progreso', 'level_25'),
        ('Nivel 50', 'Alcanza el nivel 50', '👑', 'progreso', 'level_50'),
    ]
    
    cursor.execute('SELECT COUNT(*) FROM badges')
    if cursor.fetchone()[0] == 0:
        cursor.executemany('''
            INSERT INTO badges (name, description, icon, category, requirement)
            VALUES (?, ?, ?, ?, ?)
        ''', badges)
    
    conn.commit()
    conn.close()

def hash_password(password):
    """Hashea una contraseña"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password, password_hash):
    """Verifica una contraseña"""
    return hash_password(password) == password_hash

def login_required(f):
    """Decorador para rutas que requieren autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def get_user(user_id):
    """Obtiene un usuario por ID"""
    conn = get_db()
    user = conn.execute(
        'SELECT * FROM users WHERE id = ?', (user_id,)
    ).fetchone()
    conn.close()
    return user

def get_user_by_username(username):
    """Obtiene un usuario por nombre de usuario"""
    conn = get_db()
    user = conn.execute(
        'SELECT * FROM users WHERE username = ?', (username,)
    ).fetchone()
    conn.close()
    return user

def create_user(username, email, password):
    """Crea un nuevo usuario"""
    conn = get_db()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, email, password_hash)
            VALUES (?, ?, ?)
        ''', (username, email, hash_password(password)))
        user_id = cursor.lastrowid
        
        # Inicializar leaderboard
        cursor.execute('''
            INSERT INTO leaderboard (user_id) VALUES (?)
        ''', (user_id,))
        
        conn.commit()
        return user_id
    except sqlite3.IntegrityError:
        return None
    finally:
        conn.close()

def update_user_xp(user_id, xp_gained):
    """Actualiza el XP del usuario y calcula el nivel"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Obtener XP actual
    user = cursor.execute(
        'SELECT xp, level FROM users WHERE id = ?', (user_id,)
    ).fetchone()
    
    new_xp = user['xp'] + xp_gained
    current_level = user['level']
    
    # Calcular nuevo nivel (100 XP por nivel, aumenta exponencialmente)
    new_level = current_level
    xp_for_next_level = current_level * 100
    
    while new_xp >= xp_for_next_level:
        new_level += 1
        xp_for_next_level = new_level * 100
    
    # Actualizar usuario
    cursor.execute('''
        UPDATE users SET xp = ?, level = ? WHERE id = ?
    ''', (new_xp, new_level, user_id))
    
    # Actualizar leaderboard
    cursor.execute('''
        UPDATE leaderboard SET total_xp = ?, last_updated = CURRENT_TIMESTAMP
        WHERE user_id = ?
    ''', (new_xp, user_id))
    
    conn.commit()
    conn.close()
    
    return new_level, new_xp

def update_user_coins(user_id, coins_gained):
    """Actualiza las monedas del usuario"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE users SET coins = coins + ? WHERE id = ?
    ''', (coins_gained, user_id))
    conn.commit()
    conn.close()

def update_streak(user_id):
    """Actualiza la racha diaria del usuario"""
    conn = get_db()
    cursor = conn.cursor()
    
    user = cursor.execute(
        'SELECT streak, last_streak_date FROM users WHERE id = ?', (user_id,)
    ).fetchone()
    
    today = datetime.now().date().isoformat()
    last_date = user['last_streak_date']
    
    if last_date == today:
        # Ya resolvió hoy, no hacer nada
        new_streak = user['streak']
    elif last_date is None or (datetime.now().date() - datetime.fromisoformat(last_date).date()).days > 1:
        # Perdió la racha o es el primer día
        new_streak = 1
    else:
        # Continúa la racha
        new_streak = user['streak'] + 1
    
    cursor.execute('''
        UPDATE users SET streak = ?, last_streak_date = ? WHERE id = ?
    ''', (new_streak, today, user_id))
    
    conn.commit()
    conn.close()
    return new_streak

