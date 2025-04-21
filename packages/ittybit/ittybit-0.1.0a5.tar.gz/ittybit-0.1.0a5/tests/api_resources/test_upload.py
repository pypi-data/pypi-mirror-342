# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from ittybit import Ittybit, AsyncIttybit
from tests.utils import assert_matches_type
from ittybit.types import UploadUploadResponse

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestUpload:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_upload(self, client: Ittybit) -> None:
        upload = client.upload.upload()
        assert_matches_type(UploadUploadResponse, upload, path=["response"])

    @parametrize
    def test_method_upload_with_all_params(self, client: Ittybit) -> None:
        upload = client.upload.upload(
            alt="alt",
            async_=True,
            file_id="file_id",
            filename="filename",
            folder="folder",
            label="label",
            media_id="media_id",
            metadata={},
            api_timeout=0,
            title="title",
        )
        assert_matches_type(UploadUploadResponse, upload, path=["response"])

    @parametrize
    def test_raw_response_upload(self, client: Ittybit) -> None:
        response = client.upload.with_raw_response.upload()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = response.parse()
        assert_matches_type(UploadUploadResponse, upload, path=["response"])

    @parametrize
    def test_streaming_response_upload(self, client: Ittybit) -> None:
        with client.upload.with_streaming_response.upload() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = response.parse()
            assert_matches_type(UploadUploadResponse, upload, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncUpload:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_upload(self, async_client: AsyncIttybit) -> None:
        upload = await async_client.upload.upload()
        assert_matches_type(UploadUploadResponse, upload, path=["response"])

    @parametrize
    async def test_method_upload_with_all_params(self, async_client: AsyncIttybit) -> None:
        upload = await async_client.upload.upload(
            alt="alt",
            async_=True,
            file_id="file_id",
            filename="filename",
            folder="folder",
            label="label",
            media_id="media_id",
            metadata={},
            api_timeout=0,
            title="title",
        )
        assert_matches_type(UploadUploadResponse, upload, path=["response"])

    @parametrize
    async def test_raw_response_upload(self, async_client: AsyncIttybit) -> None:
        response = await async_client.upload.with_raw_response.upload()

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        upload = await response.parse()
        assert_matches_type(UploadUploadResponse, upload, path=["response"])

    @parametrize
    async def test_streaming_response_upload(self, async_client: AsyncIttybit) -> None:
        async with async_client.upload.with_streaming_response.upload() as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            upload = await response.parse()
            assert_matches_type(UploadUploadResponse, upload, path=["response"])

        assert cast(Any, response.is_closed) is True
