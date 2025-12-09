"""
Regional endpoint management for Agora API.

This module provides area-based URL selection with automatic region cycling
and DNS-based domain selection for optimal connectivity.
"""

import enum
import socket
import threading
import time
import typing


class GatewayArea(enum.Enum):
    """Global regions where the Open API gateway endpoint is located."""

    US = "US"
    EU = "EU"
    APAC = "APAC"
    CN = "CN"


CHINESE_MAINLAND_DOMAIN = "sd-rtn.com"
OVERSEAS_DOMAIN = "agora.io"

GLOBAL_DOMAIN_PREFIX = "api"

US_WEST_REGION_PREFIX = "api-us-west-1"
US_EAST_REGION_PREFIX = "api-us-east-1"

AP_SOUTHEAST_REGION_PREFIX = "api-ap-southeast-1"
AP_NORTHEAST_REGION_PREFIX = "api-ap-northeast-1"

EU_WEST_REGION_PREFIX = "api-eu-west-1"
EU_CENTRAL_REGION_PREFIX = "api-eu-central-1"

CN_EAST_REGION_PREFIX = "api-cn-east-1"
CN_NORTH_REGION_PREFIX = "api-cn-north-1"


class _DomainConfig(typing.NamedTuple):
    """Configuration for a gateway area's domains."""

    region_prefixes: typing.List[str]
    domain_suffixes: typing.List[str]


REGION_DOMAIN_CONFIG: typing.Dict[GatewayArea, _DomainConfig] = {
    GatewayArea.US: _DomainConfig(
        region_prefixes=[US_WEST_REGION_PREFIX, US_EAST_REGION_PREFIX],
        domain_suffixes=[OVERSEAS_DOMAIN, CHINESE_MAINLAND_DOMAIN],
    ),
    GatewayArea.EU: _DomainConfig(
        region_prefixes=[EU_WEST_REGION_PREFIX, EU_CENTRAL_REGION_PREFIX],
        domain_suffixes=[OVERSEAS_DOMAIN, CHINESE_MAINLAND_DOMAIN],
    ),
    GatewayArea.APAC: _DomainConfig(
        region_prefixes=[AP_SOUTHEAST_REGION_PREFIX, AP_NORTHEAST_REGION_PREFIX],
        domain_suffixes=[OVERSEAS_DOMAIN, CHINESE_MAINLAND_DOMAIN],
    ),
    GatewayArea.CN: _DomainConfig(
        region_prefixes=[CN_EAST_REGION_PREFIX, CN_NORTH_REGION_PREFIX],
        domain_suffixes=[CHINESE_MAINLAND_DOMAIN, OVERSEAS_DOMAIN],
    ),
}

UPDATE_DURATION_SECONDS = 30.0


class RegionalEndpointPool:
    """
    Manages a pool of regional URLs with automatic cycling and domain selection.

    This class provides:
    - Area-based endpoint selection (US, EU, APAC, CN)
    - DNS-based domain selection for optimal connectivity
    - Region cycling for failover scenarios
    """

    def __init__(self, gateway_area: GatewayArea) -> None:
        """
        Initialize a regional endpoint pool for the specified area.

        Parameters
        ----------
        gateway_area : GatewayArea
            The geographic area for endpoint selection.

        Raises
        ------
        ValueError
            If the gateway_area is not a valid GatewayArea.
        """
        if gateway_area not in REGION_DOMAIN_CONFIG:
            raise ValueError(f"Invalid gateway area: {gateway_area}")

        config = REGION_DOMAIN_CONFIG[gateway_area]
        self._gateway_area = gateway_area
        self._domain_suffixes = list(config.domain_suffixes)
        self._current_domain = self._domain_suffixes[0]
        self._region_prefixes = list(config.region_prefixes)
        self._current_region_prefixes = list(self._region_prefixes)
        self._lock = threading.Lock()
        self._last_update: typing.Optional[float] = None

    def _domain_needs_update(self) -> bool:
        """Check if the domain selection needs to be refreshed."""
        if self._last_update is None:
            return True
        return (time.time() - self._last_update) > UPDATE_DURATION_SECONDS

    def _resolve_domain(self, domains: typing.List[str], region_prefix: str) -> typing.Optional[str]:
        """
        Resolve the best available domain using DNS lookup.

        Parameters
        ----------
        domains : List[str]
            List of domain suffixes to try.
        region_prefix : str
            The region prefix to use for DNS lookup.

        Returns
        -------
        Optional[str]
            The first domain that resolves successfully, or None if all fail.
        """
        for domain in domains:
            url = f"{region_prefix}.{domain}"
            try:
                socket.getaddrinfo(url, None)
                return domain
            except socket.gaierror:
                continue
        return None

    def select_best_domain(self) -> None:
        """
        Use DNS resolution to select the best available domain.

        This method performs DNS lookups to find the most responsive domain
        and updates the current domain selection accordingly.
        """
        if not self._domain_needs_update():
            return

        with self._lock:
            if not self._domain_needs_update():
                return

            domain = self._resolve_domain(
                self._domain_suffixes,
                self._current_region_prefixes[0],
            )
            if domain is not None:
                self._current_domain = domain
                self._last_update = time.time()

    def next_region(self) -> None:
        """
        Cycle to the next region prefix in the pool.

        This method is useful for failover scenarios where the current
        region is not responding.
        """
        with self._lock:
            self._current_region_prefixes = self._current_region_prefixes[1:]
            if len(self._current_region_prefixes) == 0:
                self._current_region_prefixes = list(self._region_prefixes)

    def get_current_url(self) -> str:
        """
        Get the current base URL based on the selected region and domain.

        Returns
        -------
        str
            The full base URL for API requests.
        """
        with self._lock:
            current_region = self._current_region_prefixes[0]
            current_domain = self._current_domain
            return f"https://{current_region}.{current_domain}"

    @property
    def gateway_area(self) -> GatewayArea:
        """The gateway area this pool is configured for."""
        return self._gateway_area
