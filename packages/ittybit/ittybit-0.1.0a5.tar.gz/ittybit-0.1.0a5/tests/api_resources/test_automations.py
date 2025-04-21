# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from ittybit import Ittybit, AsyncIttybit

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestAutomations:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_create(self, client: Ittybit) -> None:
        automation = client.automations.create(
            name="name",
        )
        assert automation is None

    @parametrize
    def test_method_create_with_all_params(self, client: Ittybit) -> None:
        automation = client.automations.create(
            name="name",
            actions=[{}],
            description="description",
            triggers=[{}],
        )
        assert automation is None

    @parametrize
    def test_raw_response_create(self, client: Ittybit) -> None:
        response = client.automations.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        automation = response.parse()
        assert automation is None

    @parametrize
    def test_streaming_response_create(self, client: Ittybit) -> None:
        with client.automations.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            automation = response.parse()
            assert automation is None

        assert cast(Any, response.is_closed) is True


class TestAsyncAutomations:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_create(self, async_client: AsyncIttybit) -> None:
        automation = await async_client.automations.create(
            name="name",
        )
        assert automation is None

    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncIttybit) -> None:
        automation = await async_client.automations.create(
            name="name",
            actions=[{}],
            description="description",
            triggers=[{}],
        )
        assert automation is None

    @parametrize
    async def test_raw_response_create(self, async_client: AsyncIttybit) -> None:
        response = await async_client.automations.with_raw_response.create(
            name="name",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        automation = await response.parse()
        assert automation is None

    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncIttybit) -> None:
        async with async_client.automations.with_streaming_response.create(
            name="name",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            automation = await response.parse()
            assert automation is None

        assert cast(Any, response.is_closed) is True
