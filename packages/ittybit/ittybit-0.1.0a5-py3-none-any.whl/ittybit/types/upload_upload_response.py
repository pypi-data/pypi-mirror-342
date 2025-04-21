# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["UploadUploadResponse", "Data"]


class Data(BaseModel):
    url: Optional[str] = None
    """Signed URL for uploading file"""


class UploadUploadResponse(BaseModel):
    data: Optional[Data] = None
