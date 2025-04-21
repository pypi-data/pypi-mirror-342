# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["MediaCreateParams"]


class MediaCreateParams(TypedDict, total=False):
    async_: Annotated[bool, PropertyInfo(alias="async")]
    """Whether to process the media asynchronously"""

    empty: bool
    """Create an empty media placeholder"""

    filename: str
    """Filename for the media"""

    folder: str
    """Folder to store the media in"""

    label: str
    """Label for the media"""

    metadata: object
    """Additional metadata for the media"""

    title: str
    """Title for the media"""

    url: str
    """URL of the media to ingest"""
