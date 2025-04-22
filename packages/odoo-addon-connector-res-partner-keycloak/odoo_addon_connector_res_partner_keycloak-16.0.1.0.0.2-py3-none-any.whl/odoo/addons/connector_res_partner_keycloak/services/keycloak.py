import logging

from keycloak import KeycloakAdmin, KeycloakOpenIDConnection
from keycloak.exceptions import KeycloakPostError, KeycloakPutError

_logger = logging.getLogger(__name__)


class KeycloakService:
    def __init__(self, company):
        _logger.debug("Create Admin connection with Keycloak...")
        keycloak_connection = KeycloakOpenIDConnection(
            server_url=company.keycloak_url,
            username=company.keycloak_admin_user,
            password=company.keycloak_admin_password,
            user_realm_name=company.keycloak_user_realm_name,
            realm_name=company.keycloak_realm_name,
            client_id=company.keycloak_client_id,
            client_secret_key=company.keycloak_client_secret,
            verify=True,
        )
        self.keycloak_admin = KeycloakAdmin(connection=keycloak_connection)
        _logger.debug("Admin connection created.")

    def create_keycloak_user(self, record):
        _logger.debug(f"Create the user for username {record.vat}")
        user = self.keycloak_admin.create_user(
            {
                "email": record.email,
                "username": record.vat,
                "firstName": record.firstname,
                "lastName": record.lastname,
                "enabled": True,
                "emailVerified": False,
                "requiredActions": ["UPDATE_PASSWORD", "VERIFY_EMAIL"],
            },
            exist_ok=True,
        )
        # Update the password
        self.keycloak_admin.send_update_account(
            user_id=user, payload=["UPDATE_PASSWORD"]
        )
        _logger.debug(f"User created for username {record.vat}")
