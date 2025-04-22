from datetime import datetime
from typing import Optional

from fastapi import Form
from pydantic import BaseModel, ConfigDict, field_validator


class FileUploadRequest(BaseModel):
    """Schema for file upload request data."""

    purpose: str = Form(...)
    user_id: str = Form(...)


class FileResponse(BaseModel):
    """Schema for file response data."""

    id: str
    object: str = "file"
    bytes: int
    created_at: int
    filename: str
    purpose: str
    status: str = "uploaded"
    expires_at: Optional[int] = None

    @field_validator("created_at", mode="before")
    @classmethod
    def datetime_to_timestamp(cls, value):
        if isinstance(value, datetime):
            return int(value.timestamp())
        return value

    model_config = ConfigDict(from_attributes=True)
