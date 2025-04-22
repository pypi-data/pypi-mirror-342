import importlib
import os
import zipimport
from importlib import import_module
from typing import Callable

from hmd_lang_naming.service import Service

from hmd_graphql_client.hmd_base_client import BaseClient
from hmd_graphql_client.hmd_rest_client import RestClient
from hmd_meta_types import Entity
from hmd_schema_loader import DefaultLoader


def get_default_loader():
    package_path = "schemas"

    package_path = os.path.normpath(package_path).rstrip(os.path.sep)
    package_name = "hmd_lib_naming"

    # Make sure the package exists. This also makes namespace
    # packages work, otherwise get_loader returns None.
    import_module(package_name)
    spec = importlib.util.find_spec(package_name)
    assert spec is not None, "An import spec was not found for the package."
    loader = spec.loader
    assert loader is not None, "A loader was not found for the package."
    _archive = None
    schema_root = None

    if isinstance(loader, zipimport.zipimporter):
        _archive = loader.archive
        pkgdir = next(iter(spec.submodule_search_locations))  # type: ignore
        schema_root = os.path.join(pkgdir, package_path)
    elif spec.submodule_search_locations:
        # This will be one element for regular packages and multiple
        # for namespace packages.
        for root in spec.submodule_search_locations:
            root = os.path.join(root, package_path)

            if os.path.isdir(root):
                schema_root = root
                break

    if schema_root is None:
        raise ValueError(
            f"The {package_name!r} package was not installed in a"
            " way that PackageLoader understands."
        )

    return DefaultLoader(schema_root)


class HmdNamingClient:
    def __init__(
        self,
        base_client: BaseClient = None,
        base_url: str = None,
        api_key: str = None,
        auth_token: str = None,
        expired_auth_token_callback: Callable = None,
    ) -> None:
        if base_client is not None:
            self.client = base_client
        elif base_url is not None:
            self.client = RestClient(
                base_url,
                get_default_loader(),
                api_key,
                auth_token,
                expired_auth_token_callback=expired_auth_token_callback,
            )
        else:
            raise Exception("Must provide either base_url or base_client")

    def register_service(self, service: Service, environment: str) -> Service:
        svc = self.client.invoke_custom_operation(
            f"service/{service.name}/{environment}", service.serialize(), "PUT"
        )

        return Entity.deserialize(Service, svc)

    def resolve_service(self, service: Service, environment: str) -> Service:
        svc = self.client.invoke_custom_operation(
            f"resolve/{service.name}", {"environment": environment}, "POST"
        )

        return Entity.deserialize(Service, svc)
