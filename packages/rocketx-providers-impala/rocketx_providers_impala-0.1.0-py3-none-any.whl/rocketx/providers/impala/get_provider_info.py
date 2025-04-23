def get_provider_info():
    return {
        "package-name": "rocketx-providers-impala",
        "name": "Apache Impala",
        "description": "`Apache Impala <https://impala.apache.org/>`__.\n",
        "integrations": [
            {
                "integration-name": "Apache Impala",
                "external-doc-url": "https://impala.apache.org",
                "tags": ["apache"],
            }
        ],
        "hooks": [
            {
                "integration-name": "Apache Impala",
                "python-modules": ["rocketx.providers.impala.hooks.impala"],
            }
        ],
        "connection-types": [
            {
                "hook-class-name": "rocketx.providers.impala.hooks.impala.ImpalaHook",
                "connection-type": "impala",
            }
        ],
    }