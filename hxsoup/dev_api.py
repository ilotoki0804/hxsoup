# ruff: noqa: UP007, UP006 Use httpx's convention.
from __future__ import annotations

import typing
from contextlib import contextmanager
from functools import lru_cache

from httpx._types import (
    AuthTypes,
    CertTypes,
    CookieTypes,
    HeaderTypes,
    ProxiesTypes,
    ProxyTypes,
    QueryParamTypes,
    RequestContent,
    RequestData,
    RequestFiles,
    TimeoutTypes,
    URLTypes,
    VerifyTypes,
)

from .client import DEFAULT_TIMEOUT_CONFIG, DEV_DEFAULT_TIMEOUT_CONFIG
from .client import DevClient as Client
from .souptools import Parsers, SoupedResponse
from .utils import freeze_dict_and_list


def request(
    method: str,
    url: URLTypes,
    *,
    params: typing.Optional[QueryParamTypes] = None,
    content: typing.Optional[RequestContent] = None,
    data: typing.Optional[RequestData] = None,
    files: typing.Optional[RequestFiles] = None,
    json: typing.Optional[typing.Any] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxy: typing.Optional[ProxyTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    timeout: TimeoutTypes = DEV_DEFAULT_TIMEOUT_CONFIG,
    follow_redirects: bool = True,  # changed
    verify: VerifyTypes = True,
    cert: typing.Optional[CertTypes] = None,
    trust_env: bool = True,
    attempts: int | None = None,
    raise_for_status: bool | None = None,
    parser: Parsers | None = None,
    no_empty_result: bool | None = None,
) -> SoupedResponse:
    """
    Sends an HTTP request.

    **Parameters:**

    * **method** - HTTP method for the new `Request` object: `GET`, `OPTIONS`,
    `HEAD`, `POST`, `PUT`, `PATCH`, or `DELETE`.
    * **url** - URL for the new `Request` object.
    * **params** - *(optional)* Query parameters to include in the URL, as a
    string, dictionary, or sequence of two-tuples.
    * **content** - *(optional)* Binary content to include in the body of the
    request, as bytes or a byte iterator.
    * **data** - *(optional)* Form data to include in the body of the request,
    as a dictionary.
    * **files** - *(optional)* A dictionary of upload files to include in the
    body of the request.
    * **json** - *(optional)* A JSON serializable object to include in the body
    of the request.
    * **headers** - *(optional)* Dictionary of HTTP headers to include in the
    request.
    * **cookies** - *(optional)* Dictionary of Cookie items to include in the
    request.
    * **auth** - *(optional)* An authentication class to use when sending the
    request.
    * **proxy** - *(optional)* A proxy URL where all the traffic should be routed.
    * **proxies** - *(optional)* A dictionary mapping proxy keys to proxy URLs.
    * **timeout** - *(optional)* The timeout configuration to use when sending
    the request.
    * **follow_redirects** - *(optional)* Enables or disables HTTP redirects.
    * **verify** - *(optional)* SSL certificates (a.k.a CA bundle) used to
    verify the identity of requested hosts. Either `True` (default CA bundle),
    a path to an SSL certificate file, an `ssl.SSLContext`, or `False`
    (which will disable verification).
    * **cert** - *(optional)* An SSL certificate used by the requested host
    to authenticate the client. Either a path to an SSL certificate file, or
    two-tuple of (certificate file, key file), or a three-tuple of (certificate
    file, key file, password).
    * **trust_env** - *(optional)* Enables or disables usage of environment
    variables for configuration.

    **Returns:** `Response`

    Usage:

    ```
    >>> import httpx
    >>> response = httpx.request('GET', 'https://httpbin.org/get')
    >>> response
    <Response [200 OK]>
    ```
    """
    with Client(
        cookies=cookies,
        proxy=proxy,
        proxies=proxies,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
    ) as client:
        return client.request(
            method=method,
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            auth=auth,
            follow_redirects=follow_redirects,
            attempts=attempts,
            raise_for_status=raise_for_status,
            parser=parser,
            no_empty_result=no_empty_result,
        )


@contextmanager
def stream(
    method: str,
    url: URLTypes,
    *,
    params: typing.Optional[QueryParamTypes] = None,
    content: typing.Optional[RequestContent] = None,
    data: typing.Optional[RequestData] = None,
    files: typing.Optional[RequestFiles] = None,
    json: typing.Optional[typing.Any] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxy: typing.Optional[ProxyTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    follow_redirects: bool = True,  # changed
    verify: VerifyTypes = True,
    cert: typing.Optional[CertTypes] = None,
    trust_env: bool = True,
    attempts: int | None = None,
    raise_for_status: bool | None = None,
    parser: Parsers | None = None,
    no_empty_result: bool | None = None,
) -> typing.Iterator[SoupedResponse]:
    """
    Alternative to `httpx.request()` that streams the response body
    instead of loading it into memory at once.

    **Parameters**: See `httpx.request`.

    See also: [Streaming Responses][0]

    [0]: /quickstart#streaming-responses
    """
    with Client(
        cookies=cookies,
        proxy=proxy,
        proxies=proxies,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
    ) as client:
        with client.stream(
            method=method,
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            auth=auth,
            follow_redirects=follow_redirects,
            attempts=attempts,
            raise_for_status=raise_for_status,
            parser=parser,
            no_empty_result=no_empty_result,
        ) as response:
            yield response


def get(
    url: URLTypes,
    *,
    params: typing.Optional[QueryParamTypes] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxy: typing.Optional[ProxyTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    follow_redirects: bool = True,  # changed
    cert: typing.Optional[CertTypes] = None,
    verify: VerifyTypes = True,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
    attempts: int | None = None,
    raise_for_status: bool | None = None,
    parser: Parsers | None = None,
    no_empty_result: bool | None = None,
) -> SoupedResponse:
    """
    Sends a `GET` request.

    **Parameters**: See `httpx.request`.

    Note that the `data`, `files`, `json` and `content` parameters are not available
    on this function, as `GET` requests should not include a request body.
    """
    return request(
        "GET",
        url,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxy=proxy,
        proxies=proxies,
        follow_redirects=follow_redirects,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
        attempts=attempts,
        raise_for_status=raise_for_status,
        parser=parser,
        no_empty_result=no_empty_result,
    )


def options(
    url: URLTypes,
    *,
    params: typing.Optional[QueryParamTypes] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxy: typing.Optional[ProxyTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    follow_redirects: bool = True,  # changed
    cert: typing.Optional[CertTypes] = None,
    verify: VerifyTypes = True,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
    attempts: int | None = None,
    raise_for_status: bool | None = None,
    parser: Parsers | None = None,
    no_empty_result: bool | None = None,
) -> SoupedResponse:
    """
    Sends an `OPTIONS` request.

    **Parameters**: See `httpx.request`.

    Note that the `data`, `files`, `json` and `content` parameters are not available
    on this function, as `OPTIONS` requests should not include a request body.
    """
    return request(
        "OPTIONS",
        url,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxy=proxy,
        proxies=proxies,
        follow_redirects=follow_redirects,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
        attempts=attempts,
        raise_for_status=raise_for_status,
        parser=parser,
        no_empty_result=no_empty_result,
    )


def head(
    url: URLTypes,
    *,
    params: typing.Optional[QueryParamTypes] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxy: typing.Optional[ProxyTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    follow_redirects: bool = True,  # changed
    cert: typing.Optional[CertTypes] = None,
    verify: VerifyTypes = True,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
    attempts: int | None = None,
    raise_for_status: bool | None = None,
    parser: Parsers | None = None,
    no_empty_result: bool | None = None,
) -> SoupedResponse:
    """
    Sends a `HEAD` request.

    **Parameters**: See `httpx.request`.

    Note that the `data`, `files`, `json` and `content` parameters are not available
    on this function, as `HEAD` requests should not include a request body.
    """
    return request(
        "HEAD",
        url,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxy=proxy,
        proxies=proxies,
        follow_redirects=follow_redirects,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
        attempts=attempts,
        raise_for_status=raise_for_status,
        parser=parser,
        no_empty_result=no_empty_result,
    )


def post(
    url: URLTypes,
    *,
    content: typing.Optional[RequestContent] = None,
    data: typing.Optional[RequestData] = None,
    files: typing.Optional[RequestFiles] = None,
    json: typing.Optional[typing.Any] = None,
    params: typing.Optional[QueryParamTypes] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxy: typing.Optional[ProxyTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    follow_redirects: bool = True,  # changed
    cert: typing.Optional[CertTypes] = None,
    verify: VerifyTypes = True,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
    attempts: int | None = None,
    raise_for_status: bool | None = None,
    parser: Parsers | None = None,
    no_empty_result: bool | None = None,
) -> SoupedResponse:
    """
    Sends a `POST` request.

    **Parameters**: See `httpx.request`.
    """
    return request(
        "POST",
        url,
        content=content,
        data=data,
        files=files,
        json=json,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxy=proxy,
        proxies=proxies,
        follow_redirects=follow_redirects,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
        attempts=attempts,
        raise_for_status=raise_for_status,
        parser=parser,
        no_empty_result=no_empty_result,
    )


def put(
    url: URLTypes,
    *,
    content: typing.Optional[RequestContent] = None,
    data: typing.Optional[RequestData] = None,
    files: typing.Optional[RequestFiles] = None,
    json: typing.Optional[typing.Any] = None,
    params: typing.Optional[QueryParamTypes] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxy: typing.Optional[ProxyTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    follow_redirects: bool = True,  # changed
    cert: typing.Optional[CertTypes] = None,
    verify: VerifyTypes = True,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
    attempts: int | None = None,
    raise_for_status: bool | None = None,
    parser: Parsers | None = None,
    no_empty_result: bool | None = None,
) -> SoupedResponse:
    """
    Sends a `PUT` request.

    **Parameters**: See `httpx.request`.
    """
    return request(
        "PUT",
        url,
        content=content,
        data=data,
        files=files,
        json=json,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxy=proxy,
        proxies=proxies,
        follow_redirects=follow_redirects,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
        attempts=attempts,
        raise_for_status=raise_for_status,
        parser=parser,
        no_empty_result=no_empty_result,
    )


def patch(
    url: URLTypes,
    *,
    content: typing.Optional[RequestContent] = None,
    data: typing.Optional[RequestData] = None,
    files: typing.Optional[RequestFiles] = None,
    json: typing.Optional[typing.Any] = None,
    params: typing.Optional[QueryParamTypes] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxy: typing.Optional[ProxyTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    follow_redirects: bool = True,  # changed
    cert: typing.Optional[CertTypes] = None,
    verify: VerifyTypes = True,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
    attempts: int | None = None,
    raise_for_status: bool | None = None,
    parser: Parsers | None = None,
    no_empty_result: bool | None = None,
) -> SoupedResponse:
    """
    Sends a `PATCH` request.

    **Parameters**: See `httpx.request`.
    """
    return request(
        "PATCH",
        url,
        content=content,
        data=data,
        files=files,
        json=json,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxy=proxy,
        proxies=proxies,
        follow_redirects=follow_redirects,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
        attempts=attempts,
        raise_for_status=raise_for_status,
        parser=parser,
        no_empty_result=no_empty_result,
    )


def delete(
    url: URLTypes,
    *,
    params: typing.Optional[QueryParamTypes] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxy: typing.Optional[ProxyTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    follow_redirects: bool = True,  # changed
    cert: typing.Optional[CertTypes] = None,
    verify: VerifyTypes = True,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
    attempts: int | None = None,
    raise_for_status: bool | None = None,
    parser: Parsers | None = None,
    no_empty_result: bool | None = None,
) -> SoupedResponse:
    """
    Sends a `DELETE` request.

    **Parameters**: See `httpx.request`.

    Note that the `data`, `files`, `json` and `content` parameters are not available
    on this function, as `DELETE` requests should not include a request body.
    """
    return request(
        "DELETE",
        url,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxy=proxy,
        proxies=proxies,
        follow_redirects=follow_redirects,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
        attempts=attempts,
        raise_for_status=raise_for_status,
        parser=parser,
        no_empty_result=no_empty_result,
    )


@freeze_dict_and_list()
@lru_cache
def crequest(
    method: str,
    url: URLTypes,
    *,
    params: typing.Optional[QueryParamTypes] = None,
    content: typing.Optional[RequestContent] = None,
    data: typing.Optional[RequestData] = None,
    files: typing.Optional[RequestFiles] = None,
    json: typing.Optional[typing.Any] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxy: typing.Optional[ProxyTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    timeout: TimeoutTypes = DEV_DEFAULT_TIMEOUT_CONFIG,
    follow_redirects: bool = True,  # changed
    verify: VerifyTypes = True,
    cert: typing.Optional[CertTypes] = None,
    trust_env: bool = True,
    attempts: int | None = None,
    raise_for_status: bool | None = None,
    parser: Parsers | None = None,
    no_empty_result: bool | None = None,
) -> SoupedResponse:
    """
    Sends an HTTP request.

    **Parameters:**

    * **method** - HTTP method for the new `Request` object: `GET`, `OPTIONS`,
    `HEAD`, `POST`, `PUT`, `PATCH`, or `DELETE`.
    * **url** - URL for the new `Request` object.
    * **params** - *(optional)* Query parameters to include in the URL, as a
    string, dictionary, or sequence of two-tuples.
    * **content** - *(optional)* Binary content to include in the body of the
    request, as bytes or a byte iterator.
    * **data** - *(optional)* Form data to include in the body of the request,
    as a dictionary.
    * **files** - *(optional)* A dictionary of upload files to include in the
    body of the request.
    * **json** - *(optional)* A JSON serializable object to include in the body
    of the request.
    * **headers** - *(optional)* Dictionary of HTTP headers to include in the
    request.
    * **cookies** - *(optional)* Dictionary of Cookie items to include in the
    request.
    * **auth** - *(optional)* An authentication class to use when sending the
    request.
    * **proxy** - *(optional)* A proxy URL where all the traffic should be routed.
    * **proxies** - *(optional)* A dictionary mapping proxy keys to proxy URLs.
    * **timeout** - *(optional)* The timeout configuration to use when sending
    the request.
    * **follow_redirects** - *(optional)* Enables or disables HTTP redirects.
    * **verify** - *(optional)* SSL certificates (a.k.a CA bundle) used to
    verify the identity of requested hosts. Either `True` (default CA bundle),
    a path to an SSL certificate file, an `ssl.SSLContext`, or `False`
    (which will disable verification).
    * **cert** - *(optional)* An SSL certificate used by the requested host
    to authenticate the client. Either a path to an SSL certificate file, or
    two-tuple of (certificate file, key file), or a three-tuple of (certificate
    file, key file, password).
    * **trust_env** - *(optional)* Enables or disables usage of environment
    variables for configuration.

    **Returns:** `Response`

    Usage:

    ```
    >>> import httpx
    >>> response = httpx.request('GET', 'https://httpbin.org/get')
    >>> response
    <Response [200 OK]>
    ```
    """
    with Client(
        cookies=cookies,
        proxy=proxy,
        proxies=proxies,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
    ) as client:
        return client.request(
            method=method,
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            auth=auth,
            follow_redirects=follow_redirects,
            attempts=attempts,
            raise_for_status=raise_for_status,
            parser=parser,
            no_empty_result=no_empty_result,
        )


def cget(
    url: URLTypes,
    *,
    params: typing.Optional[QueryParamTypes] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxy: typing.Optional[ProxyTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    follow_redirects: bool = True,  # changed
    cert: typing.Optional[CertTypes] = None,
    verify: VerifyTypes = True,
    timeout: TimeoutTypes = DEV_DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
    attempts: int | None = None,
    raise_for_status: bool | None = None,
    parser: Parsers | None = None,
    no_empty_result: bool | None = None,
) -> SoupedResponse:
    """
    Sends a `GET` request.

    **Parameters**: See `httpx.request`.

    Note that the `data`, `files`, `json` and `content` parameters are not available
    on this function, as `GET` requests should not include a request body.
    """
    return crequest(
        "GET",
        url,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxy=proxy,
        proxies=proxies,
        follow_redirects=follow_redirects,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
        attempts=attempts,
        raise_for_status=raise_for_status,
        parser=parser,
        no_empty_result=no_empty_result,
    )


def coptions(
    url: URLTypes,
    *,
    params: typing.Optional[QueryParamTypes] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxy: typing.Optional[ProxyTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    follow_redirects: bool = True,  # changed
    cert: typing.Optional[CertTypes] = None,
    verify: VerifyTypes = True,
    timeout: TimeoutTypes = DEV_DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
    attempts: int | None = None,
    raise_for_status: bool | None = None,
    parser: Parsers | None = None,
    no_empty_result: bool | None = None,
) -> SoupedResponse:
    """
    Sends an `OPTIONS` request.

    **Parameters**: See `httpx.request`.

    Note that the `data`, `files`, `json` and `content` parameters are not available
    on this function, as `OPTIONS` requests should not include a request body.
    """
    return crequest(
        "OPTIONS",
        url,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxy=proxy,
        proxies=proxies,
        follow_redirects=follow_redirects,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
        attempts=attempts,
        raise_for_status=raise_for_status,
        parser=parser,
        no_empty_result=no_empty_result,
    )


def chead(
    url: URLTypes,
    *,
    params: typing.Optional[QueryParamTypes] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxy: typing.Optional[ProxyTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    follow_redirects: bool = True,  # changed
    cert: typing.Optional[CertTypes] = None,
    verify: VerifyTypes = True,
    timeout: TimeoutTypes = DEV_DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
    attempts: int | None = None,
    raise_for_status: bool | None = None,
    parser: Parsers | None = None,
    no_empty_result: bool | None = None,
) -> SoupedResponse:
    """
    Sends a `HEAD` request.

    **Parameters**: See `httpx.request`.

    Note that the `data`, `files`, `json` and `content` parameters are not available
    on this function, as `HEAD` requests should not include a request body.
    """
    return crequest(
        "HEAD",
        url,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxy=proxy,
        proxies=proxies,
        follow_redirects=follow_redirects,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
        attempts=attempts,
        raise_for_status=raise_for_status,
        parser=parser,
        no_empty_result=no_empty_result,
    )


def cpost(
    url: URLTypes,
    *,
    content: typing.Optional[RequestContent] = None,
    data: typing.Optional[RequestData] = None,
    files: typing.Optional[RequestFiles] = None,
    json: typing.Optional[typing.Any] = None,
    params: typing.Optional[QueryParamTypes] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxy: typing.Optional[ProxyTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    follow_redirects: bool = True,  # changed
    cert: typing.Optional[CertTypes] = None,
    verify: VerifyTypes = True,
    timeout: TimeoutTypes = DEV_DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
    attempts: int | None = None,
    raise_for_status: bool | None = None,
    parser: Parsers | None = None,
    no_empty_result: bool | None = None,
) -> SoupedResponse:
    """
    Sends a `POST` request.

    **Parameters**: See `httpx.request`.
    """
    return crequest(
        "POST",
        url,
        content=content,
        data=data,
        files=files,
        json=json,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxy=proxy,
        proxies=proxies,
        follow_redirects=follow_redirects,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
        attempts=attempts,
        raise_for_status=raise_for_status,
        parser=parser,
        no_empty_result=no_empty_result,
    )


def cput(
    url: URLTypes,
    *,
    content: typing.Optional[RequestContent] = None,
    data: typing.Optional[RequestData] = None,
    files: typing.Optional[RequestFiles] = None,
    json: typing.Optional[typing.Any] = None,
    params: typing.Optional[QueryParamTypes] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxy: typing.Optional[ProxyTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    follow_redirects: bool = True,  # changed
    cert: typing.Optional[CertTypes] = None,
    verify: VerifyTypes = True,
    timeout: TimeoutTypes = DEV_DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
    attempts: int | None = None,
    raise_for_status: bool | None = None,
    parser: Parsers | None = None,
    no_empty_result: bool | None = None,
) -> SoupedResponse:
    """
    Sends a `PUT` request.

    **Parameters**: See `httpx.request`.
    """
    return crequest(
        "PUT",
        url,
        content=content,
        data=data,
        files=files,
        json=json,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxy=proxy,
        proxies=proxies,
        follow_redirects=follow_redirects,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
        attempts=attempts,
        raise_for_status=raise_for_status,
        parser=parser,
        no_empty_result=no_empty_result,
    )


def cpatch(
    url: URLTypes,
    *,
    content: typing.Optional[RequestContent] = None,
    data: typing.Optional[RequestData] = None,
    files: typing.Optional[RequestFiles] = None,
    json: typing.Optional[typing.Any] = None,
    params: typing.Optional[QueryParamTypes] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxy: typing.Optional[ProxyTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    follow_redirects: bool = True,  # changed
    cert: typing.Optional[CertTypes] = None,
    verify: VerifyTypes = True,
    timeout: TimeoutTypes = DEV_DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
    attempts: int | None = None,
    raise_for_status: bool | None = None,
    parser: Parsers | None = None,
    no_empty_result: bool | None = None,
) -> SoupedResponse:
    """
    Sends a `PATCH` request.

    **Parameters**: See `httpx.request`.
    """
    return crequest(
        "PATCH",
        url,
        content=content,
        data=data,
        files=files,
        json=json,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxy=proxy,
        proxies=proxies,
        follow_redirects=follow_redirects,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
        attempts=attempts,
        raise_for_status=raise_for_status,
        parser=parser,
        no_empty_result=no_empty_result,
    )


def cdelete(
    url: URLTypes,
    *,
    params: typing.Optional[QueryParamTypes] = None,
    headers: typing.Optional[HeaderTypes] = None,
    cookies: typing.Optional[CookieTypes] = None,
    auth: typing.Optional[AuthTypes] = None,
    proxy: typing.Optional[ProxyTypes] = None,
    proxies: typing.Optional[ProxiesTypes] = None,
    follow_redirects: bool = True,  # changed
    cert: typing.Optional[CertTypes] = None,
    verify: VerifyTypes = True,
    timeout: TimeoutTypes = DEV_DEFAULT_TIMEOUT_CONFIG,
    trust_env: bool = True,
    attempts: int | None = None,
    raise_for_status: bool | None = None,
    parser: Parsers | None = None,
    no_empty_result: bool | None = None,
) -> SoupedResponse:
    """
    Sends a `DELETE` request.

    **Parameters**: See `httpx.request`.

    Note that the `data`, `files`, `json` and `content` parameters are not available
    on this function, as `DELETE` requests should not include a request body.
    """
    return crequest(
        "DELETE",
        url,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        proxy=proxy,
        proxies=proxies,
        follow_redirects=follow_redirects,
        cert=cert,
        verify=verify,
        timeout=timeout,
        trust_env=trust_env,
        attempts=attempts,
        raise_for_status=raise_for_status,
        parser=parser,
        no_empty_result=no_empty_result,
    )
