from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.building_result import BuildingResult
from ...models.http_validation_error import HTTPValidationError
from ...types import Response


def _get_kwargs(
    building_id: int,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/v1.0/buildings/{building_id}/results",
    }

    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> BuildingResult | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = BuildingResult.from_dict(response.json())

        return response_200
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[BuildingResult | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    building_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[BuildingResult | HTTPValidationError]:
    """Get Building Result

     Return the modeled baseline and the results of intervention analysis.

    Args:
        building_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BuildingResult, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        building_id=building_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    building_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> BuildingResult | HTTPValidationError | None:
    """Get Building Result

     Return the modeled baseline and the results of intervention analysis.

    Args:
        building_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BuildingResult, HTTPValidationError]
    """

    return sync_detailed(
        building_id=building_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    building_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> Response[BuildingResult | HTTPValidationError]:
    """Get Building Result

     Return the modeled baseline and the results of intervention analysis.

    Args:
        building_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[BuildingResult, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        building_id=building_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    building_id: int,
    *,
    client: AuthenticatedClient | Client,
) -> BuildingResult | HTTPValidationError | None:
    """Get Building Result

     Return the modeled baseline and the results of intervention analysis.

    Args:
        building_id (int):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[BuildingResult, HTTPValidationError]
    """

    return (
        await asyncio_detailed(
            building_id=building_id,
            client=client,
        )
    ).parsed
