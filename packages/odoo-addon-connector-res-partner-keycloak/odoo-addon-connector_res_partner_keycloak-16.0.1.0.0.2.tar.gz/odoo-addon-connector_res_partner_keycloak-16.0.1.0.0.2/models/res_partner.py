# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import fields, models

from ..services.keycloak import KeycloakService


class ResPartner(models.Model):
    _inherit = "res.partner"

    keycloak_group_id = fields.Char(string="Keycloak Group ID")

    def create_keycloak_user(self):
        self.ensure_one()
        KeycloakService(self.env.company).create_keycloak_user(self)
