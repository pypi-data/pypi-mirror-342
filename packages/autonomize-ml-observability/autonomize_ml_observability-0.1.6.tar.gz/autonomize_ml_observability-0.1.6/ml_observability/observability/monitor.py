"""
This module provides monitoring and observability capabilities for LLM (Large Language Model) 
clients.
It includes functionality for cost tracking, MLflow integration, and client wrapping for various 
LLM providers like OpenAI, Azure OpenAI, and Anthropic.
"""
import os
import logging
from typing import Optional

import mlflow

from ml_observability.core import ModelhubCredential
from ml_observability.observability.cost_tracking import CostTracker
from ml_observability.core.mlflow_client import MLflowClient

logger = logging.getLogger(__name__)

# Global instances
_mlflow_client: MLflowClient
_cost_tracker: CostTracker


def initialize(
    cost_rates: Optional[dict] = None,
    experiment_name: Optional[str] = None,
    credential: Optional[ModelhubCredential] = None,
):
    """
    Initialize the MLflowClient, Observability, and CostTracker.
    Must be called once at startup.

    Optionally, specify an experiment_name to set the active MLflow experiment.
    """
    global _mlflow_client, _cost_tracker
    
    if not credential:
        # Create a ModelhubCredential instance using environment variables.
        credential = ModelhubCredential(
            modelhub_url=os.getenv("MODELHUB_BASE_URL"),
            client_id=os.getenv("MODELHUB_CLIENT_ID"),
            client_secret=os.getenv("MODELHUB_CLIENT_SECRET")
        )

    _mlflow_client = MLflowClient(
        credential=credential,
    )
    experiment_name = experiment_name or os.getenv("EXPERIMENT_NAME")
    if experiment_name:
        _mlflow_client.set_experiment(experiment_name=experiment_name)
    _cost_tracker = CostTracker(cost_rates=cost_rates)
    logger.debug("Observability system initialized.")


def monitor(
    client,
    provider: Optional[str] = None,
    cost_rates: Optional[dict] = None,
    experiment_name: Optional[str] = None,
    credential: Optional[ModelhubCredential] = None,
):
    """
    Enable monitoring on an LLM client.
    Supports multiple providers: 'openai', 'azure_openai', 'anthropic', etc.
    If provider is not provided, it is inferred from the client's module.

    You can also provide an experiment_name which will be used to configure MLflow.
    """
    initialize(
        cost_rates=cost_rates,
        experiment_name=experiment_name,
        credential=credential,
    )
    if provider is None:
        # Try checking the class name first.
        client_name = client.__class__.__name__.lower()
        if "azure" in client_name:
            provider = "azure_openai"
        elif "openai" in client_name:
            provider = "openai"
        elif "anthropic" in client_name:
            provider = "anthropic"
        else:
            # Fallback to module-based detection.
            mod = client.__class__.__module__.lower()
            if "openai" in mod:
                provider = "openai"
            elif "azure" in mod:
                provider = "azure_openai"
            elif "anthropic" in mod:
                provider = "anthropic"
            else:
                provider = "unknown"

    logger.debug("Detected provider: %s", provider)

    logger.debug("Provider: %s", provider)

    if provider in ("openai", "azure_openai"):
        _mlflow_client.mlflow.openai.autolog()
        wrap_openai(client)
    elif provider == "anthropic":
        _mlflow_client.mlflow.anthropic.autolog()
        wrap_anthropic(client)
    else:
        logger.warning("Monitoring not implemented for provider %s", provider)


def wrap_openai(client):
    """
    Wraps an OpenAI client to enable monitoring and logging capabilities.
    
    This function intercepts the client's completion creation methods (both synchronous
    and asynchronous) to track costs, log parameters, and manage MLflow runs.

    Args:
        client: An instance of the OpenAI client to be wrapped.

    Returns:
        None. The function modifies the client instance in-place by wrapping its methods.
    """
    # Wrap synchronous completions.create
    if hasattr(client.chat, "completions") and hasattr(client.chat.completions, "create"):
        original_create = client.chat.completions.create

        def wrapped_create(*args, **kwargs):
            active = mlflow.active_run()
            logger.debug("Active run: %s", active)
            started_run = False
            if not active:
                run = mlflow.start_run(run_name="llm_call_auto")
                started_run = True
            else:
                run = active
            try:
                result = original_create(*args, **kwargs)
                logger.debug("result: %s", result)
                prompt_tokens = result.usage.prompt_tokens
                completion_tokens = result.usage.completion_tokens
                _cost_tracker.track_cost(
                    model_name=kwargs.get("model", "gpt-3.5-turbo"),
                    input_tokens=prompt_tokens,
                    output_tokens=completion_tokens,
                    run_id=run.info.run_id
                )
                _mlflow_client.log_param("model", kwargs.get("model", "gpt-3.5-turbo"))
                return result
            finally:
                if started_run:
                    mlflow.end_run()

        client.chat.completions.create = wrapped_create

    # Wrap asynchronous completions.create (create)
    if hasattr(client, "chat") and hasattr(client.chat, "completions"):
        # Check if the client is an AsyncOpenAI instance
        if hasattr(client.chat.completions, "create") and callable(
                client.chat.completions.create) and client.__class__.__name__ == "AsyncOpenAI":
            original_async_create = client.chat.completions.create

            async def wrapped_async_create(*args, **kwargs):
                active = mlflow.active_run()
                logger.debug("Active async run: %s", active)
                started_run = False
                if not active:
                    run = mlflow.start_run(run_name="async_llm_call_auto")
                    started_run = True
                else:
                    run = active

                try:
                    result = original_async_create(*args, **kwargs)
                    prompt_tokens = result.usage.prompt_tokens
                    completion_tokens = result.usage.completion_tokens
                    _cost_tracker.track_cost(
                        model_name=kwargs.get("model", "gpt-3.5-turbo"),
                        input_tokens=prompt_tokens,
                        output_tokens=completion_tokens,
                        run_id=run.info.run_id
                    )
                    _mlflow_client.log_param("model", kwargs.get("model", "gpt-3.5-turbo"))
                    return result
                finally:
                    if started_run:
                        mlflow.end_run()

            client.chat.completions.create = wrapped_async_create

    logger.debug("Monitoring enabled for OpenAI/AzureOpenAI client.")


