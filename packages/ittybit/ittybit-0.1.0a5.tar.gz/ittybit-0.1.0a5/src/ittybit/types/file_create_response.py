# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["FileCreateResponse"]


class FileCreateResponse(BaseModel):
    id: Optional[str] = None

    filename: Optional[str] = None

    folder: Optional[str] = None

    media_id: Optional[str] = None

    url: Optional[str] = None
