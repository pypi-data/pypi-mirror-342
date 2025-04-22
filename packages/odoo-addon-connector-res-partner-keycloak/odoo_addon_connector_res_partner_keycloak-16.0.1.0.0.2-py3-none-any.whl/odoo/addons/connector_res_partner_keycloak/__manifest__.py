{
    "name": "ResPartner Keycloak connector",
    "version": "16.0.1.0.0",
    "depends": ["auth_oidc", "base", "component_event", "queue_job"],
    "author": "Coopdevs Treball SCCL",
    "category": "",
    "website": "https://coopdevs.org",
    "license": "AGPL-3",
    "summary": """
        Connector to create users in Keycloak when a new customer is created.
    """,
    "data": [
        "views/res_company.xml",
    ],
    "installable": True,
    "external_dependencies": {"python": ["python-keycloak"]},
}
