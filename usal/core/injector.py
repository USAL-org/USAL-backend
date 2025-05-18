from re import compile
from types import ModuleType
from typing import Any

from fastapi import FastAPI
from fastapi.routing import APIRoute
from wireup import ServiceLifetime, initialize_container
from wireup.integration.util import is_view_using_container
from wireup.util import _find_objects_in_module  # type:ignore

from usal.core.config import AppConfig
from usal.core.container import container
from usal.util.config import load_config


class Registrant:
    def __init__(
        self, module: ModuleType, pattern: str = "*", qualifiers: dict[type, str] = {}
    ) -> None:
        self.module = module
        self.pattern = compile(pattern)
        self.qualifiers = qualifiers

    def _register(self, lifetime: ServiceLifetime) -> None:
        klass: type[Any]
        for klass in self._find_classes():
            container.register(
                klass, lifetime=lifetime, qualifier=self.qualifiers.get(klass, None)
            )

    def _abstract(self) -> None:
        klass: type[Any]
        for klass in self._find_classes():
            container.abstract(klass)

    def _find_classes(self) -> set[type]:
        return _find_objects_in_module(
            self.module,
            predicate=lambda obj: isinstance(obj, type),
            pattern=self.pattern,
        )


class Injector:
    @staticmethod
    def init(
        app: FastAPI,
        modules: list[ModuleType],
        interfaces: list[Registrant],
        factories: list[Registrant],
        singletons: list[Registrant],
    ) -> "Injector":
        return Injector(app, modules, interfaces, factories, singletons)

    def __init__(
        self,
        app: FastAPI,
        modules: list[ModuleType],
        interfaces: list[Registrant],
        factories: list[Registrant],
        singletons: list[Registrant],
    ) -> None:
        load_config()

        initialize_container(container, service_modules=modules)

        app_config = AppConfig.build()

        app.title = app_config.app_name
        app.version = app_config.app_version

        for registrant in interfaces:
            registrant._abstract()  # type: ignore

        for registrant in factories:
            registrant._register(ServiceLifetime.TRANSIENT)  # type: ignore

        for registrant in singletons:
            registrant._register(ServiceLifetime.SINGLETON)  # type: ignore

        for route in app.routes:
            if isinstance(route, APIRoute) and self._has_dependent_container(route):
                route.dependant.call = container.autowire(route.dependant.call)  # type: ignore

    def _has_dependent_container(self, route: APIRoute) -> bool | None:
        callable_dependent = route.dependant.call

        return callable_dependent and is_view_using_container(
            container, callable_dependent
        )
