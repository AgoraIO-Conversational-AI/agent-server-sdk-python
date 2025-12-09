"""
Regional Agora clients with area-based URL selection.

This module provides wrapper clients that extend the base Agora clients
with support for regional endpoint selection.
"""

from __future__ import annotations

import typing

import httpx

from .area import GatewayArea, RegionalEndpointPool
from .client import Agora as BaseAgora
from .client import AsyncAgora as BaseAsyncAgora
from .environment import AgoraEnvironment


class RegionalAgora(BaseAgora):
    """
    Agora client with regional endpoint selection.

    This client extends the base Agora client with support for area-based
    URL selection, allowing you to connect to the optimal regional endpoint.

    Parameters
    ----------
    gateway_area : typing.Optional[GatewayArea]
        The geographic area for endpoint selection. If provided, the client
        will automatically select the appropriate regional endpoint.

    endpoint_pool : typing.Optional[RegionalEndpointPool]
        A pre-configured endpoint pool. Use this if you want to manage
        the pool lifecycle yourself or share a pool across multiple clients.

    base_url : typing.Optional[str]
        The base url to use for requests from the client. If provided,
        this takes precedence over gateway_area and endpoint_pool.

    environment : AgoraEnvironment
        The environment to use for requests from the client.
        Defaults to AgoraEnvironment.DEFAULT

    username : typing.Union[str, typing.Callable[[], str]]
        The username for authentication.

    password : typing.Union[str, typing.Callable[[], str]]
        The password for authentication.

    headers : typing.Optional[typing.Dict[str, str]]
        Additional headers to send with every request.

    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not.

    httpx_client : typing.Optional[httpx.Client]
        The httpx client to use for making requests.

    Examples
    --------
    from agoraio import Agora, GatewayArea

    client = Agora(
        gateway_area=GatewayArea.US,
        username="YOUR_USERNAME",
        password="YOUR_PASSWORD",
    )
    """

    def __init__(
        self,
        *,
        gateway_area: typing.Optional[GatewayArea] = None,
        endpoint_pool: typing.Optional[RegionalEndpointPool] = None,
        base_url: typing.Optional[str] = None,
        environment: AgoraEnvironment = AgoraEnvironment.DEFAULT,
        username: typing.Union[str, typing.Callable[[], str]],
        password: typing.Union[str, typing.Callable[[], str]],
        headers: typing.Optional[typing.Dict[str, str]] = None,
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.Client] = None,
    ):
        self._endpoint_pool: typing.Optional[RegionalEndpointPool] = None

        if base_url is not None:
            resolved_base_url = base_url
        elif endpoint_pool is not None:
            self._endpoint_pool = endpoint_pool
            self._endpoint_pool.select_best_domain()
            resolved_base_url = self._endpoint_pool.get_current_url()
        elif gateway_area is not None:
            self._endpoint_pool = RegionalEndpointPool(gateway_area)
            self._endpoint_pool.select_best_domain()
            resolved_base_url = self._endpoint_pool.get_current_url()
        else:
            resolved_base_url = None

        super().__init__(
            base_url=resolved_base_url,
            environment=environment,
            username=username,
            password=password,
            headers=headers,
            timeout=timeout,
            follow_redirects=follow_redirects,
            httpx_client=httpx_client,
        )

    @property
    def endpoint_pool(self) -> typing.Optional[RegionalEndpointPool]:
        """The endpoint pool used by this client, if any."""
        return self._endpoint_pool


class AsyncRegionalAgora(BaseAsyncAgora):
    """
    Async Agora client with regional endpoint selection.

    This client extends the base AsyncAgora client with support for area-based
    URL selection, allowing you to connect to the optimal regional endpoint.

    Parameters
    ----------
    gateway_area : typing.Optional[GatewayArea]
        The geographic area for endpoint selection. If provided, the client
        will automatically select the appropriate regional endpoint.

    endpoint_pool : typing.Optional[RegionalEndpointPool]
        A pre-configured endpoint pool. Use this if you want to manage
        the pool lifecycle yourself or share a pool across multiple clients.

    base_url : typing.Optional[str]
        The base url to use for requests from the client. If provided,
        this takes precedence over gateway_area and endpoint_pool.

    environment : AgoraEnvironment
        The environment to use for requests from the client.
        Defaults to AgoraEnvironment.DEFAULT

    username : typing.Union[str, typing.Callable[[], str]]
        The username for authentication.

    password : typing.Union[str, typing.Callable[[], str]]
        The password for authentication.

    headers : typing.Optional[typing.Dict[str, str]]
        Additional headers to send with every request.

    timeout : typing.Optional[float]
        The timeout to be used, in seconds, for requests.

    follow_redirects : typing.Optional[bool]
        Whether the default httpx client follows redirects or not.

    httpx_client : typing.Optional[httpx.AsyncClient]
        The httpx client to use for making requests.

    Examples
    --------
    from agoraio import AsyncAgora, GatewayArea

    client = AsyncAgora(
        gateway_area=GatewayArea.US,
        username="YOUR_USERNAME",
        password="YOUR_PASSWORD",
    )
    """

    def __init__(
        self,
        *,
        gateway_area: typing.Optional[GatewayArea] = None,
        endpoint_pool: typing.Optional[RegionalEndpointPool] = None,
        base_url: typing.Optional[str] = None,
        environment: AgoraEnvironment = AgoraEnvironment.DEFAULT,
        username: typing.Union[str, typing.Callable[[], str]],
        password: typing.Union[str, typing.Callable[[], str]],
        headers: typing.Optional[typing.Dict[str, str]] = None,
        timeout: typing.Optional[float] = None,
        follow_redirects: typing.Optional[bool] = True,
        httpx_client: typing.Optional[httpx.AsyncClient] = None,
    ):
        self._endpoint_pool: typing.Optional[RegionalEndpointPool] = None

        if base_url is not None:
            resolved_base_url = base_url
        elif endpoint_pool is not None:
            self._endpoint_pool = endpoint_pool
            self._endpoint_pool.select_best_domain()
            resolved_base_url = self._endpoint_pool.get_current_url()
        elif gateway_area is not None:
            self._endpoint_pool = RegionalEndpointPool(gateway_area)
            self._endpoint_pool.select_best_domain()
            resolved_base_url = self._endpoint_pool.get_current_url()
        else:
            resolved_base_url = None

        super().__init__(
            base_url=resolved_base_url,
            environment=environment,
            username=username,
            password=password,
            headers=headers,
            timeout=timeout,
            follow_redirects=follow_redirects,
            httpx_client=httpx_client,
        )

    @property
    def endpoint_pool(self) -> typing.Optional[RegionalEndpointPool]:
        """The endpoint pool used by this client, if any."""
        return self._endpoint_pool
