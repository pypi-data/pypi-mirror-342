# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import upload_upload_params
from .._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from .._utils import (
    maybe_transform,
    async_maybe_transform,
)
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from .._base_client import make_request_options
from ..types.upload_upload_response import UploadUploadResponse

__all__ = ["UploadResource", "AsyncUploadResource"]


class UploadResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> UploadResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ittybit/sdk-python#accessing-raw-response-data-eg-headers
        """
        return UploadResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> UploadResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ittybit/sdk-python#with_streaming_response
        """
        return UploadResourceWithStreamingResponse(self)

    def upload(
        self,
        *,
        alt: str | NotGiven = NOT_GIVEN,
        async_: bool | NotGiven = NOT_GIVEN,
        file_id: str | NotGiven = NOT_GIVEN,
        filename: str | NotGiven = NOT_GIVEN,
        folder: str | NotGiven = NOT_GIVEN,
        label: str | NotGiven = NOT_GIVEN,
        media_id: str | NotGiven = NOT_GIVEN,
        metadata: object | NotGiven = NOT_GIVEN,
        api_timeout: int | NotGiven = NOT_GIVEN,
        title: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UploadUploadResponse:
        """
        Create a new upload URL

        Args:
          alt: Optional alt text

          async_: Whether to process upload asynchronously

          file_id: Optional file ID

          filename: Optional filename

          folder: Optional folder path

          label: Optional label for the upload

          media_id: Optional media ID

          metadata: Optional metadata object

          api_timeout: Upload URL timeout in seconds

          title: Optional title

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/uploads",
            body=maybe_transform(
                {
                    "alt": alt,
                    "async_": async_,
                    "file_id": file_id,
                    "filename": filename,
                    "folder": folder,
                    "label": label,
                    "media_id": media_id,
                    "metadata": metadata,
                    "api_timeout": api_timeout,
                    "title": title,
                },
                upload_upload_params.UploadUploadParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UploadUploadResponse,
        )


class AsyncUploadResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncUploadResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ittybit/sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncUploadResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncUploadResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ittybit/sdk-python#with_streaming_response
        """
        return AsyncUploadResourceWithStreamingResponse(self)

    async def upload(
        self,
        *,
        alt: str | NotGiven = NOT_GIVEN,
        async_: bool | NotGiven = NOT_GIVEN,
        file_id: str | NotGiven = NOT_GIVEN,
        filename: str | NotGiven = NOT_GIVEN,
        folder: str | NotGiven = NOT_GIVEN,
        label: str | NotGiven = NOT_GIVEN,
        media_id: str | NotGiven = NOT_GIVEN,
        metadata: object | NotGiven = NOT_GIVEN,
        api_timeout: int | NotGiven = NOT_GIVEN,
        title: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> UploadUploadResponse:
        """
        Create a new upload URL

        Args:
          alt: Optional alt text

          async_: Whether to process upload asynchronously

          file_id: Optional file ID

          filename: Optional filename

          folder: Optional folder path

          label: Optional label for the upload

          media_id: Optional media ID

          metadata: Optional metadata object

          api_timeout: Upload URL timeout in seconds

          title: Optional title

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/uploads",
            body=await async_maybe_transform(
                {
                    "alt": alt,
                    "async_": async_,
                    "file_id": file_id,
                    "filename": filename,
                    "folder": folder,
                    "label": label,
                    "media_id": media_id,
                    "metadata": metadata,
                    "api_timeout": api_timeout,
                    "title": title,
                },
                upload_upload_params.UploadUploadParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=UploadUploadResponse,
        )


class UploadResourceWithRawResponse:
    def __init__(self, upload: UploadResource) -> None:
        self._upload = upload

        self.upload = to_raw_response_wrapper(
            upload.upload,
        )


class AsyncUploadResourceWithRawResponse:
    def __init__(self, upload: AsyncUploadResource) -> None:
        self._upload = upload

        self.upload = async_to_raw_response_wrapper(
            upload.upload,
        )


class UploadResourceWithStreamingResponse:
    def __init__(self, upload: UploadResource) -> None:
        self._upload = upload

        self.upload = to_streamed_response_wrapper(
            upload.upload,
        )


class AsyncUploadResourceWithStreamingResponse:
    def __init__(self, upload: AsyncUploadResource) -> None:
        self._upload = upload

        self.upload = async_to_streamed_response_wrapper(
            upload.upload,
        )
