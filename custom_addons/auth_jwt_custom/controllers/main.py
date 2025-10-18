from odoo import http
from odoo.http import request
from odoo.addons.auth_jwt.tools import jwt_auth
from odoo.tools import config
import logging

_logger = logging.getLogger(__name__)

# =====================================================
# LOGIN USANDO AUTH_JWT (OCA)
# =====================================================
class JWTAuthController(http.Controller):

    @http.route('/api/jwt/login', type='json', auth='none', methods=['POST'], csrf=False)
    def jwt_login(self, **kwargs):
        """Autenticación estándar Odoo con generación de token JWT OCA."""
        login = kwargs.get('login')
        password = kwargs.get('password')

        # Autenticación normal de Odoo
        uid = request.session.authenticate(request.db, login, password)
        if not uid:
            return {'error': 'Credenciales inválidas'}

        user = request.env['res.users'].browse(uid)

        # Generar token con el validador 'api'
        try:
            token = request.env['auth.jwt.validator']._get_validator_by_name('api')._encode(
                {'uid': user.id, 'login': user.login},
                secret=config.get('jwt_secret', 'MiClaveJWTsuperSegura123'),
                expire=int(config.get('jwt_expiration', 3600))
            )
        except Exception as e:
            _logger.error(f"Error generando token JWT: {e}")
            return {'error': str(e)}

        return {
            'message': f'Inicio de sesión exitoso. Bienvenido {user.name}',
            'token': token
        }


# =====================================================
# CRUD CONTACTOS (RUTAS PROTEGIDAS CON JWT OCA)
# =====================================================
class ContactAPIController(http.Controller):

    @http.route('/api/contacts', type='json', auth='jwt_api', methods=['POST'], csrf=False, save_session=False)
    def create_contact(self, **kwargs):
        import json

        try:
            data = json.loads(request.httprequest.data)
        except Exception:
            return request.make_json_response({'error': 'JSON inválido o malformado'}, status=400)

        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')

        if not name:
            return request.make_json_response({'error': 'El campo "name" es obligatorio'}, status=400)

        contact = request.env['res.partner'].sudo().create({
            'name': name,
            'email': email,
            'phone': phone,
        })

        return request.make_json_response({
            'success': True,
            'message': f'Contacto {contact.name} creado correctamente',
            'id': contact.id
        }, status=200)

    @http.route('/api/contacts', type='http', auth='jwt_api', methods=['GET'], csrf=False, save_session=False)
    def list_contacts(self, **kwargs):
        """Listar los últimos 3 contactos"""
        contacts = request.env['res.partner'].sudo().search([], order='id desc', limit=3)
        data = [{'id': c.id, 'name': c.name, 'email': c.email, 'phone': c.phone} for c in contacts]
        return request.make_json_response({'ultimos_3_contactos': data})

    @http.route('/api/contacts/<int:contact_id>', type='http', auth='jwt_api', methods=['PUT'], csrf=False,
                save_session=False)
    def update_contact(self, contact_id, **kwargs):
        """Actualizar un contacto existente"""
        import json

        try:
            data = json.loads(request.httprequest.data)
        except Exception:
            return request.make_json_response({'error': 'JSON inválido o malformado'}, status=400)

        contact = request.env['res.partner'].sudo().browse(contact_id)
        if not contact.exists():
            return request.make_json_response({'error': 'Contacto no encontrado'}, status=404)

        contact.write({
            'name': data.get('name', contact.name),
            'email': data.get('email', contact.email),
            'phone': data.get('phone', contact.phone),
        })

        return request.make_json_response({
            'success': True,
            'message': f'Contacto {contact.name} actualizado correctamente',
            'id': contact.id
        }, status=200)

    @http.route('/api/contacts/<int:contact_id>', type='http', auth='jwt_api', methods=['DELETE'], csrf=False, save_session=False)
    def delete_contact(self, contact_id, **kwargs):
        """Eliminar contacto por ID"""
        contact = request.env['res.partner'].sudo().browse(contact_id)
        if not contact.exists():
            return request.make_json_response({'error': 'Contacto no encontrado'}, status=404)
        contact.unlink()
        return request.make_json_response({'message': f'Contacto {contact_id} eliminado correctamente'})
