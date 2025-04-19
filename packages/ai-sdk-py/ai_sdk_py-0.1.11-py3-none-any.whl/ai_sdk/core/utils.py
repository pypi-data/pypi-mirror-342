from typing import List, Optional, Tuple
from .types import Message, SystemMessage, UserMessage
import os
import opik
import logging

LOGGER = logging.getLogger(__name__)

@opik.track
def standardize_messages(
    system: Optional[str],
    prompt: Optional[str],
    messages: Optional[List[Message]]
) -> List[Message]:
    if prompt is not None and messages is not None:
        raise ValueError("prompt and messages cannot both be provided")
    res: List[Message] = []

    if system is not None:
        res += [SystemMessage(content=system)]
    
    if prompt is not None:
        res += [UserMessage(content=prompt)]
    
    if messages is not None:
        res +=messages
    
    return res

def load_api_key(
    api_key: Optional[str],
    env_var_name: Optional[str],
    description: str,
    api_key_parameter_name: str = "api_key"
) -> str:
    if api_key is not None:
        return api_key
    
    api_key = os.getenv(env_var_name)

    if api_key is None:
        raise ValueError(f"{description} API key is missing. Pass it using the '{api_key_parameter_name}' parameter or the {env_var_name} environment variable.")
    
    return api_key

def is_opik_configured() -> Tuple[bool, Optional[str]]:
    try:
        import opik
    except ImportError:
        os.environ["OPIK_TRACK_DISABLE"] = "true"
        return False
    
    _client = opik.Opik(_show_misconfiguration_message=False)

    try:
        _client.auth_check()
        return True
    except Exception as e:  # noqa: BLE001
        LOGGER.warning("Opik is not configured, run `opik configure` in your terminal or call `opik.configure()` in your code.")
        return False
