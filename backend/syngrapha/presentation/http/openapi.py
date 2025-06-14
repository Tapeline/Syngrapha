from litestar.openapi import OpenAPIConfig
from litestar.openapi.plugins import SwaggerRenderPlugin
from litestar.openapi.spec import Components

from syngrapha.presentation.http.security import security_components

app_openapi_config = OpenAPIConfig(
    title="Syngrapha",
    description="Syngrapha API",
    version="1.0.0",
    render_plugins=[
        SwaggerRenderPlugin(),
    ],
    path="/docs",
    components=Components(
        security_schemes=security_components  # type: ignore
    )
)
