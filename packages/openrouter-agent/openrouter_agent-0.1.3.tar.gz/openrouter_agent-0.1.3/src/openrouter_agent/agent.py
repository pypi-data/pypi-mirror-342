# openrouter_agent.py
import uuid
import os
from typing import Any, Dict, Optional

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from .config import BASE_URL, API_KEY, DEFAULT_MODEL_NAME


class OpenRouterModel(OpenAIModel):
    """A model class to allow using OpenRouter models with the Pydantic AI library
    This class inherits from OpenAIModel and uses the OpenAIProvider to
    communicate with the OpenRouter API.
    """

    def __init__(
        self,
        model_name: str = DEFAULT_MODEL_NAME,
        base_url: str = BASE_URL,
        api_key: Optional[str] = API_KEY,
    ):
        super().__init__(
            model_name=model_name,
            provider=OpenAIProvider(base_url=base_url, api_key=api_key),
        )
    
    def _process_response(self, response):
        """Override to handle missing created timestamp"""
        # If response doesn't have created field or it's None, add current timestamp
        if not hasattr(response, 'created') or response.created is None:
            from datetime import datetime, timezone
            # Create a modified response object with current timestamp
            from types import SimpleNamespace
            modified_response = SimpleNamespace(**{k: v for k, v in response.__dict__.items()})
            modified_response.created = int(datetime.now(timezone.utc).timestamp())
            return super()._process_response(modified_response)
        
        # Otherwise, process normally
        return super()._process_response(response)

class OpenRouterAgent(Agent):
    """A class to create an agent that uses the OpenRouter model.
    This class inherits from Agent and uses the OpenRouterModel to
    communicate with the OpenRouter API.
    """

    def __init__(
        self,
        agent_name: str = uuid.uuid4().hex,
        model_name: str = DEFAULT_MODEL_NAME,
        temp: float = 0.1,
        result_retries: int = 10,
        base_url: str = BASE_URL,
        api_key: Optional[str] = API_KEY,
        instrument: bool = True,
        **kwargs: Any,
    ):
        super().__init__(
            model=OpenRouterModel(
                model_name=model_name, 
                base_url=base_url,
                api_key=api_key,
            ),
            result_retries=result_retries,
            name=agent_name,
            model_settings={
                "temperature": temp,
            },
            instrument=instrument,
            **kwargs,  # pass any additional keyword arguments to the Agent constructor.
        )

Agent = OpenRouterAgent
__all__ = ["OpenRouterModel", "OpenRouterAgent", "Agent"]