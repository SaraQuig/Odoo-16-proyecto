from odoo import models, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def get_last_contacts(self):
        """Devuelve los 3 últimos contactos creados"""
        return self.search([], order="create_date desc", limit=3)
