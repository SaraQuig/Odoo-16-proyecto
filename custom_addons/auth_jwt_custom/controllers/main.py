from odoo import http
from odoo.http import request
import jwt
import datetime
import os

# Clave secreta para firmar el token
SECRET_KEY = "mi_clave_secreta"

# Ruta absoluta donde se guardará el token
TOKEN_FILE = os.path.join(os.path.dirname(__file__), "../token.txt")

def create_jwt(user_id):
    """Genera un token JWT y lo guarda en un archivo"""
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    token = jwt.encode({'user_id': user_id, 'exp': expiration}, SECRET_KEY, algorithm='HS256')

    # Guardar el token en el archivo
    with open(TOKEN_FILE, 'w') as f:
        f.write(token)

    return token


def verify_jwt(token):
    """Verifica si el token JWT es válido"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['user_id']
    except Exception:
        return None


class ContactAPI(http.Controller):

    @http.route('/api/token', type='json', auth='none', methods=['POST'])
    def get_token(self, **kwargs):
        """Genera y guarda el token JWT"""
        login = kwargs.get('login')
        password = kwargs.get('password')

        if not login or not password:
            return {'error': 'Faltan login o contraseña'}

        # Buscar usuario por login o email
        user = request.env['res.users'].sudo().search(
            ['|', ('login', '=', login), ('email', '=', login)], limit=1
        )

        if not user:
            return {'error': 'Usuario no encontrado'}

        # Validar credenciales manualmente
        try:
            request.env['res.users'].sudo().with_user(user)._check_credentials(password)
        except Exception:
            return {'error': 'Contraseña inválida'}

        # Crear y guardar token JWT
        token = create_jwt(user.id)

        return {
            'success': True,
            'user_id': user.id,
            'login': user.login,
            'token': token,
            'token_file': os.path.abspath(TOKEN_FILE)
        }

    @http.route('/api/contact', type='json', auth='none', methods=['POST'])
    def create_contact(self, **kwargs):
        """Crea un contacto si el token es válido"""
        token = kwargs.get('token')
        user_id = verify_jwt(token)
        if not user_id:
            return {'error': 'Token inválido o expirado'}

        name = kwargs.get('name')
        email = kwargs.get('email')

        if not name or not email:
            return {'error': 'Faltan campos obligatorios'}

        contact = request.env['res.partner'].sudo().create({
            'name': name,
            'email': email
        })

        return {'success': True, 'contact_id': contact.id, 'name': contact.name}

    @http.route('/api/contact', type='json', auth='none', methods=['GET'])
    def list_contacts(self, **kwargs):
        """Lista todos los contactos si el token es válido"""
        token = kwargs.get('token')
        user_id = verify_jwt(token)
        if not user_id:
            return {'error': 'Token inválido o expirado'}

        contacts = request.env['res.partner'].sudo().search([])
        data = [{'id': c.id, 'name': c.name, 'email': c.email} for c in contacts]
        return {'contacts': data}
