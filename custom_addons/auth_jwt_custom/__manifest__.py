{
    'name': 'Auth JWT Custom',
    'version': '16.0.1.0.0',
    'author': 'Tu Nombre',
    'depends': ['base', 'auth_jwt'],
    'category': 'Authentication',
    'summary': 'Autenticación JWT personalizada para APIs',
    'data': [],
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
    'post_load': 'post_load_patch',
}
