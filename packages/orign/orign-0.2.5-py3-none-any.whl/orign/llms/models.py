from typing import List, Optional, Union

# External references (make sure these imports point to your actual modules):
from nebu.containers.models import V1Container, V1ContainerRequest
from nebu.meta import V1ResourceMeta, V1ResourceMetaRequest, V1ResourceReference
from pydantic import BaseModel, ConfigDict

from orign.buffers.models import V1ReplayBuffer, V1ReplayBufferRequest

# Union for V1BufferOption
V1BufferOption = Union[str, V1ReplayBuffer]


# Union for V1BufferOptionRequest
V1BufferOptionRequest = Union[str, V1ReplayBufferRequest]


# Union for V1ServerOption
V1ServerOption = Union[V1ResourceReference, V1Container]


# Union for V1ServerOptionRequest
V1ServerOptionRequest = Union[V1ResourceReference, V1ContainerRequest]


#
# Higher-level models use the union types
#
class V1OnlineLLMRequest(BaseModel):
    metadata: V1ResourceMetaRequest
    model: str
    buffer: V1BufferOptionRequest
    server: V1ServerOptionRequest
    chat_schema: Optional[str] = None

    model_config = ConfigDict(use_enum_values=True)


class V1UpdateOnlineLLMRequest(BaseModel):
    buffer: Optional[V1BufferOptionRequest] = None
    server: Optional[V1ServerOptionRequest] = None
    no_delete: bool = False
    model_config = ConfigDict(use_enum_values=True)


class V1OnlineLLMStatus(BaseModel):
    is_online: Optional[bool] = None
    endpoint: Optional[str] = None
    last_error: Optional[str] = None

    model_config = ConfigDict(use_enum_values=True)


class V1OnlineLLM(BaseModel):
    metadata: V1ResourceMeta
    model: str
    buffer: V1ReplayBuffer
    server: V1Container
    chat_schema: Optional[str] = None
    status: V1OnlineLLMStatus

    model_config = ConfigDict(use_enum_values=True)


class V1OnlineLLMs(BaseModel):
    llms: List[V1OnlineLLM]

    model_config = ConfigDict(use_enum_values=True)
