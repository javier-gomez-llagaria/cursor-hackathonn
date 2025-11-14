# 📐 MathGame - Plataforma Gamificada de Matemáticas

Una aplicación web gamificada para aprender matemáticas de forma divertida, diseñada para estudiantes de ESO y Bachillerato.

## 🎮 Características Principales

### 🗺️ Mapa de Reinos
- **5 Reinos Matemáticos**: Aritmética, Álgebra, Geometría, Trigonometría, Cálculo
- **Sistema de Niveles**: 10 niveles por reino
- **Tareas y Exámenes**: Completa tareas (azules) y exámenes (rojos) para avanzar

### 🎯 Sistema Adaptativo
- Identifica áreas débiles automáticamente
- Ajusta la dificultad según tu rendimiento
- Prioriza temas que necesitas practicar más

### 🏆 Gamificación Completa
- **XP y Niveles**: Gana experiencia resolviendo problemas
- **Monedas**: Gasta en la tienda de cosméticos
- **Badges**: 12+ logros diferentes para desbloquear
- **Rachas**: Mantén días consecutivos para bonus
- **Misiones**: Desafíos diarios y semanales
- **Clasificación**: Compite con otros usuarios

### 🛒 Tienda y Personalización
- **Cosméticos para Avatar**: Caras, peinados, ropa, accesorios
- **Power-ups**: Pistas, tiempo extra, eliminar opciones
- **Más de 20 items** disponibles para comprar

## 🚀 Instalación Local

### Windows:
```powershell
.\instalar.bat
python app.py
```

### Linux/Mac:
```bash
chmod +x instalar.sh
./instalar.sh
python3 app.py
```

Luego abre: http://localhost:5000

## 📦 Desplegar Online

### Opción 1: Render.com (Recomendado - Gratis)

1. **Instala Git**: https://git-scm.com/download/win
2. **Inicializa Git**:
   ```powershell
   .\inicializar_git.ps1
   ```
3. **Sigue las instrucciones** en `SETUP_GIT.md`
4. **Despliega en Render.com** (gratis)

Ver `COMO_DESPLEGAR.md` para guía detallada.

## 📁 Estructura del Proyecto

```
mathgame/
├── app.py                 # Aplicación Flask principal
├── database.py            # Modelos de base de datos
├── problem_generator.py   # Generador de problemas
├── adaptive_algorithm.py  # Algoritmo adaptativo
├── gamification.py        # Sistema de gamificación
├── shop_system.py         # Sistema de tienda
├── map_system.py          # Sistema de mapa de reinos
├── templates/             # Templates HTML
├── static/                # CSS, JS, imágenes
└── requirements.txt       # Dependencias
```

## 🎯 Tecnologías

- **Backend**: Flask (Python)
- **Base de Datos**: SQLite (fácil migración a PostgreSQL)
- **Frontend**: HTML5, CSS3, JavaScript
- **Despliegue**: Render.com, Railway, Heroku

## 📝 Requisitos

- Python 3.8+
- pip (gestor de paquetes)

## 🔧 Configuración

### Variables de Entorno

Para producción, configura:
- `SECRET_KEY`: Clave secreta para sesiones (genera una segura)

### Base de Datos

La base de datos se crea automáticamente al iniciar. Para producción, considera usar PostgreSQL.

## 🎨 Personalización

Los colores principales se pueden modificar en `static/css/main.css`:
```css
:root {
    --primary-color: #667eea;
    --secondary-color: #764ba2;
}
```

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso educativo.

## 👥 Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o pull request.

---

¡Disfruta aprendiendo matemáticas de forma divertida! 🎉
