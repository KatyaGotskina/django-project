from django.test.runner import DiscoverRunner

class PostgresSchemaRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        return super().setup_databases(**kwargs)