from typing import Any, Dict, List, Optional, Union

import requests
from openai.types.chat import ChatCompletion

from orign.auth import get_user_profile
from orign.buffers.models import V1ReplayBufferData
from orign.config import GlobalConfig
from orign.llms.models import (
    V1BufferOptionRequest,
    V1OnlineLLM,
    V1OnlineLLMRequest,
    V1OnlineLLMs,
    V1OnlineLLMStatus,
    V1ResourceMetaRequest,
    V1ServerOptionRequest,
    V1UpdateOnlineLLMRequest,
)


class OnlineLLM:
    """
    A class for managing Online LLM instances.
    """

    def __init__(
        self,
        name: str,
        model: str,
        server: V1ServerOptionRequest,
        buffer: V1BufferOptionRequest,
        namespace: Optional[str] = None,
        labels: Optional[Dict[str, str]] = None,
        config: Optional[GlobalConfig] = None,
        no_delete: bool = False,
    ):
        self.config = config or GlobalConfig.read()
        self.api_key = self.config.api_key
        self.orign_host = self.config.server
        self.name = name
        self.namespace = namespace
        self.labels = labels
        self.model = model
        self.llms_url = f"{self.orign_host}/v1/llms"

        # Fetch existing LLMs
        response = requests.get(
            self.llms_url, headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()

        if not namespace:
            if not self.api_key:
                raise ValueError("No API key provided")

            user_profile = get_user_profile(self.api_key)
            namespace = user_profile.handle

            if not namespace:
                namespace = user_profile.email.replace("@", "-").replace(".", "-")

        print(f"Using namespace: {namespace}")

        existing_llms = V1OnlineLLMs.model_validate(response.json())
        self.llm: Optional[V1OnlineLLM] = next(
            (
                llm_val
                for llm_val in existing_llms.llms
                if llm_val.metadata.name == name
                and llm_val.metadata.namespace == namespace
            ),
            None,
        )

        # If not found, create
        if not self.llm:
            request = V1OnlineLLMRequest(
                metadata=V1ResourceMetaRequest(
                    name=name,
                    namespace=namespace,
                    labels=labels,
                ),
                model=model,
                buffer=buffer,
                server=server,
            )
            print("Request:")
            print(request.model_dump_json())
            create_response = requests.post(
                self.llms_url,
                json=request.model_dump(),
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            create_response.raise_for_status()
            self.llm = V1OnlineLLM.model_validate(create_response.json())
            print(f"Created LLM {self.llm.metadata.name}")
        else:
            # Else, update
            print(f"Found LLM {self.llm.metadata.name}, updating if necessary")
            update_request = V1UpdateOnlineLLMRequest(
                buffer=buffer,
                server=server,
                no_delete=no_delete,
            )
            print("Update request:")
            print(update_request.model_dump_json())
            patch_response = requests.patch(
                f"{self.llms_url}/{self.llm.metadata.namespace}/{self.llm.metadata.name}",
                json=update_request.model_dump(),
                headers={"Authorization": f"Bearer {self.api_key}"},
            )
            patch_response.raise_for_status()
            print(f"Updated LLM {self.llm.metadata.name}")

    def chat(self, messages: List[Dict[str, Any]]) -> ChatCompletion:
        """
        Chat with the LLM.
        """
        if not self.llm or not self.llm.metadata.name:
            raise ValueError("LLM not found")

        url = f"{self.llms_url}/{self.llm.metadata.namespace}/{self.llm.metadata.name}/chat"

        request = {
            "model": self.model,
            "messages": messages,
        }

        response = requests.post(
            url,
            json=request,
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()
        return ChatCompletion.model_validate(response.json())

    def train(self) -> dict:
        """
        Train the LLM.
        """
        if not self.llm or not self.llm.metadata.name:
            raise ValueError("LLM not found")

        url = f"{self.llms_url}/{self.llm.metadata.namespace}/{self.llm.metadata.name}/train"
        response = requests.post(
            url, headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()
        return response.json()

    def learn(
        self,
        examples: Union[Dict[str, Any], List[Dict[str, Any]]],
        train: bool = False,
    ):
        """
        Learn from a list of examples.

        Examples should be a set of openai-style multi-turn conversations, or a single conversation.
        """

        if not self.llm or not self.llm.metadata.name:
            raise ValueError("LLM not found")

        # Convert single dictionary to list of dictionaries if needed
        if isinstance(examples, dict):
            examples = [examples]

        url = f"{self.llms_url}/{self.llm.metadata.namespace}/{self.llm.metadata.name}/learn"
        request = V1ReplayBufferData(examples=examples, train=train)

        response = requests.post(
            url,
            json=request.model_dump(),
            headers={"Authorization": f"Bearer {self.api_key}"},
        )

        response.raise_for_status()
        return response.json()

    @classmethod
    def load(
        cls,
        name: str,
        namespace: Optional[str] = None,
        config: Optional[GlobalConfig] = None,
    ):
        """
        Get an LLM from the remote server.
        """
        llms = cls.get(namespace=namespace, name=name, config=config)
        if not llms:
            raise ValueError("LLM not found")
        llm_v1 = llms[0]

        out = cls.__new__(cls)
        out.llm = llm_v1
        out.config = config or GlobalConfig.read()
        out.api_key = out.config.api_key
        out.orign_host = out.config.server
        out.llms_url = f"{out.orign_host}/v1/llms"
        out.name = name
        out.namespace = namespace
        out.model = llm_v1.model
        return out

    @classmethod
    def get(
        cls,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        config: Optional[GlobalConfig] = None,
    ) -> List[V1OnlineLLM]:
        """
        Get a list of LLMs that match the optional name and/or namespace filters.
        """
        config = config or GlobalConfig.read()
        llms_url = f"{config.server}/v1/llms"

        response = requests.get(
            llms_url, headers={"Authorization": f"Bearer {config.api_key}"}
        )
        response.raise_for_status()

        llms_response = V1OnlineLLMs.model_validate(response.json())
        filtered_llms = llms_response.llms

        if name:
            filtered_llms = [llm for llm in filtered_llms if llm.metadata.name == name]
        if namespace:
            filtered_llms = [
                llm for llm in filtered_llms if llm.metadata.namespace == namespace
            ]

        return filtered_llms

    def delete(self):
        """
        Delete the LLM.
        """
        if not self.llm or not self.llm.metadata.name:
            raise ValueError("LLM not found")

        url = f"{self.llms_url}/{self.llm.metadata.namespace}/{self.llm.metadata.name}"
        response = requests.delete(
            url, headers={"Authorization": f"Bearer {self.api_key}"}
        )
        response.raise_for_status()
        return

    def status(self) -> V1OnlineLLMStatus:
        """
        Get the status of the LLM.
        """
        if not self.llm or not self.llm.metadata.name:
            raise ValueError("LLM not found")

        llms = self.get(
            namespace=self.llm.metadata.namespace, name=self.llm.metadata.name
        )
        if not llms:
            raise ValueError("LLM not found")
        llm = llms[0]

        return llm.status

    def ref(self) -> str:
        """
        Get the resource ref for the container.
        """
        return f"{self.name}.{self.namespace}.Container"
