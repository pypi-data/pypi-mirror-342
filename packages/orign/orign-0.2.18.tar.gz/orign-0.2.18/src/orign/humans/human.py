import inspect
import random
import string
from typing import Any, Callable, Dict, List, Optional

import requests
from nebu.containers.models import (
    V1ContainerRequest,
    V1EnvVar,
    V1ResourceMetaRequest,
)

from orign.config import GlobalConfig
from orign.humans.models import (
    V1ApprovalRequest,
    V1ApprovalResponse,
    V1FeedbackRequest,
    V1FeedbackResponse,
    V1Human,
    V1HumanRequest,
    V1Humans,
)


class Human:
    def __init__(
        self,
        name: str,
        medium: str,
        response_job: Optional[V1ContainerRequest] = None,
        response_func: Optional[Callable] = None,
        namespace: Optional[str] = None,
        channel: Optional[str] = None,
        config: Optional[GlobalConfig] = None,
        platform: str = "runpod",
        python_cmd: str = "python",
        timeout: Optional[str] = None,
        accelerators: Optional[List[str]] = None,
        env: Optional[List[V1EnvVar]] = None,
    ):
        if not response_job and not response_func:
            raise ValueError("Either response_job or response_func must be provided")

        if response_job and response_func:
            raise ValueError(
                "Only one of response_job or response_func should be provided"
            )

        config = config or GlobalConfig.read()
        self.api_key = config.api_key
        self.orign_host = config.server

        self.name = name
        self.medium = medium
        self.namespace = namespace
        self.channel = channel

        # Create container request from function if provided
        if response_func:
            sig = inspect.signature(response_func)
            params = list(sig.parameters.values())
            if len(params) != 1:
                raise ValueError(
                    "The response function must accept exactly one parameter (V1FeedbackResponse)"
                )

            # Get function source code
            func_code = inspect.getsource(response_func)
            func_name = response_func.__name__

            command = f"""
print("Starting feedback container")
import json
import os

resp = os.getenv("FEEDBACK_RESPONSE")
if not resp:
    raise ValueError("FEEDBACK_RESPONSE environment variable not set")

print("Received feedback response:")
print(resp)

resp = json.loads(resp)

{func_code}

print(f"Calling function {func_name} with feedback response")

# Call the function with the feedback response
result = {func_name}(resp)
print(f"Function result: {{result}}")
"""

            print("creating container with command: ")
            print(command)

            image = "us-docker.pkg.dev/agentsea-dev/orign/py:latest"

            # Create the container request
            response_job = V1ContainerRequest(
                kind="Container",
                platform=platform,
                metadata=V1ResourceMetaRequest(
                    name=f"{name}-feedback-{''.join(random.choices(string.ascii_lowercase + string.digits, k=5))}",
                    namespace=namespace,
                ),
                image=image,
                env=env,
                command=f"{python_cmd} -c '{command}'",
                accelerators=accelerators,
                timeout=timeout,
                restart="Never",
            )

        self.response_job = response_job

        # Base URL for humans API
        self.humans_url = f"{self.orign_host}/v1/humans"

        # Check if human exists or create a new one
        humans = self.get(namespace=namespace, name=name, config=config)

        self.human = next(
            (
                h
                for h in humans
                if h.metadata.name == name and h.metadata.namespace == namespace
            ),
            None,
        )

        if not self.human:
            # Human doesn't exist, create it
            request = V1HumanRequest(
                metadata=V1ResourceMetaRequest(
                    name=name,
                    namespace=namespace,
                ),
                medium=medium,
                channel=channel,
                response_job=response_job,  # type: ignore
            )
            response = requests.post(
                self.humans_url,
                json=request.model_dump(),
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            response.raise_for_status()
            self.human = V1Human.model_validate(response.json())
            print(
                f"Created human {self.human.metadata.namespace}/{self.human.metadata.name}"
            )
        else:
            print(
                f"Found existing human {self.human.metadata.namespace}/{self.human.metadata.name}"
            )

    def request_feedback(
        self,
        content: str,
        messages: Optional[Dict[str, Any]] = None,
        images: Optional[List[str]] = None,
        videos: Optional[List[str]] = None,
    ) -> V1FeedbackResponse:
        """
        Request feedback from a human.
        """
        if not self.human:
            raise ValueError("Human not found")

        url = f"{self.humans_url}/{self.human.metadata.namespace}/{self.human.metadata.name}/feedback"

        request = V1FeedbackRequest(
            kind="approval",
            request=V1ApprovalRequest(
                content=content,
                images=images,
                videos=videos,
                messages=messages,
            ),
        )

        response = requests.post(
            url,
            json=request.model_dump(),
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()
        return V1FeedbackResponse.model_validate(response.json())

    def record_response(
        self,
        feedback_id: str,
        content: str,
        approved: bool = False,
        messages: Optional[Dict[str, Any]] = None,
        images: Optional[List[str]] = None,
        videos: Optional[List[str]] = None,
    ) -> dict:
        """
        Record a human's response to a feedback request.
        """
        if not self.human:
            raise ValueError("Human not found")

        url = f"{self.humans_url}/{self.human.metadata.namespace}/{self.human.metadata.name}/feedback/{feedback_id}"

        data = V1FeedbackResponse(
            kind="approval",
            response=V1ApprovalResponse(
                content=content,
                images=images,
                videos=videos,
                approved=approved,
                messages=messages,
            ),
        )

        response = requests.post(
            url,
            json=data.model_dump(),
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()
        return response.json()

    def delete(self) -> dict:
        """
        Delete this human.
        """
        if not self.human:
            raise ValueError("Human not found")

        url = f"{self.humans_url}/{self.human.metadata.namespace}/{self.human.metadata.name}"

        response = requests.delete(
            url,
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()
        return response.json()

    @classmethod
    def get(
        cls,
        namespace: Optional[str] = None,
        name: Optional[str] = None,
        config: Optional[GlobalConfig] = None,
    ) -> List[V1Human]:
        """
        Get a list of humans, optionally filtered by namespace and/or name.
        """
        config = config or GlobalConfig.read()
        humans_url = f"{config.server}/v1/humans"

        response = requests.get(
            humans_url, headers={"Authorization": f"Bearer {config.api_key}"}
        )
        response.raise_for_status()

        humans_response = V1Humans.model_validate(response.json())
        humans = humans_response.humans

        if name:
            humans = [h for h in humans if h.metadata.name == name]

        if namespace:
            humans = [h for h in humans if h.metadata.namespace == namespace]

        return humans
