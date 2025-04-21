# src/projectdavid_common/validation.py # Or schemas/vector_store_schemas.py depending on your structure

import time
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

# Ensure you import the datetime class correctly if/when needed in OTHER models
# from datetime import datetime as dt


class StatusEnum(str, Enum):
    deleted = "deleted"
    active = "active"
    queued = "queued"
    in_progress = "in_progress"
    pending_action = "action_required"
    completed = "completed"
    failed = "failed"
    cancelling = "cancelling"
    cancelled = "cancelled"
    pending = "pending"
    processing = "processing"
    expired = "expired"
    retrying = "retrying"
    inactive = "inactive"
    error = "error"


class VectorStoreCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=128, description="Human-friendly store name")
    user_id: str = Field(..., min_length=3, description="Owner user ID")
    vector_size: int = Field(..., gt=0, description="Dimensionality of the vectors")
    distance_metric: str = Field(..., description="Distance metric (COSINE, EUCLID, DOT)")
    config: Optional[Dict[str, Any]] = Field(None, description="Additional configuration options")

    @field_validator("distance_metric")
    @classmethod
    def validate_distance_metric(cls, v: str) -> str:
        allowed = {"COSINE", "EUCLID", "DOT"}
        upper = v.upper()
        if upper not in allowed:
            raise ValueError(f"Invalid distance metric: '{v}'. Must be one of {allowed}")
        return upper


class VectorStoreRead(BaseModel):
    id: str = Field(..., description="Unique identifier for the vector store")
    name: str = Field(..., description="Vector store name")
    user_id: str = Field(..., description="User who owns this store")
    collection_name: str = Field(..., description="Qdrant collection name (matches ID)")
    vector_size: int = Field(..., description="Vector dimensionality")
    distance_metric: str = Field(..., description="Metric used for comparison")
    # --- Using int for timestamps, which is correct based on this schema ---
    created_at: int = Field(..., description="Unix timestamp when created")
    updated_at: Optional[int] = Field(None, description="Last modified timestamp")
    status: StatusEnum = Field(..., description="Vector store status")
    config: Optional[Dict[str, Any]] = Field(None, description="Optional config dict")
    file_count: int = Field(..., ge=0, description="Number of files associated")
    object: str = Field("vector_store", description="Object type identifier.")

    model_config = ConfigDict(from_attributes=True)


class VectorStoreCreateWithSharedId(VectorStoreCreate):
    shared_id: str = Field(
        ..., description="The pre-generated unique ID for the store and collection."
    )


class VectorStoreUpdate(BaseModel):
    name: Optional[str] = Field(
        None, min_length=3, max_length=128, description="New vector store name"
    )
    status: Optional[StatusEnum] = Field(None, description="Status override")
    config: Optional[Dict[str, Any]] = Field(None, description="New config")


class VectorStoreFileCreate(BaseModel):
    file_id: str = Field(..., description="Client-assigned unique ID for the file record")
    file_name: str = Field(..., max_length=256, description="Original filename")
    file_path: str = Field(..., max_length=1024, description="Identifier path used in metadata")
    status: Optional[StatusEnum] = Field(None, description="Initial processing state")
    meta_data: Optional[Dict[str, Any]] = Field(None, description="Metadata dict")


class VectorStoreFileRead(BaseModel):
    id: str = Field(..., description="File record ID")
    vector_store_id: str = Field(..., description="Owning vector store ID")
    file_name: str = Field(..., description="Original file name")
    file_path: str = Field(..., description="Qdrant metadata path identifier")
    # --- Using int for timestamp, which is correct based on this schema ---
    processed_at: Optional[int] = Field(
        None, description="Unix timestamp of last processing change"
    )
    status: StatusEnum = Field(..., description="Current processing state")
    error_message: Optional[str] = Field(None, description="Failure reason if applicable")
    meta_data: Optional[Dict[str, Any]] = Field(None, description="Metadata dict")
    object: str = Field("vector_store.file", description="Object type identifier.")

    model_config = ConfigDict(from_attributes=True)


class VectorStoreFileUpdateStatus(BaseModel):
    status: StatusEnum = Field(..., description="The new status for the file record.")
    error_message: Optional[str] = Field(None, description="Error message if status is 'failed'.")


class VectorStoreFileUpdate(BaseModel):
    status: Optional[StatusEnum] = Field(None, description="Status override")
    error_message: Optional[str] = Field(None, description="New error message")
    meta_data: Optional[Dict[str, Any]] = Field(None, description="Metadata replacement")


class VectorStoreList(BaseModel):
    vector_stores: List[VectorStoreRead]
    object: str = Field("list", description="Object type identifier.")


class VectorStoreFileList(BaseModel):
    files: List[VectorStoreFileRead]
    object: str = Field("list", description="Object type identifier.")


class VectorStoreLinkAssistant(BaseModel):
    assistant_ids: List[str] = Field(..., min_length=1, description="List of Assistant IDs to link")


class VectorStoreUnlinkAssistant(BaseModel):
    assistant_id: str = Field(..., description="Assistant ID to unlink")


class VectorStoreSearchResult(BaseModel):
    text: str = Field(..., description="Returned text chunk")
    meta_data: Optional[Dict[str, Any]] = Field(
        None, description="Metadata associated with the chunk"
    )
    score: float = Field(..., description="Similarity score from the vector search")
    vector_id: Optional[str] = Field(
        None, description="Unique ID of the vector point in the database"
    )
    store_id: Optional[str] = Field(
        None, description="ID of the vector store where the result originated"
    )
    # --- Using int for timestamp, which is correct based on this schema ---
    retrieved_at: int = Field(
        default_factory=lambda: int(time.time()),
        description="Unix timestamp when search was performed",
    )


class SearchExplanation(BaseModel):
    base_score: float
    filters_passed: Optional[List[str]] = None
    boosts_applied: Optional[Dict[str, float]] = None
    final_score: float


class EnhancedVectorSearchResult(VectorStoreSearchResult):
    explanation: Optional[SearchExplanation] = Field(
        None, description="Detailed explanation of the search score, if available"
    )


class VectorStoreAddRequest(BaseModel):
    texts: List[str] = Field(..., description="List of text chunks to index")
    vectors: List[List[float]] = Field(
        ..., description="List of vector embeddings corresponding to text chunks"
    )
    meta_data: List[Dict[str, Any]] = Field(
        ..., description="List of metadata dictionaries corresponding to text chunks"
    )

    @model_validator(mode="after")
    def check_lengths_match(self) -> "VectorStoreAddRequest":
        if not (len(self.texts) == len(self.vectors) == len(self.meta_data)):
            raise ValueError(
                f"Input lengths must match: texts({len(self.texts)}), "
                f"vectors({len(self.vectors)}), meta_data({len(self.meta_data)})"
            )
        return self
