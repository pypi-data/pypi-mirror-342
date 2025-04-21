# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..types import media_create_params
from .._types import NOT_GIVEN, Body, Query, Headers, NoneType, NotGiven
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

__all__ = ["MediaResource", "AsyncMediaResource"]


class MediaResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> MediaResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ittybit/sdk-python#accessing-raw-response-data-eg-headers
        """
        return MediaResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> MediaResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ittybit/sdk-python#with_streaming_response
        """
        return MediaResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        async_: bool | NotGiven = NOT_GIVEN,
        empty: bool | NotGiven = NOT_GIVEN,
        filename: str | NotGiven = NOT_GIVEN,
        folder: str | NotGiven = NOT_GIVEN,
        label: str | NotGiven = NOT_GIVEN,
        metadata: object | NotGiven = NOT_GIVEN,
        title: str | NotGiven = NOT_GIVEN,
        url: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Creates a new media item from a URL or as an empty placeholder

        Args:
          async_: Whether to process the media asynchronously

          empty: Create an empty media placeholder

          filename: Filename for the media

          folder: Folder to store the media in

          label: Label for the media

          metadata: Additional metadata for the media

          title: Title for the media

          url: URL of the media to ingest

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return self._post(
            "/media",
            body=maybe_transform(
                {
                    "async_": async_,
                    "empty": empty,
                    "filename": filename,
                    "folder": folder,
                    "label": label,
                    "metadata": metadata,
                    "title": title,
                    "url": url,
                },
                media_create_params.MediaCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class AsyncMediaResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncMediaResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/ittybit/sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncMediaResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncMediaResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/ittybit/sdk-python#with_streaming_response
        """
        return AsyncMediaResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        async_: bool | NotGiven = NOT_GIVEN,
        empty: bool | NotGiven = NOT_GIVEN,
        filename: str | NotGiven = NOT_GIVEN,
        folder: str | NotGiven = NOT_GIVEN,
        label: str | NotGiven = NOT_GIVEN,
        metadata: object | NotGiven = NOT_GIVEN,
        title: str | NotGiven = NOT_GIVEN,
        url: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> None:
        """
        Creates a new media item from a URL or as an empty placeholder

        Args:
          async_: Whether to process the media asynchronously

          empty: Create an empty media placeholder

          filename: Filename for the media

          folder: Folder to store the media in

          label: Label for the media

          metadata: Additional metadata for the media

          title: Title for the media

          url: URL of the media to ingest

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        extra_headers = {"Accept": "*/*", **(extra_headers or {})}
        return await self._post(
            "/media",
            body=await async_maybe_transform(
                {
                    "async_": async_,
                    "empty": empty,
                    "filename": filename,
                    "folder": folder,
                    "label": label,
                    "metadata": metadata,
                    "title": title,
                    "url": url,
                },
                media_create_params.MediaCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=NoneType,
        )


class MediaResourceWithRawResponse:
    def __init__(self, media: MediaResource) -> None:
        self._media = media

        self.create = to_raw_response_wrapper(
            media.create,
        )


class AsyncMediaResourceWithRawResponse:
    def __init__(self, media: AsyncMediaResource) -> None:
        self._media = media

        self.create = async_to_raw_response_wrapper(
            media.create,
        )


class MediaResourceWithStreamingResponse:
    def __init__(self, media: MediaResource) -> None:
        self._media = media

        self.create = to_streamed_response_wrapper(
            media.create,
        )


class AsyncMediaResourceWithStreamingResponse:
    def __init__(self, media: AsyncMediaResource) -> None:
        self._media = media

        self.create = async_to_streamed_response_wrapper(
            media.create,
        )
