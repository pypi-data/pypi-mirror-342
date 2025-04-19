from typing import Any, Dict, List, Optional

from nebu.meta import V1ResourceMeta, V1ResourceMetaRequest, V1ResourceReference
from pydantic import BaseModel, Field


class V1HumanRequest(BaseModel):
    metadata: V1ResourceMetaRequest
    medium: str
    channel: Optional[str] = None
    callback: V1ResourceReference


class V1UpdateHumanRequest(BaseModel):
    medium: Optional[str] = None
    channel: Optional[str] = None
    callback: V1ResourceReference


class V1HumanStatus(BaseModel):
    is_active: Optional[bool] = None
    last_active: Optional[str] = None


class V1Human(BaseModel):
    metadata: V1ResourceMeta
    medium: str
    channel: Optional[str] = None
    callback: V1ResourceReference
    status: V1HumanStatus = Field(default_factory=V1HumanStatus)


class V1Humans(BaseModel):
    humans: List[V1Human] = Field(default_factory=list)


class V1ApprovalRequest(BaseModel):
    content: str
    messages: Optional[Dict[str, Any]] = None
    images: Optional[List[str]] = None
    videos: Optional[List[str]] = None


class V1ApprovalResponse(BaseModel):
    content: str
    messages: Optional[Dict[str, Any]] = None
    images: Optional[List[str]] = None
    videos: Optional[List[str]] = None
    approved: bool = False


class V1FeedbackRequest(BaseModel):
    kind: str
    request: Optional[V1ApprovalRequest] = None


class V1Feedback(BaseModel):
    kind: str
    request: V1ApprovalRequest
    response: Optional[V1ApprovalResponse] = None


class V1FeedbackResponse(BaseModel):
    kind: str
    response: Optional[V1ApprovalResponse] = None
