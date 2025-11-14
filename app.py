from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from database import (
    init_db, get_db, login_required, get_user, get_user_by_username,
    create_user, verify_password, hash_password
)
from problem_generator import ProblemGenerator
from adaptive_algorithm import AdaptiveAlgorithm
from gamification import GamificationSystem
from shop_system import ShopSystem
from map_system import MapSystem
import json
import os

app = Flask(__name__)
# Usar variable de entorno en producción, clave de desarrollo en local
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')

# Inicializar base de datos al iniciar
with app.app_context():
    init_db()
    GamificationSystem.initialize_daily_missions()

@app.context_processor
def inject_user_stats():
    """Inyecta estadísticas del usuario en todos los templates"""
    if 'user_id' in session:
        user = get_user(session['user_id'])
        if user:
            stats = GamificationSystem.get_user_stats(session['user_id'])
            return {'user': user, 'user_stats': stats}
    return {'user': None, 'user_stats': None}

@app.route('/')
def index():
    """Redirige al dashboard si está logueado, sino al login"""
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Please fill in all fields', 'error')
            return render_template('login.html')
        
        user = get_user_by_username(username)
        
        if user and verify_password(password, user['password_hash']):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Welcome back!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Incorrect username or password', 'error')
    
    return render_template('login.html')

@app.route('/guest')
def guest_login():
    """Login as guest user (no authentication required)"""
    # Check if guest user exists, if not create it
    guest_user = get_user_by_username('guest')
    
    if not guest_user:
        # Create guest user
        guest_id = create_user('guest', 'guest@mathgame.local', 'guest123')
        if guest_id:
            session['user_id'] = guest_id
            session['username'] = 'guest'
            session['is_guest'] = True
            flash('Logged in as Guest. Your progress will not be saved permanently.', 'info')
        else:
            flash('Error creating guest account', 'error')
            return redirect(url_for('login'))
    else:
        session['user_id'] = guest_user['id']
        session['username'] = 'guest'
        session['is_guest'] = True
        flash('Logged in as Guest. Your progress will not be saved permanently.', 'info')
    
    return redirect(url_for('dashboard'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Página de registro"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if not all([username, email, password, confirm_password]):
            flash('Por favor completa todos los campos', 'error')
            return render_template('register.html')
        
        if password != confirm_password:
            flash('Las contraseñas no coinciden', 'error')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('La contraseña debe tener al menos 6 caracteres', 'error')
            return render_template('register.html')
        
        user_id = create_user(username, email, password)
        
        if user_id:
            session['user_id'] = user_id
            session['username'] = username
            flash('¡Cuenta creada exitosamente!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('El usuario o email ya existe', 'error')
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Sesión cerrada', 'info')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal del usuario"""
    user_id = session['user_id']
    
    # Obtener estadísticas
    stats = GamificationSystem.get_user_stats(user_id)
    
    # Obtener misiones activas
    missions = GamificationSystem.get_active_missions(user_id)
    
    # Obtener áreas débiles
    weak_areas = AdaptiveAlgorithm.get_user_weak_areas(user_id)
    
    # Obtener badges recientes
    badges = GamificationSystem.get_user_badges(user_id)
    recent_badges = badges[:6] if badges else []
    
    # Get user avatar and shop categories
    user_avatar = ShopSystem.get_user_avatar(user_id)
    categories = ShopSystem.get_items_by_category()
    
    # Get realm progress for the map
    realms_progress = MapSystem.get_all_realms_progress(user_id)
    
    return render_template('index.html',
                         user_stats=stats,
                         missions=missions,
                         weak_areas=weak_areas,
                         recent_badges=recent_badges,
                         user_avatar=user_avatar,
                         categories=categories,
                         realms_progress=realms_progress)

@app.route('/problem')
@login_required
def problem():
    """Página para resolver un problema"""
    user_id = session['user_id']
    
    # Obtener tema específico si se proporciona
    topic = request.args.get('topic')
    
    if topic:
        # Usar el tema especificado
        difficulty = AdaptiveAlgorithm._get_adaptive_difficulty(user_id, topic)
    else:
        # Usar algoritmo adaptativo
        topic, difficulty = AdaptiveAlgorithm.get_next_problem(user_id)
    
    # Generar problema
    problem_data = ProblemGenerator.generate(topic, difficulty)
    
    return render_template('problem.html', problem=problem_data)

@app.route('/problem/submit', methods=['POST'])
@login_required
def submit_problem():
    """Procesa la respuesta del problema"""
    user_id = session['user_id']
    data = request.get_json()
    
    correct = data.get('correct', False)
    time_taken = data.get('time_taken', 0)
    used_hint = data.get('used_hint', False)
    difficulty = data.get('difficulty', 1)
    topic = data.get('topic', 'aritmetica')
    
    # Procesar resultado y actualizar sistema
    result = GamificationSystem.process_problem_result(
        user_id, correct, difficulty, topic, time_taken, used_hint
    )
    
    # Actualizar rendimiento del tema
    AdaptiveAlgorithm.update_user_topic_performance(
        user_id, topic, correct, difficulty
    )
    
    return jsonify(result)

@app.route('/progress')
@login_required
def progress():
    """Página de progreso del usuario"""
    user_id = session['user_id']
    
    stats = GamificationSystem.get_user_stats(user_id)
    topic_stats = AdaptiveAlgorithm.get_user_topic_stats(user_id)
    
    return render_template('progress.html',
                         user_stats=stats,
                         topic_stats=topic_stats)

@app.route('/achievements')
@login_required
def achievements():
    """Página de logros"""
    user_id = session['user_id']
    
    badges = GamificationSystem.get_user_badges(user_id)
    
    return render_template('achievements.html', badges=badges)

@app.route('/shop')
@login_required
def shop():
    """Shop page"""
    user_id = session['user_id']
    
    stats = GamificationSystem.get_user_stats(user_id)
    items = ShopSystem.get_available_items(user_id)
    categories = ShopSystem.get_items_by_category()
    user_avatar = ShopSystem.get_user_avatar(user_id)
    
    return render_template('shop.html', 
                         user_stats=stats, 
                         items=items,
                         categories=categories,
                         user_avatar=user_avatar)

@app.route('/shop/purchase', methods=['POST'])
@login_required
def purchase_item():
    """Purchase an item from the shop"""
    user_id = session['user_id']
    data = request.get_json()
    item_id = data.get('item_id')
    
    result = ShopSystem.purchase_item(user_id, item_id)
    return jsonify(result)

@app.route('/shop/avatar/update', methods=['POST'])
@login_required
def update_avatar():
    """Update user avatar"""
    user_id = session['user_id']
    data = request.get_json()
    
    result = ShopSystem.update_user_avatar(
        user_id,
        face=data.get('face'),
        hair=data.get('hair'),
        clothes=data.get('clothes'),
        accessory=data.get('accessory')
    )
    return jsonify(result)

@app.route('/leaderboard')
@login_required
def leaderboard():
    """Página de clasificación"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Ranking global
    global_leaderboard = cursor.execute('''
        SELECT u.id as user_id, u.username, u.level, l.total_xp
        FROM users u
        INNER JOIN leaderboard l ON u.id = l.user_id
        ORDER BY l.total_xp DESC
        LIMIT 50
    ''').fetchall()
    
    # Ranking semanal
    weekly_leaderboard = cursor.execute('''
        SELECT u.id as user_id, u.username, u.level, l.weekly_xp
        FROM users u
        INNER JOIN leaderboard l ON u.id = l.user_id
        ORDER BY l.weekly_xp DESC
        LIMIT 50
    ''').fetchall()
    
    conn.close()
    
    return render_template('leaderboard.html',
                         global_leaderboard=[dict(row) for row in global_leaderboard],
                         weekly_leaderboard=[dict(row) for row in weekly_leaderboard])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
