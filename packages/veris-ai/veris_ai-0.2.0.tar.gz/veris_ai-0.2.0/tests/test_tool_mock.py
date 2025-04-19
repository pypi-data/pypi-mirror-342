import os
from typing import Any, Union
from unittest.mock import AsyncMock, Mock, patch

import httpx
import pytest

from veris_ai import veris


@pytest.fixture
def tool_mock():
    return veris


# Test type conversion
@pytest.mark.parametrize(
    "value,target_type,expected",
    [
        ("42", int, 42),
        (42, str, "42"),
        ("3.14", float, 3.14),
        ("true", bool, True),
        ([1, 2, 3], list[int], [1, 2, 3]),
        (["1", "2"], list[int], [1, 2]),
        ({"a": 1}, dict[str, int], {"a": 1}),
        ("42", Union[int, str], 42),
        ("abc", Union[int, str], "abc"),
    ],
)
def test_convert_to_type(tool_mock, value, target_type, expected):
    result = tool_mock._convert_to_type(value, target_type)
    assert result == expected
    assert isinstance(result, type(expected))


def test_convert_to_type_invalid(tool_mock):
    with pytest.raises(ValueError):
        tool_mock._convert_to_type("not a list", list[int])


def test_convert_to_type_dict_invalid(tool_mock):
    with pytest.raises(ValueError, match="Expected dict but got <class 'str'>"):
        tool_mock._convert_to_type("not a dict", dict[str, int])


def test_convert_to_type_union_all_fail(tool_mock):
    with pytest.raises(ValueError, match="Could not convert abc to any of the union types"):
        tool_mock._convert_to_type("abc", Union[int, float])


def test_convert_to_type_custom_type(tool_mock):
    class CustomType:
        def __init__(self, value):
            self.value = value

    result = tool_mock._convert_to_type("test", CustomType)
    assert isinstance(result, CustomType)
    assert result.value == "test"


# Test mock decorator
@pytest.mark.asyncio
async def test_mock_decorator_simulation_mode(simulation_env):
    @veris.mock
    async def test_func(param1: str, param2: int) -> dict[str, Any]:
        return {"result": "real"}

    mock_response = {"result": {"mocked": True}}

    with patch("httpx.AsyncClient") as mock_client:
        mock_response_obj = Mock()
        mock_response_obj.json.return_value = mock_response
        mock_response_obj.raise_for_status.return_value = None

        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response_obj,
        )

        result = await test_func("test", 42)
        assert result == {"mocked": True}


@pytest.mark.asyncio
async def test_mock_decorator_production_mode(production_env):
    @veris.mock
    async def test_func(param1: str, param2: int) -> dict:
        return {"result": "real"}

    result = await test_func("test", 42)
    assert result == {"result": "real"}


@pytest.mark.asyncio
async def test_mock_with_context(simulation_env, mock_context):
    @veris.mock
    async def test_func(ctx) -> dict:
        return {"result": "real"}

    mock_response = {"result": {"mocked": True}}

    with patch("veris_ai.tool_mock.httpx.AsyncClient") as mock_client:
        mock_response_obj = Mock()
        mock_response_obj.json.return_value = mock_response
        mock_response_obj.raise_for_status.return_value = None

        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response_obj,
        )

        result = await test_func(mock_context)
        first_call = mock_client.return_value.__aenter__.return_value.post.call_args
        assert (
            first_call.kwargs["json"]["session_id"]
            == mock_context.request_context.lifespan_context.session_id
        )
        assert result == {"mocked": True}


@pytest.mark.asyncio
async def test_mock_without_context(simulation_env):
    @veris.mock
    async def test_func() -> dict:
        return {"result": "real"}

    mock_response = {"result": {"mocked": True}}

    with patch("veris_ai.tool_mock.httpx.AsyncClient") as mock_client:
        mock_response_obj = Mock()
        mock_response_obj.json.return_value = mock_response
        mock_response_obj.raise_for_status.return_value = None

        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response_obj,
        )

        result = await test_func()
        first_call = mock_client.return_value.__aenter__.return_value.post.call_args
        assert first_call.kwargs["json"]["session_id"] == None
        assert result == {"mocked": True}


@pytest.mark.asyncio
async def test_mock_with_malformed_context(simulation_env):
    @veris.mock
    async def test_func(ctx) -> dict:
        return {"result": "real"}

    mock_response = {"result": {"mocked": True}}

    with patch("veris_ai.tool_mock.httpx.AsyncClient") as mock_client:
        mock_response_obj = Mock()
        mock_response_obj.json.return_value = mock_response
        mock_response_obj.raise_for_status.return_value = None

        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response_obj,
        )

        result = await test_func({"unknown": "unknown"})
        first_call = mock_client.return_value.__aenter__.return_value.post.call_args
        assert first_call.kwargs["json"]["session_id"] == None
        assert result == {"mocked": True}


# Test error handling
@pytest.mark.asyncio
async def test_mock_http_error(simulation_env):
    @veris.mock
    async def test_func(param1: str) -> dict:
        return {"result": "real"}

    with patch("httpx.AsyncClient") as mock_client:
        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            side_effect=httpx.HTTPError("Mock HTTP Error"),
        )

        with pytest.raises(httpx.HTTPError):
            await test_func("test")


@pytest.mark.asyncio
async def test_mock_missing_endpoint():
    with (
        patch.dict(os.environ, {"VERIS_MOCK_ENDPOINT_URL": ""}),
        pytest.raises(ValueError, match="VERIS_MOCK_ENDPOINT_URL environment variable is not set"),
    ):

        @veris.mock
        async def test_func():
            return {"result": "real"}


@pytest.mark.asyncio
async def test_mock_invalid_endpoint(simulation_env):
    with patch.dict(os.environ, {"VERIS_MOCK_ENDPOINT_URL": ""}), pytest.raises(ValueError):

        @veris.mock
        async def test_func():
            return {"result": "real"}

        await test_func()


@pytest.mark.asyncio
async def test_mock_string_json_response(simulation_env):
    @veris.mock
    async def test_func() -> dict:
        return {"result": "real"}

    mock_response = {"result": '{"key": "value"}'}

    with patch("httpx.AsyncClient") as mock_client:
        mock_response_obj = Mock()
        mock_response_obj.json.return_value = mock_response
        mock_response_obj.raise_for_status.return_value = None

        mock_client.return_value.__aenter__.return_value.post = AsyncMock(
            return_value=mock_response_obj,
        )

        result = await test_func()
        assert result == {"key": "value"}
