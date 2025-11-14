import json
from database import get_db, update_user_coins, get_user

class ShopSystem:
    """Sistema de tienda y cosméticos"""
    
    # Catálogo de items disponibles
    ITEMS = {
        # Caras
        'face_happy': {'name': 'Cara Feliz', 'icon': '😊', 'category': 'face', 'price': 50, 'type': 'cosmetic'},
        'face_cool': {'name': 'Cara Genial', 'icon': '😎', 'category': 'face', 'price': 75, 'type': 'cosmetic'},
        'face_smart': {'name': 'Cara Inteligente', 'icon': '🤓', 'category': 'face', 'price': 100, 'type': 'cosmetic'},
        'face_hero': {'name': 'Cara de Héroe', 'icon': '🦸', 'category': 'face', 'price': 150, 'type': 'cosmetic'},
        'face_robot': {'name': 'Cara Robot', 'icon': '🤖', 'category': 'face', 'price': 200, 'type': 'cosmetic'},
        
        # Peinados
        'hair_short': {'name': 'Pelo Corto', 'icon': '👨', 'category': 'hair', 'price': 30, 'type': 'cosmetic'},
        'hair_long': {'name': 'Pelo Largo', 'icon': '👩', 'category': 'hair', 'price': 40, 'type': 'cosmetic'},
        'hair_curly': {'name': 'Pelo Rizado', 'icon': '👨‍🦱', 'category': 'hair', 'price': 50, 'type': 'cosmetic'},
        'hair_red': {'name': 'Pelo Rojo', 'icon': '👨‍🦰', 'category': 'hair', 'price': 60, 'type': 'cosmetic'},
        'hair_blonde': {'name': 'Pelo Rubio', 'icon': '👱', 'category': 'hair', 'price': 70, 'type': 'cosmetic'},
        'hair_afro': {'name': 'Afro', 'icon': '👨‍🦲', 'category': 'hair', 'price': 80, 'type': 'cosmetic'},
        'hair_crown': {'name': 'Corona', 'icon': '👑', 'category': 'hair', 'price': 500, 'type': 'cosmetic'},
        
        # Ropa
        'clothes_shirt': {'name': 'Camisa', 'icon': '👔', 'category': 'clothes', 'price': 40, 'type': 'cosmetic'},
        'clothes_tshirt': {'name': 'Camiseta', 'icon': '👕', 'category': 'clothes', 'price': 35, 'type': 'cosmetic'},
        'clothes_jacket': {'name': 'Chaqueta', 'icon': '🧥', 'category': 'clothes', 'price': 80, 'type': 'cosmetic'},
        'clothes_suit': {'name': 'Traje', 'icon': '🤵', 'category': 'clothes', 'price': 200, 'type': 'cosmetic'},
        'clothes_hoodie': {'name': 'Sudadera', 'icon': '🧑‍💼', 'category': 'clothes', 'price': 60, 'type': 'cosmetic'},
        'clothes_armor': {'name': 'Armadura', 'icon': '🛡️', 'category': 'clothes', 'price': 300, 'type': 'cosmetic'},
        
        # Accesorios
        'accessory_glasses': {'name': 'Gafas', 'icon': '👓', 'category': 'accessory', 'price': 50, 'type': 'cosmetic'},
        'accessory_sunglasses': {'name': 'Gafas de Sol', 'icon': '🕶️', 'category': 'accessory', 'price': 75, 'type': 'cosmetic'},
        'accessory_hat': {'name': 'Sombrero', 'icon': '🎩', 'category': 'accessory', 'price': 60, 'type': 'cosmetic'},
        'accessory_cap': {'name': 'Gorra', 'icon': '🧢', 'category': 'accessory', 'price': 40, 'type': 'cosmetic'},
        'accessory_mask': {'name': 'Máscara', 'icon': '🎭', 'category': 'accessory', 'price': 100, 'type': 'cosmetic'},
        'accessory_medal': {'name': 'Medalla', 'icon': '🏅', 'category': 'accessory', 'price': 150, 'type': 'cosmetic'},
        
        # Power-ups
        'powerup_hint': {'name': 'Pista Extra', 'icon': '💡', 'category': 'powerup', 'price': 50, 'type': 'powerup'},
        'powerup_time': {'name': 'Tiempo Extra', 'icon': '⏱️', 'category': 'powerup', 'price': 30, 'type': 'powerup'},
        'powerup_eliminate': {'name': 'Eliminar Opción', 'icon': '❌', 'category': 'powerup', 'price': 40, 'type': 'powerup'},
    }
    
    @staticmethod
    def get_available_items(user_id):
        """Obtiene items disponibles para el usuario"""
        user = get_user(user_id)
        if not user:
            return []
        
        # Obtener items ya comprados
        avatar_data = json.loads(user['avatar_data'] or '{}')
        owned_items = avatar_data.get('owned_items', [])
        
        # Items básicos que todos tienen por defecto
        default_items = ['face_happy', 'hair_short', 'clothes_tshirt']
        
        items = []
        for item_id, item_data in ShopSystem.ITEMS.items():
            owned = item_id in owned_items or item_id in default_items
            items.append({
                'id': item_id,
                'name': item_data['name'],
                'icon': item_data['icon'],
                'category': item_data['category'],
                'price': item_data['price'],
                'type': item_data['type'],
                'owned': owned
            })
        
        return items
    
    @staticmethod
    def purchase_item(user_id, item_id):
        """Compra un item para el usuario"""
        if item_id not in ShopSystem.ITEMS:
            return {'success': False, 'message': 'Item not found'}
        
        user = get_user(user_id)
        if not user:
            return {'success': False, 'message': 'User not found'}
        
        item = ShopSystem.ITEMS[item_id]
        user_coins = user['coins']
        
        # Verificar si ya lo tiene
        avatar_data = json.loads(user['avatar_data'] or '{}')
        owned_items = avatar_data.get('owned_items', [])
        
        if item_id in owned_items:
            return {'success': False, 'message': 'You already own this item'}
        
        # Verificar si tiene suficientes monedas
        if user_coins < item['price']:
            return {'success': False, 'message': f'Not enough coins. You need {item["price"]} coins'}
        
        # Comprar el item
        conn = get_db()
        cursor = conn.cursor()
        
        # Descontar monedas
        update_user_coins(user_id, -item['price'])
        
        # Agregar a items comprados
        owned_items.append(item_id)
        avatar_data['owned_items'] = owned_items
        
        # Guardar avatar_data
        cursor.execute('''
            UPDATE users SET avatar_data = ? WHERE id = ?
        ''', (json.dumps(avatar_data), user_id))
        
        conn.commit()
        conn.close()
        
        return {'success': True, 'message': f'You purchased {item["name"]}!'}
    
    @staticmethod
    def get_user_avatar(user_id):
        """Obtiene la configuración del avatar del usuario"""
        user = get_user(user_id)
        if not user:
            return {}
        
        avatar_data = json.loads(user['avatar_data'] or '{}')
        return {
            'face': avatar_data.get('face', 'face_happy'),
            'hair': avatar_data.get('hair', 'hair_short'),
            'clothes': avatar_data.get('clothes', 'clothes_tshirt'),
            'accessory': avatar_data.get('accessory', None),
            'owned_items': avatar_data.get('owned_items', [])
        }
    
    @staticmethod
    def update_user_avatar(user_id, face=None, hair=None, clothes=None, accessory=None):
        """Actualiza la configuración del avatar del usuario"""
        user = get_user(user_id)
        if not user:
            return {'success': False, 'message': 'User not found'}
        
        avatar_data = json.loads(user['avatar_data'] or '{}')
        owned_items = avatar_data.get('owned_items', [])
        
        # Items básicos que todos tienen
        default_items = ['face_happy', 'hair_short', 'clothes_tshirt']
        all_owned = owned_items + default_items
        
        # Verificar que el usuario posea los items
        if face and face not in all_owned:
            return {'success': False, 'message': 'You do not own this face'}
        if hair and hair not in all_owned:
            return {'success': False, 'message': 'You do not own this hair'}
        if clothes and clothes not in all_owned:
            return {'success': False, 'message': 'You do not own this clothing'}
        if accessory and accessory not in all_owned and accessory:
            return {'success': False, 'message': 'You do not own this accessory'}
        
        # Actualizar avatar
        if face:
            avatar_data['face'] = face
        if hair:
            avatar_data['hair'] = hair
        if clothes:
            avatar_data['clothes'] = clothes
        if accessory is not None:
            avatar_data['accessory'] = accessory if accessory else None
        
        # Guardar
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            UPDATE users SET avatar_data = ? WHERE id = ?
        ''', (json.dumps(avatar_data), user_id))
        conn.commit()
        conn.close()
        
        return {'success': True, 'message': 'Avatar updated!'}
    
    @staticmethod
    def get_items_by_category():
        """Obtiene items agrupados por categoría"""
        categories = {
            'face': [],
            'hair': [],
            'clothes': [],
            'accessory': [],
            'powerup': []
        }
        
        for item_id, item_data in ShopSystem.ITEMS.items():
            category = item_data['category']
            if category in categories:
                categories[category].append({
                    'id': item_id,
                    **item_data
                })
        
        return categories

