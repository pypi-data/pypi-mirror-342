from typing import Dict, List, Optional

import requests

from orign.auth import get_user_profile
from orign.buffers.models import (
    V1ContainerRequest,
    V1ReplayBuffer,
    V1ReplayBufferData,
    V1ReplayBufferRequest,
    V1ReplayBuffersResponse,
    V1ResourceMetaRequest,
    V1SampleBufferQuery,
    V1SampleResponse,
    V1UpdateReplayBufferRequest,
)
from orign.config import GlobalConfig


class ReplayBuffer:
    def __init__(
        self,
        name: str,
        train_job: Optional[V1ContainerRequest] = None,
        namespace: Optional[str] = None,
        train_every: int = 50,
        sample_n: int = 100,
        sample_strategy: str = "Random",
        labels: Optional[Dict[str, str]] = None,
        config: Optional[GlobalConfig] = None,
    ):
        config = config or GlobalConfig.read()
        self.api_key = config.api_key
        self.orign_host = config.server

        # Construct the WebSocket URL with query parameters
        self.buffers_url = f"{self.orign_host}/v1/buffers"

        if not namespace:
            if not self.api_key:
                raise ValueError("No API key provided")

            user_profile = get_user_profile(self.api_key)
            namespace = user_profile.handle

            if not namespace:
                namespace = user_profile.email.replace("@", "-").replace(".", "-")

        response = requests.get(
            self.buffers_url, headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()
        buffers = V1ReplayBuffersResponse.model_validate(response.json())
        print(buffers)
        self.buffer = next(
            (
                b
                for b in buffers.buffers
                if b.metadata.name == name and b.metadata.namespace == namespace
            ),
            None,
        )

        if not self.buffer:
            print(f"Creating buffer {name} in namespace {namespace}")
            request = V1ReplayBufferRequest(
                metadata=V1ResourceMetaRequest(
                    name=name,
                    namespace=namespace,
                    labels=labels,
                ),
                train_every=train_every,
                sample_n=sample_n,
                sample_strategy=sample_strategy,
                train_job=train_job,
            )
            response = requests.post(
                self.buffers_url,
                json=request.model_dump(),
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            response.raise_for_status()
            self.buffer = V1ReplayBuffer.model_validate(response.json())
            print(f"Created buffer {self.buffer.metadata.name}")
        else:
            print(f"Found buffer {self.buffer.metadata.name}, updating if necessary")
            request = V1UpdateReplayBufferRequest(
                train_every=train_every,
                sample_n=sample_n,
                sample_strategy=sample_strategy,
                train_job=train_job,
            )
            response = requests.patch(
                f"{self.buffers_url}/{self.buffer.metadata.namespace}/{self.buffer.metadata.name}",
                json=request.model_dump(),
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            response.raise_for_status()
            print(f"Updated buffer {self.buffer.metadata.name}")

    def send(self, data: List[dict], train: Optional[bool] = None):
        if not self.buffer or not self.buffer.metadata.name:
            raise ValueError("Buffer not found")

        url = f"{self.buffers_url}/{self.buffer.metadata.namespace}/{self.buffer.metadata.name}/examples"

        request = V1ReplayBufferData(examples=data, train=train)  # type: ignore

        response = requests.post(
            url,
            json=request.model_dump(),
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()
        return response.json()

    def sample(
        self,
        n: int = 10,
        strategy: str = "Random",
        link: bool = False,
    ) -> V1SampleResponse:
        """
        Samples data from the replay buffer using a POST request.

        Args:
            sample_n: The number of samples to retrieve.
            sample_strategy: The sampling strategy to use (e.g., "Random").

        Returns:
            A V1SampleResponse object containing information about the sampled dataset.
        """
        if not self.buffer or not self.buffer.metadata.name:
            raise ValueError("Buffer not found")

        url = f"{self.buffers_url}/{self.buffer.metadata.namespace}/{self.buffer.metadata.name}/sample"
        query = V1SampleBufferQuery(n=n, strategy=strategy, link=link)

        response = requests.post(
            url,
            json=query.model_dump(),
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()
        return V1SampleResponse.model_validate(response.json())

    def train(self):
        if not self.buffer or not self.buffer.metadata.name:
            raise ValueError("Buffer not found")

        url = f"{self.buffers_url}/{self.buffer.metadata.namespace}/{self.buffer.metadata.name}/train"
        response = requests.post(
            url, headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()
        return response.json()

    @classmethod
    def get(
        cls,
        namespace: Optional[str] = None,
        name: Optional[str] = None,
        config: Optional[GlobalConfig] = None,
    ) -> List[V1ReplayBuffer]:
        config = config or GlobalConfig.read()

        # Construct the WebSocket URL with query parameters
        buffers_url = f"{config.server}/v1/buffers"

        response = requests.get(
            buffers_url, headers={"Authorization": f"Bearer {config.api_key}"}
        )
        response.raise_for_status()
        buffer_response = V1ReplayBuffersResponse.model_validate(response.json())
        buffers = buffer_response.buffers
        if name:
            buffers = [b for b in buffers if b.metadata.name == name]

        if namespace:
            buffers = [b for b in buffers if b.metadata.namespace == namespace]

        return buffers
