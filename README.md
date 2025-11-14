# MathGame - Plataforma Gamificada de Matemáticas

Una aplicación web gamificada para aprender matemáticas de forma divertida, diseñada para estudiantes de ESO y Bachillerato.

## 🎮 Características

### Sistema de Problemas
- **Generación dinámica** de problemas matemáticos
- **Múltiples temas**: Aritmética, Álgebra, Geometría, Trigonometría, Cálculo
- **Niveles de dificultad**: 1-10 adaptativos
- **Problemas únicos** con variaciones

### Sistema Adaptativo
- **Identificación de áreas débiles**: Detecta temas donde el usuario tiene dificultades
- **Ajuste automático de dificultad**: Aumenta o disminuye según el rendimiento
- **Priorización inteligente**: Se enfoca en temas que necesitan más práctica
- **Dashboard de progreso**: Visualización de áreas que requieren atención

### Gamificación Completa

#### Progreso y Niveles
- **Sistema de XP**: Gana experiencia resolviendo problemas
- **Niveles**: Sube de nivel ganando XP (100 XP por nivel)
- **Barra de progreso visual**: Sigue tu avance hacia el siguiente nivel

#### Sistema de Monedas
- **MathCoins**: Gana monedas resolviendo problemas
- **Tienda virtual**: Gasta monedas en power-ups y personalización (próximamente)

#### Logros y Badges
- **12+ badges diferentes**: Desde "Primer Paso" hasta "Nivel 50"
- **Badges temáticos**: Por cada área matemática
- **Badges de racha**: Por mantener días consecutivos
- **Badges de velocidad**: Por resolver problemas rápidamente

#### Sistema de Rachas
- **Racha diaria**: Días consecutivos resolviendo problemas
- **Bonus de racha**: Multiplicador de XP que aumenta con la racha
- **Visualización**: Calendario con días marcados

#### Misiones y Quests
- **Misiones diarias**: Desafíos que se renuevan cada día
- **Recompensas**: XP extra, monedas y badges exclusivos
- **Progreso visual**: Barra de progreso para cada misión

#### Tabla de Clasificación
- **Ranking global**: Top 50 usuarios por XP total
- **Ranking semanal**: Top 50 usuarios por XP semanal
- **Sistema de ligas**: Bronce, Plata, Oro, Platino, Diamante

#### Power-ups
- **Pista**: Muestra una pista del problema (-50% XP)
- **Tiempo extra**: +30 segundos en problemas con tiempo (próximamente)
- **Eliminar opción**: Quita una respuesta incorrecta (próximamente)

## 🚀 Instalación

### Requisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Pasos

1. **Clonar o descargar el proyecto**

2. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

3. **Ejecutar la aplicación**:
```bash
python app.py
```

4. **Abrir en el navegador**:
```
http://localhost:5000
```

## 📁 Estructura del Proyecto

```
/
├── app.py                      # Aplicación Flask principal
├── database.py                 # Modelos y conexión a base de datos
├── problem_generator.py         # Generador de problemas matemáticos
├── adaptive_algorithm.py        # Algoritmo adaptativo
├── gamification.py             # Sistema de gamificación
├── requirements.txt            # Dependencias Python
├── database.db                 # Base de datos SQLite (se crea automáticamente)
├── static/
│   ├── css/
│   │   ├── main.css           # Estilos principales
│   │   ├── dashboard.css      # Estilos del dashboard
│   │   └── problem.css        # Estilos de problemas
│   ├── js/
│   │   ├── main.js            # JavaScript principal
│   │   ├── problem.js         # Lógica de problemas
│   │   └── animations.js      # Animaciones y efectos
│   └── images/
│       ├── avatars/           # Imágenes de avatares
│       └── badges/            # Iconos de badges
└── templates/
    ├── base.html              # Template base
    ├── index.html             # Dashboard
    ├── login.html             # Página de login
    ├── register.html         # Página de registro
    ├── problem.html           # Página de problemas
    ├── progress.html          # Página de progreso
    ├── achievements.html      # Página de logros
    ├── shop.html              # Tienda
    └── leaderboard.html       # Clasificación
```

## 🎯 Uso

### Primera vez
1. Crea una cuenta en "Registrarse"
2. Inicia sesión
3. ¡Comienza a resolver problemas!

### Resolver Problemas
1. Ve a "Resolver Problema" desde el dashboard
2. Lee el problema cuidadosamente
3. Selecciona o ingresa tu respuesta
4. Recibe feedback inmediato y gana XP/monedas

### Ver Progreso
- **Dashboard**: Vista general de tu progreso
- **Progreso**: Estadísticas detalladas por tema
- **Logros**: Badges obtenidos
- **Clasificación**: Tu posición en los rankings

## 🔧 Configuración

### Cambiar clave secreta
En `app.py`, cambia:
```python
app.secret_key = 'tu-clave-secreta-cambiar-en-produccion'
```

### Base de datos
La aplicación usa SQLite por defecto. Para producción, considera migrar a PostgreSQL o MySQL.

## 🎨 Personalización

### Temas
Los colores principales se pueden modificar en `static/css/main.css`:
```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
    /* ... */
}
```

### Problemas
Agrega nuevos tipos de problemas en `problem_generator.py`.

## 📝 Notas

- La base de datos se crea automáticamente al iniciar la aplicación
- Las misiones diarias se inicializan automáticamente
- El sistema adaptativo aprende del rendimiento del usuario
- Todos los datos se guardan localmente en SQLite

## 🚧 Próximas Mejoras

- [ ] Sistema de avatares personalizables completo
- [ ] Power-ups en la tienda
- [ ] Modo desafío contra el tiempo
- [ ] Explicaciones paso a paso detalladas
- [ ] Sistema de temporadas y eventos
- [ ] Modo multijugador (desafíos 1v1)
- [ ] Exportar progreso a PDF

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request.

---

¡Disfruta aprendiendo matemáticas de forma divertida! 🎉
