from dishka import Provider, Scope, provide

from syngrapha.application.external.ai_categorizer import AICategorizerService
from syngrapha.application.interactors.auto_cat.cat_process import \
    AutoCategorizeInteractor
from syngrapha.infrastructure.ai_categorizer import AICategorizerServiceImpl


class AICategorizerDIProvider(Provider):
    """Provides everything related to AI categorizer."""

    service = provide(
        AICategorizerServiceImpl,
        provides=AICategorizerService,
        scope=Scope.REQUEST
    )
    categorizer = provide(AutoCategorizeInteractor, scope=Scope.REQUEST)
