from typing import Any, Dict, List, Optional

import requests
from nebu import V1ResourceReference

from orign.auth import get_user_profile
from orign.config import GlobalConfig
from orign.trainings.models import (
    V1LogRequest,
    V1ResourceMetaRequest,
    V1Training,
    V1TrainingRequest,
    V1Trainings,
    V1TrainingStatus,
    V1TrainingUpdateRequest,
)


class Training:
    def __init__(
        self,
        name: str,
        namespace: Optional[str] = None,
        config_data: Optional[Dict[str, Any]] = None,
        adapter: Optional[V1ResourceReference] = None,
        labels: Optional[Dict[str, str]] = None,
        config: Optional[GlobalConfig] = None,
    ):
        config = config or GlobalConfig.read()
        self.api_key = config.api_key
        self.orign_host = config.server
        self.trainings_url = f"{self.orign_host}/v1/trainings"

        if not namespace:
            if not self.api_key:
                raise ValueError("No API key provided and namespace not specified")

            user_profile = get_user_profile(self.api_key)
            namespace = user_profile.handle
            if not namespace:
                # Fallback if handle is not set
                namespace = user_profile.email.replace("@", "-").replace(".", "-")

        self.namespace = namespace
        self.name = name
        training_id = f"{self.namespace}/{self.name}"
        get_url = f"{self.trainings_url}/{training_id}"

        try:
            response = requests.get(
                get_url, headers={"Authorization": f"Bearer {self.api_key}"}
            )
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            self.training = V1Training.model_validate(response.json())
            print(f"Found existing training {self.training.metadata.name}")
        except requests.exceptions.HTTPError as e:
            if e.response is not None and e.response.status_code == 404:
                # Training not found, create it
                print(f"Creating training {self.name} in namespace {self.namespace}")
                request = V1TrainingRequest(
                    metadata=V1ResourceMetaRequest(
                        name=self.name,
                        namespace=self.namespace,
                        labels=labels,
                    ),
                    config=config_data,
                    adapter=adapter,
                )
                response = requests.post(
                    self.trainings_url,
                    json=request.model_dump(exclude_none=True),
                    headers={"Authorization": f"Bearer {self.api_key}"},
                )
                response.raise_for_status()
                self.training = V1Training.model_validate(response.json())
                print(f"Created training {self.training.metadata.name}")
            else:
                # Re-raise other HTTP errors
                raise e
        except requests.exceptions.RequestException as e:
            # Handle connection errors, timeouts, etc.
            print(f"Request failed: {e}")
            raise

    def update(
        self,
        status: Optional[V1TrainingStatus] = None,
        summary_metrics: Optional[Dict[str, Any]] = None,
    ):
        if (
            not self.training
            or not self.training.metadata.namespace
            or not self.training.metadata.name
        ):
            raise ValueError("Training information is missing")

        url = f"{self.trainings_url}/{self.training.metadata.namespace}/{self.training.metadata.name}"
        request = V1TrainingUpdateRequest(
            status=status,
            summary_metrics=summary_metrics,
        )

        response = requests.patch(
            url,
            json=request.model_dump(exclude_none=True),
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()
        # Update local state with the response
        updated_training_data = response.json()
        self.training = V1Training.model_validate(updated_training_data)
        print(f"Updated training {self.training.metadata.name}")
        return self.training

    def log(
        self,
        data: Dict[str, Any],
        step: Optional[int] = None,
        timestamp: Optional[int] = None,
    ):
        if (
            not self.training
            or not self.training.metadata.namespace
            or not self.training.metadata.name
        ):
            raise ValueError("Training information is missing")

        url = f"{self.trainings_url}/{self.training.metadata.namespace}/{self.training.metadata.name}/log"
        request = V1LogRequest(data=data, step=step, timestamp=timestamp)

        response = requests.post(
            url,
            json=request.model_dump(exclude_none=True),
            headers={"Authorization": f"Bearer {self.api_key}"},
        )
        response.raise_for_status()
        print(f"Logged data for training {self.training.metadata.name}")
        # Log endpoint typically returns a 200 OK or similar, no body needed
        return response.json()  # Or just status code

    @staticmethod
    def get(
        namespace: Optional[str] = None,
        name: Optional[str] = None,
        config: Optional[GlobalConfig] = None,
    ) -> List[V1Training]:
        config = config or GlobalConfig.read()
        trainings_url = f"{config.server}/v1/trainings"

        response = requests.get(
            trainings_url, headers={"Authorization": f"Bearer {config.api_key}"}
        )
        response.raise_for_status()
        trainings_response = V1Trainings.model_validate(response.json())
        trainings = trainings_response.trainings

        if namespace:
            trainings = [t for t in trainings if t.metadata.namespace == namespace]

        if name:
            trainings = [t for t in trainings if t.metadata.name == name]

        return trainings
