from dependency.core.declaration import Component, Provider
from dependency.core.declaration.component import ABCComponent

def dep_in_layers(dep: ABCComponent, layers: list[list[Provider]]) -> bool:
    return any(
        issubclass(res.provided_cls, dep.base_cls)
        for layer in layers
        for res in layer
    )

def provider_is_resolved(provider: Provider, resolved_layers: list[list[Provider]]) -> bool:
    dependencies = provider.imports
    return all(
        dep_in_layers(dep, resolved_layers)
        for dep in dependencies
    )

def provider_unresolved(provider: Provider, resolved_layers: list[list[Provider]]) -> list[Component]:
    dependencies = provider.imports
    return [
        dep
        for dep in dependencies
        if not dep_in_layers(dep, resolved_layers)
    ]