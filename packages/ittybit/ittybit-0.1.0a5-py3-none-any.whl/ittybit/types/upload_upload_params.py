# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["UploadUploadParams"]


class UploadUploadParams(TypedDict, total=False):
    alt: str
    """Optional alt text"""

    async_: Annotated[bool, PropertyInfo(alias="async")]
    """Whether to process upload asynchronously"""

    file_id: str
    """Optional file ID"""

    filename: str
    """Optional filename"""

    folder: str
    """Optional folder path"""

    label: str
    """Optional label for the upload"""

    media_id: str
    """Optional media ID"""

    metadata: object
    """Optional metadata object"""

    api_timeout: Annotated[int, PropertyInfo(alias="timeout")]
    """Upload URL timeout in seconds"""

    title: str
    """Optional title"""
