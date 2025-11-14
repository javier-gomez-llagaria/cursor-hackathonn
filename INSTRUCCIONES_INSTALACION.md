# 📦 Instrucciones de Instalación - MathGame

## Paso 1: Instalar Python

Si aún no tienes Python instalado:

1. Ve a: https://www.python.org/downloads/
2. Descarga la última versión (Python 3.11 o 3.12)
3. **IMPORTANTE**: Durante la instalación, marca la casilla **"Add Python to PATH"**
4. Haz clic en "Install Now"

## Paso 2: Instalar Dependencias

Tienes dos opciones:

### Opción A: Usar el script automático (FÁCIL)

**En Windows:**
- Haz doble clic en `instalar.bat`
- O ejecuta en PowerShell: `.\instalar.ps1`

**En Mac/Linux:**
```bash
chmod +x instalar.sh
./instalar.sh
```

### Opción B: Instalar manualmente

Abre PowerShell o Terminal y ejecuta:

```bash
# Actualizar pip
python -m pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt
```

## Paso 3: Ejecutar la Aplicación

### Opción A: Usar el script (FÁCIL)

Haz doble clic en `ejecutar.bat`

### Opción B: Comando manual

```bash
python app.py
```

## Paso 4: Abrir en el Navegador

Una vez que veas el mensaje:
```
 * Running on http://127.0.0.1:5000
```

Abre tu navegador y ve a:
```
http://localhost:5000
```

## 🔧 Solución de Problemas

### Error: "python no se reconoce como comando"

**Solución:**
1. Python no está en el PATH
2. Reinstala Python y marca "Add Python to PATH"
3. O agrega Python manualmente al PATH del sistema

### Error: "pip no se reconoce como comando"

**Solución:**
```bash
python -m pip install --upgrade pip
```

### Error: "ModuleNotFoundError: No module named 'flask'"

**Solución:**
```bash
pip install -r requirements.txt
```

### Error de permisos en Windows

**Solución:**
Ejecuta PowerShell como Administrador:
1. Click derecho en PowerShell
2. "Ejecutar como administrador"
3. Ejecuta los comandos de nuevo

## ✅ Verificar Instalación

Para verificar que todo está instalado correctamente:

```bash
python --version
pip list
```

Deberías ver Flask y otras dependencias en la lista.

## 🚀 Listo!

Una vez instalado, puedes:
- Ejecutar la app con `python app.py`
- Crear una cuenta en la aplicación
- Comenzar a resolver problemas matemáticos

---

¿Necesitas ayuda? Revisa los logs de error o consulta la documentación.

