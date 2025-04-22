import logging
from dependency.core.exceptions import DependencyError
from dependency.core.declaration import Component
from dependency.core.declaration.provider import Provider
from dependency.core.resolver.utils import provider_unresolved
logger = logging.getLogger("DependencyLoader")

def provider_detect_error(
        provider: Provider,
        unresolved_providers: list[Provider],
        resolved_layers: list[list[Provider]]
    ) -> tuple[list[Component], list[Component]]:
    deps_circular: list[Component] = []
    deps_missing: list[Component] = []

    for dep in provider_unresolved(provider, resolved_layers):
        # TODO: Check for circular dependencies
        deps_missing.append(dep)

    logger.error(f"Provider {provider} has unresolved dependencies: {deps_missing}")
    return deps_circular, deps_missing

def raise_dependency_error(providers: list[Provider], resolved_layers: list[list[Provider]]) -> None:
    for provider in providers:
        provider_detect_error(provider, providers, resolved_layers)
    
    raise DependencyError("Dependencies cannot be resolved")