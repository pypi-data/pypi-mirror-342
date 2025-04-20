from typing import Any, Dict, List, Optional

from nebu.containers.models import (
    V1ContainerRequest,
    V1ResourceMeta,
    V1ResourceMetaRequest,
)
from pydantic import BaseModel, Field


class V1ReplayBufferRequest(BaseModel):
    metadata: V1ResourceMetaRequest
    train_every: Optional[int] = None
    sample_n: int = Field(default=100)
    sample_strategy: str = Field(default="Random")
    num_epochs: int = Field(default=1)
    train_job: Optional[V1ContainerRequest] = None


class V1UpdateReplayBufferRequest(BaseModel):
    train_every: Optional[int] = None
    sample_n: Optional[int] = None
    sample_strategy: Optional[str] = None
    num_epochs: Optional[int] = None
    train_job: Optional[V1ContainerRequest] = None


class V1ReplayBufferStatus(BaseModel):
    num_records: Optional[int] = None
    train_idx: Optional[int] = None
    num_train_jobs: Optional[int] = None
    last_train_job: Optional[str] = None


class V1ReplayBuffer(BaseModel):
    metadata: V1ResourceMeta
    train_every: Optional[int] = None
    sample_n: Optional[int] = None
    sample_strategy: Optional[str] = None
    status: Optional[V1ReplayBufferStatus] = None
    train_job: Optional[V1ContainerRequest] = None


class V1ReplayBuffersResponse(BaseModel):
    buffers: List[V1ReplayBuffer]


class V1ReplayBufferData(BaseModel):
    examples: List[Dict[str, Any]]
    train: Optional[bool] = None


class V1SampleResponse(BaseModel):
    dataset_uri: Optional[str] = None
    samples: Optional[List[Dict[str, Any]]] = None


class V1SampleBufferQuery(BaseModel):
    n: int = 10
    strategy: str = "Random"
    link: bool = False
