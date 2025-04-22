import logging

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)


class PartnerListener(Component):
    _name = "partner.listener"
    _inherit = "base.event.listener"
    _apply_on = ["res.partner"]

    def on_record_create(self, record, fields=None):
        _logger.debug("Check if is needed create a user in Keycloak...")
        if self.env.company.keycloak_connector_enabled and not record.is_company:
            _logger.debug("Creating user in Keycloak...")
            record.with_delay().create_keycloak_user()
