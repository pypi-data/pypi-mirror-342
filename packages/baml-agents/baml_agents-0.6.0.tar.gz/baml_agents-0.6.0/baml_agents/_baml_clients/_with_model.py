import os
from typing import TypeVar

from baml_py import ClientRegistry

T = TypeVar("T")


def with_model(b: T, model: str) -> T:
    """
    Attach a ClientRegistry with a specified or default model to an object supporting with_options.
    """
    cr = ClientRegistry()
    options = {
        "model": model,
        "api_key": os.environ["OPENAI_API_KEY"],
    }
    base_url = os.environ.get("OPENAI_BASE_URL")
    if base_url:
        options["base_url"] = base_url
    cr.add_llm_client(
        name=model,
        provider="openai",
        options=options,
    )
    cr.set_primary(model)
    return b.with_options(client_registry=cr)  # type: ignore
