def get_provider_info():
    return {
        "package-name": "rocketx-providers-common-sql",
        "name": "Common SQL",
        "description": "`Common SQL Provider <https://en.wikipedia.org/wiki/SQL>`__\n",
        "integrations": [
            {
                "integration-name": "Common SQL",
                "external-doc-url": "https://en.wikipedia.org/wiki/SQL",
                "how-to-guide": ["/docs/apache-airflow-providers-common-sql/operators.rst"],
                "logo": "/docs/integration-logos/sql.png",
                "tags": ["software"],
            }
        ],
        "operators": [
            {
                "integration-name": "Common SQL",
                "python-modules": [
                    "rocketx.providers.common.sql.operators.sql",
                    "rocketx.providers.common.sql.operators.generic_transfer",
                ],
            }
        ],
        "dialects": [
            {
                "dialect-type": "default",
                "dialect-class-name": "rocketx.providers.common.sql.dialects.dialect.Dialect",
            }
        ],
        "hooks": [
            {
                "integration-name": "Common SQL",
                "python-modules": [
                    "rocketx.providers.common.sql.hooks.handlers",
                    "rocketx.providers.common.sql.hooks.sql",
                ],
            }
        ],
        "triggers": [
            {
                "integration-name": "Common SQL",
                "python-modules": ["rocketx.providers.common.sql.triggers.sql"],
            }
        ],
        "sensors": [
            {"integration-name": "Common SQL", "python-modules": ["rocketx.providers.common.sql.sensors.sql"]}
        ],
    }