import logging
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Any, Dict, Optional, Union

import httpx
from tenacity import (
    after_log,
    before_log,
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from securebot_sdk.logger import configure_logging

logger = configure_logging()


@dataclass
class HttpClientConfig:
    """Configuration for HttpClient."""

    timeout_seconds: float = 30.0
    max_retries: int = 3
    min_retry_wait_seconds: float = 1.0
    max_retry_wait_seconds: float = 10.0
    pool_limits_max_connections: int = 100
    pool_limits_max_keepalive: int = 20
    connect_timeout_seconds: float = 10.0
    read_timeout_seconds: float = 30.0
    write_timeout_seconds: float = 30.0
    http2: bool = False  # Disabled by default to avoid dependency requirement


class HttpClient:
    """A  HTTP client with retries, timeouts, and connection pooling."""

    def __init__(self, config: Optional[HttpClientConfig] = None):
        self.config = config or HttpClientConfig()
        self._client = self._create_client()

    def _create_client(self) -> httpx.Client:
        """Create an httpx client with the configured settings."""
        return httpx.Client(
            timeout=httpx.Timeout(
                connect=self.config.connect_timeout_seconds,
                read=self.config.read_timeout_seconds,
                write=self.config.write_timeout_seconds,
                pool=self.config.timeout_seconds,
            ),
            limits=httpx.Limits(
                max_connections=self.config.pool_limits_max_connections,
                max_keepalive_connections=self.config.pool_limits_max_keepalive,
            ),
            http2=self.config.http2,
        )

    @retry(
        retry=retry_if_exception_type((httpx.NetworkError, httpx.TimeoutException)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        before=before_log(logger, logging.DEBUG),
        after=after_log(logger, logging.DEBUG),
    )
    def request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], bytes, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> httpx.Response:
        """
        Make an HTTP request with automatic retries and error handling.

        Args:
            method: HTTP method (GET, POST, etc.)
            url: Target URL
            params: Query parameters
            json: JSON body
            data: Form data or raw body
            headers: HTTP headers
            timeout: Optional timeout override

        Returns:
            httpx.Response object

        Raises:
            httpx.HTTPError: For HTTP-related errors
            Exception: For other unexpected errors
        """
        try:
            response = self._client.request(
                method=method,
                url=url,
                params=params,
                json=json,
                data=data,
                headers=headers,
                timeout=timeout or self.config.timeout_seconds,
            )
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            logger.error(
                "HTTP %s error for %s %s: %s",
                e.response.status_code,
                method,
                url,
                e.response.text,
            )
            raise
        except Exception as e:
            logger.error("Error making %s request to %s: %s", method, url, str(e))
            raise

    def get(self, url: str, **kwargs) -> httpx.Response:
        """Convenience method for GET requests."""
        return self.request("GET", url, **kwargs)

    def post(self, url: str, **kwargs) -> httpx.Response:
        """Convenience method for POST requests."""
        return self.request("POST", url, **kwargs)

    def put(self, url: str, **kwargs) -> httpx.Response:
        """Convenience method for PUT requests."""
        return self.request("PUT", url, **kwargs)

    def delete(self, url: str, **kwargs) -> httpx.Response:
        """Convenience method for DELETE requests."""
        return self.request("DELETE", url, **kwargs)

    def patch(self, url: str, **kwargs) -> httpx.Response:
        """Convenience method for PATCH requests."""
        return self.request("PATCH", url, **kwargs)

    def __enter__(self) -> "HttpClient":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Close the underlying HTTP client."""
        self._client.close()


class AsyncHttpClient:
    """Async version of the HTTP client."""

    def __init__(self, config: Optional[HttpClientConfig] = None):
        self.config = config or HttpClientConfig()
        self._client = self._create_client()

    def _create_client(self) -> httpx.AsyncClient:
        """Create an async httpx client with the configured settings."""
        return httpx.AsyncClient(
            timeout=httpx.Timeout(
                connect=self.config.connect_timeout_seconds,
                read=self.config.read_timeout_seconds,
                write=self.config.write_timeout_seconds,
                pool=self.config.timeout_seconds,
            ),
            limits=httpx.Limits(
                max_connections=self.config.pool_limits_max_connections,
                max_keepalive_connections=self.config.pool_limits_max_keepalive,
            ),
            http2=self.config.http2,
        )

    @retry(
        retry=retry_if_exception_type((httpx.NetworkError, httpx.TimeoutException)),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10),
        before=before_log(logger, logging.DEBUG),
        after=after_log(logger, logging.DEBUG),
    )
    async def request(
        self,
        method: str,
        url: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
        data: Optional[Union[Dict[str, Any], bytes, str]] = None,
        headers: Optional[Dict[str, str]] = None,
        timeout: Optional[float] = None,
    ) -> httpx.Response:
        """
        Make an async HTTP request with automatic retries and error handling.
        """
        try:
            response = await self._client.request(
                method=method,
                url=url,
                params=params,
                json=json,
                data=data,
                headers=headers,
                timeout=timeout or self.config.timeout_seconds,
            )
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as e:
            logger.error(
                "HTTP %s error for %s %s: %s",
                e.response.status_code,
                method,
                url,
                e.response.text,
            )
            raise
        except Exception as e:
            logger.error("Error making %s request to %s: %s", method, url, str(e))
            raise

    async def get(self, url: str, **kwargs) -> httpx.Response:
        """Convenience method for async GET requests."""
        return await self.request("GET", url, **kwargs)

    async def post(self, url: str, **kwargs) -> httpx.Response:
        """Convenience method for async POST requests."""
        return await self.request("POST", url, **kwargs)

    async def put(self, url: str, **kwargs) -> httpx.Response:
        """Convenience method for async PUT requests."""
        return await self.request("PUT", url, **kwargs)

    async def delete(self, url: str, **kwargs) -> httpx.Response:
        """Convenience method for async DELETE requests."""
        return await self.request("DELETE", url, **kwargs)

    async def patch(self, url: str, **kwargs) -> httpx.Response:
        """Convenience method for async PATCH requests."""
        return await self.request("PATCH", url, **kwargs)

    async def close(self):
        """Close the underlying async HTTP client."""
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncHttpClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()


@asynccontextmanager
async def get_async_client(config: Optional[HttpClientConfig] = None):
    """Context manager for getting an async HTTP client."""
    client = AsyncHttpClient(config)
    try:
        yield client
    finally:
        await client.close()


def get_client(config: Optional[HttpClientConfig] = None) -> HttpClient:
    """Get a synchronous HTTP client."""
    return HttpClient(config)
