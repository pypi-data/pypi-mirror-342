from typing import Any, List, Optional

from nebu.meta import V1ResourceMeta, V1ResourceMetaRequest, V1ResourceReference
from pydantic import BaseModel, ConfigDict


class V1OnlineLLMRequest(BaseModel):
    metadata: V1ResourceMetaRequest
    model: str
    buffer: V1ResourceReference
    server: V1ResourceReference
    trainer: V1ResourceReference
    train_args: Optional[Any] = None
    chat_schema: Optional[str] = None

    model_config = ConfigDict(use_enum_values=True)


class V1UpdateOnlineLLMRequest(BaseModel):
    model: Optional[str] = None
    buffer: Optional[V1ResourceReference] = None
    server: Optional[V1ResourceReference] = None
    trainer: Optional[V1ResourceReference] = None
    train_args: Optional[Any] = None
    chat_schema: Optional[str] = None
    no_delete: Optional[bool] = None

    model_config = ConfigDict(use_enum_values=True)


class V1OnlineLLMStatus(BaseModel):
    is_online: Optional[bool] = None
    endpoint: Optional[str] = None
    last_error: Optional[str] = None

    model_config = ConfigDict(use_enum_values=True)


class V1OnlineLLM(BaseModel):
    metadata: V1ResourceMeta
    model: str
    buffer: V1ResourceReference
    server: V1ResourceReference
    trainer: V1ResourceReference
    train_args: Optional[Any] = None
    chat_schema: Optional[str] = None
    status: V1OnlineLLMStatus

    model_config = ConfigDict(use_enum_values=True)


class V1OnlineLLMs(BaseModel):
    llms: List[V1OnlineLLM]

    model_config = ConfigDict(use_enum_values=True)
