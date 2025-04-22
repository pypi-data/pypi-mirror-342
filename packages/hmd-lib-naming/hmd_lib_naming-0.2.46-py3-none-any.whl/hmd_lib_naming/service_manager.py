import os
from typing import List, Dict, Callable

from boto3 import Session
from hmd_lang_naming.service import Service

import hmd_lib_naming
from hmd_cli_tools.hmd_cli_tools import get_secret
from hmd_graphql_client import BaseClient
from hmd_graphql_client.hmd_lambda_client import LambdaClient
from hmd_graphql_client.hmd_rest_client import RestClient
from hmd_lib_naming.hmd_lib_naming import HmdNamingClient
from hmd_schema_loader import DefaultLoader


class ServiceManager:
    def __init__(
        self,
        loaders: Dict[str, DefaultLoader],
        environment: str,
        service_names: List[str] = None,
        auth_token: str = None,
        expired_auth_token_callback: Callable = None,
        naming_instance_name: str = "ms-naming",
        naming_repo_class: str = "hmd-ms-naming",
        naming_environment: str = "admin",
        naming_did: str = "aaa",
        naming_region: str = "reg1",
    ):
        self.loaders: Dict[str, DefaultLoader] = loaders
        if not service_names:
            service_names = list(self.loaders.keys())
        else:
            for service_name in service_names:
                assert (
                    service_name in self.loaders
                ), f"Service name {service_name} in defined in loaders."

        self.service_names = service_names
        self.services: Dict[str, BaseClient] = {}
        self.environment = environment
        self.naming_service = None
        self.auth_token = auth_token
        self.expired_auth_token_callback = expired_auth_token_callback
        self.naming_instance_name = naming_instance_name
        self.naming_repo_class = naming_repo_class
        self.naming_environment = naming_environment
        self.naming_did = naming_did
        self.naming_region = naming_region

    def _get_naming_service(self):
        if not self.naming_service:
            naming_base_client = self._get_naming_service_client()
            self.naming_service = HmdNamingClient(naming_base_client)
        return self.naming_service

    def get_service(
        self, service_name: str, use_http_endpoint_by_default: bool = False
    ) -> BaseClient:
        service = self.services.get(service_name)
        if not service:
            service = self._get_base_service(service_name, use_http_endpoint_by_default)
            self.services[service_name] = service

        return service

    def _get_base_service(
        self, service_name: str, use_http_endpoint_by_default: bool = False
    ) -> BaseClient:
        loader = self.get_loaders()[service_name]
        if self.environment == "local":
            return RestClient(
                f"http://hmd_proxy/{service_name}/",
                loader,
                auth_token=self.auth_token,
                expired_auth_token_callback=self.expired_auth_token_callback,
            )

        service = Service(name=service_name)
        service_endpoints = self._get_naming_service().resolve_service(
            service, self.environment
        )
        if service_endpoints.arnEndpoint and not use_http_endpoint_by_default:
            return LambdaClient(
                service_endpoints.arnEndpoint,
                loader,
                auth_token=self.auth_token,
                expired_auth_token_callback=self.expired_auth_token_callback,
            )
        else:
            return RestClient(
                service_endpoints.httpEndpoint,
                loader,
                auth_token=self.auth_token,
                expired_auth_token_callback=self.expired_auth_token_callback,
            )

    def get_loaders(self) -> Dict[str, DefaultLoader]:
        return self.loaders

    def _get_naming_service_client(self):
        if self.environment == "local":
            naming_url = "http://hmd_gateway:8080/ms-naming/"
            auth_token = self.auth_token

            return RestClient(
                naming_url,
                hmd_lib_naming.hmd_lib_naming.get_default_loader(),
                auth_token=auth_token,
            )

        if self.environment != self.naming_environment:
            naming_url = f"https://{self.naming_instance_name}-{self.naming_did}-{self.naming_region}.{os.environ['HMD_CUSTOMER_CODE']}-{self.naming_environment}-neuronsphere.io"
            auth_token = self.auth_token

            return RestClient(
                naming_url,
                hmd_lib_naming.hmd_lib_naming.get_default_loader(),
                auth_token=auth_token,
                expired_auth_token_callback=self.expired_auth_token_callback,
            )
        return LambdaClient(
            f"{self.naming_instance_name}_{self.naming_repo_class}_{self.naming_did}_{self.naming_environment}_{self.naming_region}_{os.environ['HMD_CUSTOMER_CODE']}-lambda",
            hmd_lib_naming.hmd_lib_naming.get_default_loader(),
            {
                "account": (
                    get_secret(Session(), "organization-metadata", "admin_account")
                ),
                "role": "naming_role",
            },
        )