def wrap_anthropic(client):
    """
    Wraps an Anthropic client to enable monitoring and logging capabilities.
    
    This function intercepts the client's message creation methods (both synchronous
    and asynchronous) to track costs, log parameters, and manage MLflow runs.

    Args:
        client: An instance of the Anthropic client to be wrapped.

    Returns:
        None. The function modifies the client instance in-place by wrapping its methods.
    """
    # Wrap synchronous messages.create.
    if hasattr(client, "messages") and hasattr(client.messages, "create"):
        original_create = client.messages.create

        def wrapped_create(*args, **kwargs):
            active = mlflow.active_run()
            started_run = False
            if not active:
                run = mlflow.start_run(run_name="llm_call_auto")
                started_run = True
            else:
                run = active
            try:
                result = original_create(*args, **kwargs)
                prompt_tokens = result.usage.input_tokens
                completion_tokens = result.usage.output_tokens
                _cost_tracker.track_cost(
                    model_name=kwargs.get("model", "anthropic-default"),
                    input_tokens=prompt_tokens,
                    output_tokens=completion_tokens,
                    run_id=run.info.run_id
                )
                _mlflow_client.log_param("model", kwargs.get("model", "anthropic-default"))
                return result
            finally:
                if started_run:
                    mlflow.end_run()

        client.messages.create = wrapped_create

    # Wrap asynchronous messages.acreate if available.
    if hasattr(client, "messages") and hasattr(client.messages, "acreate"):
        original_acreate = client.messages.acreate

        async def wrapped_acreate(*args, **kwargs):
            active = mlflow.active_run()
            started_run = False
            if not active:
                run = mlflow.start_run(run_name="llm_call_auto")
                started_run = True
            else:
                run = active
            try:
                result = await original_acreate(*args, **kwargs)
                prompt_tokens = result.usage.input_tokens
                completion_tokens = result.usage.output_tokens
                _cost_tracker.track_cost(
                    model_name=kwargs.get("model", "anthropic-default"),
                    input_tokens=prompt_tokens,
                    output_tokens=completion_tokens,
                    run_id=run.info.run_id
                )
                _mlflow_client.log_param("model", kwargs.get("model", "anthropic-default"))
                return result
            finally:
                if started_run:
                    mlflow.end_run()

        client.messages.acreate = wrapped_acreate

    logger.debug("Monitoring enabled for Anthropics client.")


def agent(name=None):
    """
    Decorator for agent functions.
    Automatically wraps the function execution in an MLflow run.
    """

    def decorator(fn):
        def wrapper(*args, **kwargs):
            active = mlflow.active_run()
            started_run = False
            if not active:
                mlflow.start_run(run_name=name or fn.__name__)
                started_run = True
            else:
                run = active
            try:
                return fn(*args, **kwargs)
            finally:
                if started_run:
                    mlflow.end_run()

        return wrapper

    return decorator


def tool(name=None):
    """
    Decorator for tool functions.
    """

    def decorator(fn):
        def wrapper(*args, **kwargs):
            active = mlflow.active_run()
            started_run = False
            if not active:
                run = mlflow.start_run(run_name=name or fn.__name__)
                started_run = True
            else:
                run = active
            try:
                return fn(*args, **kwargs)
            finally:
                if started_run:
                    mlflow.end_run()

        return wrapper

    return decorator


class Identify:
    """
    A simple context manager for setting user context (if needed).
    """

    def __init__(self, user_props=None):
        self.user_props = user_props

    def __enter__(self):
        # Set user context here if desired.
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        # Clear user context.
        pass


def identify(user_props=None):
    """
    Creates and returns an Identify context manager for setting user context.
    
    Args:
        user_props (dict, optional): Dictionary containing user properties to be set
            during the context. Defaults to None.
    
    Returns:
        Identify: A context manager instance that handles user context.
    """
    return Identify(user_props)
