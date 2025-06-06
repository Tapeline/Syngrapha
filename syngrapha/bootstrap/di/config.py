from dishka import Provider, Scope, from_context, provide

from syngrapha.config import Config, PostgresConfig, SecurityConfig


class ConfigDIProvider(Provider):
    """Provider of config."""

    config = from_context(Config, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_pg_config(self, config: Config) -> PostgresConfig:
        """Provide pg conf."""
        return config.postgres

    @provide(scope=Scope.APP)
    def get_sec_config(self, config: Config) -> SecurityConfig:
        """Provide security conf."""
        return config.security
