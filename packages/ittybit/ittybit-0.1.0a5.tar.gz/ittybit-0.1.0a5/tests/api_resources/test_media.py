# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from ittybit import Ittybit, AsyncIttybit

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestMedia:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Ittybit) -> None:
        media = client.media.create()
        assert media is None

    @parametrize
    def test_method_create_with_all_params(self, client: Ittybit) -> None:
        media = client.media.create(
            async_=True,
            empty=True,
            filename="filename",
            folder="folder",
            label="label",
            metadata={},
            title="title",
            url="url",
        )
        assert media is None

    @parametrize
    def test_raw_response_create(self, client: Ittybit) -> None:
        response = client.media.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        media = response.parse()
        assert media is None

    @parametrize
    def test_streaming_response_create(self, client: Ittybit) -> None:
        with client.media.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            media = response.parse()
            assert media is None

        assert cast(Any, response.is_closed) is True


class TestAsyncMedia:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncIttybit) -> None:
        media = await async_client.media.create()
        assert media is None

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncIttybit) -> None:
        media = await async_client.media.create(
            async_=True,
            empty=True,
            filename="filename",
            folder="folder",
            label="label",
            metadata={},
            title="title",
            url="url",
        )
        assert media is None

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncIttybit) -> None:
        response = await async_client.media.with_raw_response.create()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        media = await response.parse()
        assert media is None

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncIttybit) -> None:
        async with async_client.media.with_streaming_response.create() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            media = await response.parse()
            assert media is None

        assert cast(Any, response.is_closed) is True
