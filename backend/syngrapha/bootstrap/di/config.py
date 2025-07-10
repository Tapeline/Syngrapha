from dishka import Provider, Scope, from_context, provide

from syngrapha.config import (
    AIConfig, Config,
    NalogConfig,
    PostgresConfig,
    ProverkaChekaConfig, SecurityConfig,
)


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

    @provide(scope=Scope.APP)
    def get_nalog_config(self, config: Config) -> NalogConfig:
        """Provide nalog.ru conf."""
        return config.nalog

    @provide(scope=Scope.APP)
    def get_ai_config(self, config: Config) -> AIConfig:
        """Provide nalog.ru conf."""
        return config.ai


    @provide(scope=Scope.APP)
    def get_pc_config(self, config: Config) -> ProverkaChekaConfig:
        """Provide nalog.ru conf."""
        return config.pc_proxy
