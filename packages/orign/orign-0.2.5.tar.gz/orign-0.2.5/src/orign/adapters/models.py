from typing import Dict, List, Optional

from nebu import V1ResourceMeta, V1ResourceMetaRequest
from pydantic import BaseModel, Field


class V1AdapterRequest(BaseModel):
    """Request payload for creating an adapter."""

    metadata: V1ResourceMetaRequest
    uri: str
    base_model: str
    epochs_trained: int
    last_trained: int
    examples_trained: int
    lora_rank: int = 8
    lora_alpha: int = 16
    lora_dropout: float = 0.1
    lora_target_modules: List[str] = Field(default_factory=list)
    learning_rate: float = 0.0001


class V1AdapterUpdateRequest(BaseModel):
    """Request payload for updating an adapter."""

    uri: Optional[str] = None
    epochs_trained: Optional[int] = None
    last_trained: Optional[int] = None
    examples_trained: Optional[int] = None
    learning_rate: Optional[float] = None
    labels: Optional[Dict[str, str]] = None


class V1Adapter(BaseModel):
    """Response payload representing an adapter."""

    metadata: V1ResourceMeta
    uri: str
    base_model: str
    epochs_trained: int
    last_trained: int
    examples_trained: int
    lora_rank: int
    lora_alpha: int
    lora_dropout: float
    lora_target_modules: List[str]
    learning_rate: float


class V1Adapters(BaseModel):
    """Response payload for a list of adapters."""

    adapters: List[V1Adapter]
