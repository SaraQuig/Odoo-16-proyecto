import logging
import inspect
from odoo import http

_logger = logging.getLogger(__name__)
print("🚀 [Auth JWT Custom] Archivo ir_http_patch.py cargado correctamente")

def post_load_patch():
    """Hook post_load: evita UnauthorizedSessionMismatch para rutas JWT (OCA)"""
    print("🔍 [Auth JWT Custom] Ejecutando post_load_patch()")

    ir_http_class = None

    try:
        from odoo.addons.auth_jwt.models import ir_http as jwt_ir_http

        # Detectar la clase correcta
        for name, obj in inspect.getmembers(jwt_ir_http, inspect.isclass):
            if "irhttp" in name.lower() or "jwt" in name.lower():
                ir_http_class = obj
                break

        if not ir_http_class:
            raise ImportError("No se encontró clase ir_http o IrHttpJwt en auth_jwt")

    except Exception as e:
        print(f"❌ [Auth JWT Custom] No se pudo importar ir_http: {e}")
        _logger.error(f"No se pudo importar ir_http: {e}")
        return

    # Evitar doble parche
    if hasattr(ir_http_class, "_original_authenticate"):
        print("ℹ️ [Auth JWT Custom] Parche ya aplicado.")
        return

    if not hasattr(ir_http_class, "_authenticate"):
        print("⚠️ [Auth JWT Custom] Clase sin método _authenticate. Abortando parche.")
        return

    print(f"🔧 [Auth JWT Custom] Aplicando parche sobre {ir_http_class.__name__}...")

    original_auth = getattr(ir_http_class, "_authenticate", None)
    ir_http_class._original_authenticate = original_auth

    def _authenticate_no_session(endpoint):
        """Versión extendida que ignora validación de sesión solo para rutas JWT"""
        routing = getattr(endpoint, "routing", {})
        auth_mode = routing.get("auth")
        route = routing.get("route", "desconocida")

        if isinstance(auth_mode, str) and auth_mode.startswith("jwt"):
            msg = f"✅ [Auth JWT Custom] Ruta JWT detectada ({route}) → sesión omitida."
            print(msg)
            _logger.info(msg)
            return

        try:
            if callable(ir_http_class._original_authenticate):
                return ir_http_class._original_authenticate(endpoint)
            else:
                _logger.warning("⚠️ _original_authenticate no es callable, ignorando super().")
        except AttributeError:
            _logger.warning("⚠️ No existe super()._authenticate en clase IrHttpJwt, continuando sin error.")

    ir_http_class._authenticate = _authenticate_no_session

    print(f"✅ [Auth JWT Custom] Parche aplicado exitosamente en {ir_http_class.__name__}.")
    _logger.info(f"✅ Parche JWT aplicado correctamente en {ir_http_class.__name__}")
