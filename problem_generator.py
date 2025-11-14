import random
import math

# Helper para LCM (mínimo común múltiplo) si no está disponible
def lcm(a, b):
    """Calcula el mínimo común múltiplo"""
    if hasattr(math, 'lcm'):
        return math.lcm(a, b)
    return abs(a * b) // math.gcd(a, b)

class ProblemGenerator:
    """Genera problemas matemáticos dinámicamente por tema y dificultad"""
    
    TOPICS = {
        'aritmetica': ['suma', 'resta', 'multiplicacion', 'division', 'fracciones', 'decimales', 'porcentajes'],
        'algebra': ['ecuaciones_lineales', 'ecuaciones_cuadraticas', 'sistemas', 'expresiones'],
        'geometria': ['areas', 'perimetros', 'volumenes', 'teoremas'],
        'trigonometria': ['seno', 'coseno', 'tangente', 'identidades'],
        'calculo': ['derivadas', 'integrales', 'limites']
    }
    
    @staticmethod
    def generate(topic, difficulty=1):
        """Genera un problema según el tema y dificultad"""
        if topic == 'aritmetica':
            return ProblemGenerator._generate_arithmetic(difficulty)
        elif topic == 'algebra':
            return ProblemGenerator._generate_algebra(difficulty)
        elif topic == 'geometria':
            return ProblemGenerator._generate_geometry(difficulty)
        elif topic == 'trigonometria':
            return ProblemGenerator._generate_trigonometry(difficulty)
        elif topic == 'calculo':
            return ProblemGenerator._generate_calculus(difficulty)
        else:
            return ProblemGenerator._generate_arithmetic(difficulty)
    
    @staticmethod
    def _generate_arithmetic(difficulty):
        """Genera problemas de aritmética"""
        if difficulty <= 2:
            # Sumas y restas simples
            a = random.randint(10, 100)
            b = random.randint(10, 100)
            op = random.choice(['+', '-'])
            if op == '+':
                result = a + b
                problem = f"{a} + {b} = ?"
            else:
                result = a - b
                problem = f"{a} - {b} = ?"
        
        elif difficulty <= 4:
            # Multiplicaciones y divisiones
            a = random.randint(2, 12)
            b = random.randint(2, 12)
            op = random.choice(['×', '÷'])
            if op == '×':
                result = a * b
                problem = f"{a} × {b} = ?"
            else:
                result = a
                problem = f"{a * b} ÷ {b} = ?"
        
        elif difficulty <= 6:
            # Fracciones
            num1 = random.randint(1, 10)
            den1 = random.randint(2, 10)
            num2 = random.randint(1, 10)
            den2 = random.randint(2, 10)
            op = random.choice(['+', '-'])
            
            if op == '+':
                # Suma de fracciones
                lcm_val = lcm(den1, den2)
                result_num = (num1 * lcm_val // den1) + (num2 * lcm_val // den2)
                result_den = lcm_val
                gcd = math.gcd(result_num, result_den)
                result = f"{result_num // gcd}/{result_den // gcd}"
                problem = f"{num1}/{den1} + {num2}/{den2} = ?"
            else:
                # Resta de fracciones
                lcm_val = lcm(den1, den2)
                result_num = (num1 * lcm_val // den1) - (num2 * lcm_val // den2)
                result_den = lcm_val
                gcd = math.gcd(result_num, result_den)
                result = f"{result_num // gcd}/{result_den // gcd}"
                problem = f"{num1}/{den1} - {num2}/{den2} = ?"
        
        elif difficulty <= 8:
            # Porcentajes
            base = random.randint(50, 500)
            percentage = random.choice([10, 20, 25, 50, 75])
            result = round(base * percentage / 100, 2)
            problem = f"¿Cuánto es el {percentage}% de {base}?"
        
        else:
            # Operaciones combinadas
            a = random.randint(10, 50)
            b = random.randint(5, 25)
            c = random.randint(2, 10)
            result = (a + b) * c
            problem = f"({a} + {b}) × {c} = ?"
        
        # Generar opciones múltiples
        options = ProblemGenerator._generate_options(result, difficulty)
        
        return {
            'problem_text': problem,
            'solution': str(result),
            'options': options,
            'topic': 'aritmetica',
            'subtopic': 'operaciones_basicas',
            'difficulty': difficulty,
            'explanation': f"La respuesta es {result}"
        }
    
    @staticmethod
    def _generate_algebra(difficulty):
        """Genera problemas de álgebra"""
        if difficulty <= 3:
            # Ecuaciones lineales simples: ax + b = c
            a = random.randint(2, 10)
            b = random.randint(1, 20)
            x = random.randint(1, 10)
            c = a * x + b
            
            problem = f"{a}x + {b} = {c}"
            result = x
            explanation = f"Restamos {b} a ambos lados: {a}x = {c - b}. Dividimos por {a}: x = {x}"
        
        elif difficulty <= 5:
            # Ecuaciones lineales: ax + b = cx + d
            a = random.randint(2, 8)
            c = random.randint(1, 6)
            x = random.randint(1, 10)
            b = random.randint(1, 15)
            d = (a - c) * x + b
            
            problem = f"{a}x + {b} = {c}x + {d}"
            result = x
            explanation = f"Agrupamos términos: {a - c}x = {d - b}. Dividimos: x = {x}"
        
        elif difficulty <= 7:
            # Ecuaciones cuadráticas simples: x² = a
            x = random.randint(2, 15)
            a = x * x
            problem = f"x² = {a}"
            result = x
            explanation = f"Tomamos la raíz cuadrada: x = {x} (solo consideramos la solución positiva)"
        
        else:
            # Ecuaciones cuadráticas: ax² + bx + c = 0
            x1 = random.randint(1, 5)
            x2 = random.randint(1, 5)
            a = 1
            b = -(x1 + x2)
            c = x1 * x2
            
            problem = f"x² + {b}x + {c} = 0"
            # Usamos la menor solución positiva
            result = min(x1, x2)
            explanation = f"Factorizamos: (x - {x1})(x - {x2}) = 0. Soluciones: x = {x1} o x = {x2}"
        
        options = ProblemGenerator._generate_options(result, difficulty)
        
        return {
            'problem_text': problem,
            'solution': str(result),
            'options': options,
            'topic': 'algebra',
            'subtopic': 'ecuaciones',
            'difficulty': difficulty,
            'explanation': explanation
        }
    
    @staticmethod
    def _generate_geometry(difficulty):
        """Genera problemas de geometría"""
        if difficulty <= 3:
            # Área de rectángulo
            length = random.randint(5, 20)
            width = random.randint(5, 20)
            result = length * width
            problem = f"Calcula el área de un rectángulo de {length} cm de largo y {width} cm de ancho"
            explanation = f"Área = largo × ancho = {length} × {width} = {result} cm²"
        
        elif difficulty <= 5:
            # Área de triángulo
            base = random.randint(5, 20)
            height = random.randint(5, 20)
            result = round(base * height / 2, 1)
            problem = f"Calcula el área de un triángulo de base {base} cm y altura {height} cm"
            explanation = f"Área = (base × altura) / 2 = ({base} × {height}) / 2 = {result} cm²"
        
        elif difficulty <= 7:
            # Área de círculo
            radius = random.randint(3, 15)
            result = round(math.pi * radius * radius, 2)
            problem = f"Calcula el área de un círculo de radio {radius} cm"
            explanation = f"Área = π × r² = π × {radius}² = {result} cm²"
        
        else:
            # Volumen de cilindro
            radius = random.randint(2, 10)
            height = random.randint(5, 20)
            result = round(math.pi * radius * radius * height, 2)
            problem = f"Calcula el volumen de un cilindro de radio {radius} cm y altura {height} cm"
            explanation = f"Volumen = π × r² × h = π × {radius}² × {height} = {result} cm³"
        
        options = ProblemGenerator._generate_options(result, difficulty)
        
        return {
            'problem_text': problem,
            'solution': str(result),
            'options': options,
            'topic': 'geometria',
            'subtopic': 'areas',
            'difficulty': difficulty,
            'explanation': explanation
        }
    
    @staticmethod
    def _generate_trigonometry(difficulty):
        """Genera problemas de trigonometría"""
        if difficulty <= 4:
            # Valores conocidos de seno/coseno
            angles = [0, 30, 45, 60, 90]
            angle = random.choice(angles)
            func = random.choice(['sin', 'cos'])
            
            if func == 'sin':
                values = {0: 0, 30: 0.5, 45: round(math.sqrt(2)/2, 3), 60: round(math.sqrt(3)/2, 3), 90: 1}
                result = values[angle]
                problem = f"Calcula sin({angle}°)"
            else:
                values = {0: 1, 30: round(math.sqrt(3)/2, 3), 45: round(math.sqrt(2)/2, 3), 60: 0.5, 90: 0}
                result = values[angle]
                problem = f"Calcula cos({angle}°)"
            
            explanation = f"El valor de {func}({angle}°) es {result}"
        
        else:
            # Problemas con triángulos rectángulos
            angle_deg = random.choice([30, 45, 60])
            side = random.randint(5, 20)
            func = random.choice(['sin', 'cos'])
            
            angle_rad = math.radians(angle_deg)
            if func == 'sin':
                result = round(side / math.sin(angle_rad), 2)
                problem = f"En un triángulo rectángulo, el cateto opuesto a {angle_deg}° mide {side}. Calcula la hipotenusa"
            else:
                result = round(side / math.cos(angle_rad), 2)
                problem = f"En un triángulo rectángulo, el cateto adyacente a {angle_deg}° mide {side}. Calcula la hipotenusa"
            
            explanation = f"Usando {func}({angle_deg}°) = cateto/hipotenusa, despejamos: hipotenusa = {result}"
        
        options = ProblemGenerator._generate_options(result, difficulty)
        
        return {
            'problem_text': problem,
            'solution': str(result),
            'options': options,
            'topic': 'trigonometria',
            'subtopic': 'razones',
            'difficulty': difficulty,
            'explanation': explanation
        }
    
    @staticmethod
    def _generate_calculus(difficulty):
        """Genera problemas de cálculo básico"""
        if difficulty <= 5:
            # Derivadas simples
            coeff = random.randint(2, 10)
            power = random.randint(2, 5)
            problem = f"Calcula la derivada de f(x) = {coeff}x^{power}"
            result = f"{coeff * power}x^{power - 1}"
            explanation = f"d/dx({coeff}x^{power}) = {coeff * power}x^{power - 1}"
        
        else:
            # Integrales simples
            coeff = random.randint(2, 8)
            power = random.randint(1, 4)
            new_coeff = round(coeff / (power + 1), 2)
            problem = f"Calcula la integral de {coeff}x^{power}"
            result = f"{new_coeff}x^{power + 1} + C"
            explanation = f"∫{coeff}x^{power}dx = {new_coeff}x^{power + 1} + C"
        
        # Para cálculo, las opciones son fórmulas
        options = [
            result,
            result.replace('x', '2x') if 'x' in result else result,
            result.replace(str(coeff), str(coeff * 2)) if str(coeff) in result else result,
            result.replace('+ C', '') if '+ C' in result else result + ' + C'
        ]
        options = list(set(options))[:4]
        while len(options) < 4:
            options.append(f"x^{power + 2}")
        
        return {
            'problem_text': problem,
            'solution': result,
            'options': options,
            'topic': 'calculo',
            'subtopic': 'derivadas',
            'difficulty': difficulty,
            'explanation': explanation
        }
    
    @staticmethod
    def _generate_options(correct_answer, difficulty):
        """Genera opciones múltiples con la respuesta correcta"""
        try:
            correct = float(correct_answer)
            options = [correct]
            
            # Generar opciones incorrectas
            for _ in range(3):
                # Variar entre -50% y +50% de la respuesta correcta
                variation = random.uniform(-0.5, 0.5)
                wrong = round(correct * (1 + variation), 2)
                if wrong < 0:
                    wrong = abs(wrong)
                options.append(wrong)
            
            random.shuffle(options)
            return [str(opt) for opt in options]
        except (ValueError, TypeError):
            # Si no es numérico, devolver opciones simples
            return [str(correct_answer), "Otra opción 1", "Otra opción 2", "Otra opción 3"]

