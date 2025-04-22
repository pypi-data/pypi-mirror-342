#!src/projectdavid_common/schemas/file_service.py
from typing import Annotated, Literal, Optional

from pydantic import BaseModel, ConfigDict, Field


class FileUploadRequest(BaseModel):
    purpose: str = Field(..., description="Purpose for uploading the file")
    user_id: Optional[str] = Field(
        None,
        description="ID of the uploading user. If not provided, will be inferred from the authenticated API key.",
    )

    model_config = ConfigDict(from_attributes=True)


class FileResponse(BaseModel):
    id: str = Field(..., description="Unique identifier of the file")
    object: Annotated[Literal["file"], Field(description="The string 'file'")] = "file"
    bytes: int = Field(..., description="Size of the file in bytes")
    created_at: int = Field(..., description="Unix timestamp of when the file was created")
    filename: str = Field(..., description="Original filename")
    purpose: str = Field(..., description="Purpose associated with this file")
    status: str = Field("uploaded", description="Status of the file upload")
    expires_at: Optional[int] = Field(None, description="Optional Unix timestamp for expiry")

    model_config = ConfigDict(from_attributes=True)


class FileDeleteResponse(BaseModel):
    id: str = Field(..., description="Unique identifier of the file")
    object: Annotated[Literal["file"], Field(description="The string 'file'")] = "file"
    deleted: bool = Field(..., description="True if deletion was successful")

    model_config = ConfigDict(from_attributes=True)
