"""
Aider SDK - Simple Python SDK for using Aider programmatically

This SDK provides an easy way to use Aider, the AI coding assistant,
in your Python scripts without dealing with the underlying complexity.
"""

import os
import json
import uuid
import tempfile
import shutil
import datetime
import requests
import re
from typing import List, Dict, Any, Union, Optional

# Add SecureKeyManager class to handle API keys securely
class SecureKeyManager:
    """
    Manages API keys securely without exposing them through environment variables.

    This class provides a way to securely store and use provider API keys without
    directly setting them as environment variables where they could be easily accessed.
    """

    def __init__(self):
        """Initialize the secure key manager with empty storage."""
        self._provider_keys = {}
        self._original_env = {}

    def set_key(self, provider: str, key: str):
        """Store a provider API key securely."""
        self._provider_keys[provider.lower()] = key

    def get_key(self, provider: str) -> Optional[str]:
        """Get a provider API key securely."""
        return self._provider_keys.get(provider.lower())

    def has_key(self, provider: str) -> bool:
        """Check if a provider API key exists."""
        return provider.lower() in self._provider_keys

    def clear_keys(self):
        """Clear all stored provider API keys."""
        self._provider_keys.clear()

    def providers_with_keys(self) -> List[str]:
        """Get a list of providers that have keys stored."""
        return list(self._provider_keys.keys())

    def save_environment(self):
        """Save original environment variables before modifying them."""
        for env_var in ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "E2B_API_KEY"]:
            self._original_env[env_var] = os.environ.get(env_var)

    def restore_environment(self):
        """Restore original environment variables."""
        for var, value in self._original_env.items():
            if value is not None:
                os.environ[var] = value
            elif var in os.environ:
                del os.environ[var]

# Supported model names (OpenAI)
SUPPORTED_OPENAI_MODELS = [
    "openai/chatgpt-4o-latest",
    "openai/ft:gpt-3.5-turbo",
    "openai/ft:gpt-3.5-turbo-0125",
    "openai/ft:gpt-3.5-turbo-0613",
    "openai/ft:gpt-3.5-turbo-1106",
    "openai/ft:gpt-4-0613",
    "openai/ft:gpt-4o-2024-08-06",
    "openai/ft:gpt-4o-2024-11-20",
    "openai/ft:gpt-4o-mini-2024-07-18",
    "openai/gpt-3.5-turbo",
    "openai/gpt-3.5-turbo-0125",
    "openai/gpt-3.5-turbo-0301",
    "openai/gpt-3.5-turbo-0613",
    "openai/gpt-3.5-turbo-1106",
    "openai/gpt-3.5-turbo-16k",
    "openai/gpt-3.5-turbo-16k-0613",
    "openai/gpt-4",
    "openai/gpt-4-0125-preview",
    "openai/gpt-4-0314",
    "openai/gpt-4-0613",
    "openai/gpt-4-1106-preview",
    "openai/gpt-4-1106-vision-preview",
    "openai/gpt-4-32k",
    "openai/gpt-4-32k-0314",
    "openai/gpt-4-32k-0613",
    "openai/gpt-4-turbo",
    "openai/gpt-4-turbo-2024-04-09",
    "openai/gpt-4-turbo-preview",
    "openai/gpt-4-vision-preview",
    "openai/gpt-4.1",
    "openai/gpt-4.1-2025-04-14",
    "openai/gpt-4.1-mini",
    "openai/gpt-4.1-mini-2025-04-14",
    "openai/gpt-4.1-nano",
    "openai/gpt-4.1-nano-2025-04-14",
    "openai/gpt-4.5-preview",
    "openai/gpt-4.5-preview-2025-02-27",
    "openai/gpt-4o",
    "openai/gpt-4o-2024-05-13",
    "openai/gpt-4o-2024-08-06",
    "openai/gpt-4o-2024-11-20",
    "openai/gpt-4o-audio-preview",
    "openai/gpt-4o-audio-preview-2024-10-01",
    "openai/gpt-4o-audio-preview-2024-12-17",
    "openai/gpt-4o-mini",
    "openai/gpt-4o-mini-2024-07-18",
    "openai/gpt-4o-mini-audio-preview-2024-12-17",
    "openai/gpt-4o-mini-realtime-preview",
    "openai/gpt-4o-mini-realtime-preview-2024-12-17",
    "openai/gpt-4o-mini-search-preview",
    "openai/gpt-4o-mini-search-preview-2025-03-11",
    "openai/gpt-4o-realtime-preview",
    "openai/gpt-4o-realtime-preview-2024-10-01",
    "openai/gpt-4o-realtime-preview-2024-12-17",
    "openai/gpt-4o-search-preview",
    "openai/gpt-4o-search-preview-2025-03-11",
    "openai/o1",
    "openai/o1-2024-12-17",
    "openai/o1-mini",
    "openai/o1-mini-2024-09-12",
    "openai/o1-preview",
    "openai/o1-preview-2024-09-12",
    "openai/o3",
    "openai/o3-2025-04-16",
    "openai/o3-mini",
    "openai/o3-mini-2025-01-31",
    "openai/o4-mini",
    "openai/o4-mini-2025-04-16",
]

# Supported model names (Anthropic)
SUPPORTED_ANTHROPIC_MODELS = [
    "anthropic/claude-2",
    "anthropic/claude-2.1",
    "anthropic/claude-3-5-haiku-20241022",
    "anthropic/claude-3-5-haiku-latest",
    "anthropic/claude-3-5-sonnet-20240620",
    "anthropic/claude-3-5-sonnet-20241022",
    "anthropic/claude-3-5-sonnet-latest",
    "anthropic/claude-3-7-sonnet-20250219",
    "anthropic/claude-3-7-sonnet-latest",
    "anthropic/claude-3-haiku-20240307",
    "anthropic/claude-3-opus-20240229",
    "anthropic/claude-3-opus-latest",
    "anthropic/claude-3-sonnet-20240229",
    "anthropic/claude-instant-1",
    "anthropic/claude-instant-1.2",
]

# Built-in aliases
MODEL_ALIASES = {
    # OpenAI GPT-3.5
    "3": "openai/gpt-3.5-turbo",
    "35-turbo": "openai/gpt-3.5-turbo",
    "35turbo": "openai/gpt-3.5-turbo",
    "gpt-3.5-turbo": "openai/gpt-3.5-turbo",
    "gpt-3.5-turbo-0125": "openai/gpt-3.5-turbo-0125",
    "gpt-3.5-turbo-0301": "openai/gpt-3.5-turbo-0301",
    "gpt-3.5-turbo-0613": "openai/gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-1106": "openai/gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-16k": "openai/gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-16k-0613": "openai/gpt-3.5-turbo-16k-0613",

    # OpenAI GPT-4
    "4": "openai/gpt-4-0613",
    "gpt-4": "openai/gpt-4",
    "gpt-4-0125-preview": "openai/gpt-4-0125-preview",
    "gpt-4-0314": "openai/gpt-4-0314",
    "gpt-4-0613": "openai/gpt-4-0613",
    "gpt-4-1106-preview": "openai/gpt-4-1106-preview",
    "gpt-4-1106-vision-preview": "openai/gpt-4-1106-vision-preview",
    "gpt-4-32k": "openai/gpt-4-32k",
    "gpt-4-32k-0314": "openai/gpt-4-32k-0314",
    "gpt-4-32k-0613": "openai/gpt-4-32k-0613",
    "gpt-4-turbo": "openai/gpt-4-turbo",
    "gpt-4-turbo-2024-04-09": "openai/gpt-4-turbo-2024-04-09",
    "gpt-4-turbo-preview": "openai/gpt-4-turbo-preview",
    "gpt-4-vision-preview": "openai/gpt-4-vision-preview",
    "4-turbo": "openai/gpt-4-1106-preview",

    # OpenAI GPT-4.1
    "gpt-4.1": "openai/gpt-4.1",
    "gpt-4.1-2025-04-14": "openai/gpt-4.1-2025-04-14",
    "gpt-4.1-mini": "openai/gpt-4.1-mini",
    "gpt-4.1-mini-2025-04-14": "openai/gpt-4.1-mini-2025-04-14",
    "gpt-4.1-nano": "openai/gpt-4.1-nano",
    "gpt-4.1-nano-2025-04-14": "openai/gpt-4.1-nano-2025-04-14",

    # OpenAI GPT-4.5
    "gpt-4.5-preview": "openai/gpt-4.5-preview",
    "gpt-4.5-preview-2025-02-27": "openai/gpt-4.5-preview-2025-02-27",

    # OpenAI GPT-4o
    "4o": "openai/gpt-4o",
    "gpt-4o": "openai/gpt-4o",
    "gpt-4o-2024-05-13": "openai/gpt-4o-2024-05-13",
    "gpt-4o-2024-08-06": "openai/gpt-4o-2024-08-06",
    "gpt-4o-2024-11-20": "openai/gpt-4o-2024-11-20",
    "gpt-4o-audio-preview": "openai/gpt-4o-audio-preview",
    "gpt-4o-audio-preview-2024-10-01": "openai/gpt-4o-audio-preview-2024-10-01",
    "gpt-4o-audio-preview-2024-12-17": "openai/gpt-4o-audio-preview-2024-12-17",
    "gpt-4o-mini": "openai/gpt-4o-mini",
    "gpt-4o-mini-2024-07-18": "openai/gpt-4o-mini-2024-07-18",
    "gpt-4o-mini-audio-preview-2024-12-17": "openai/gpt-4o-mini-audio-preview-2024-12-17",
    "gpt-4o-mini-realtime-preview": "openai/gpt-4o-mini-realtime-preview",
    "gpt-4o-mini-realtime-preview-2024-12-17": "openai/gpt-4o-mini-realtime-preview-2024-12-17",
    "gpt-4o-mini-search-preview": "openai/gpt-4o-mini-search-preview",
    "gpt-4o-mini-search-preview-2025-03-11": "openai/gpt-4o-mini-search-preview-2025-03-11",
    "gpt-4o-realtime-preview": "openai/gpt-4o-realtime-preview",
    "gpt-4o-realtime-preview-2024-10-01": "openai/gpt-4o-realtime-preview-2024-10-01",
    "gpt-4o-realtime-preview-2024-12-17": "openai/gpt-4o-realtime-preview-2024-12-17",
    "gpt-4o-search-preview": "openai/gpt-4o-search-preview",
    "gpt-4o-search-preview-2025-03-11": "openai/gpt-4o-search-preview-2025-03-11",

    # OpenAI o1/o3/o4
    "o1": "openai/o1",
    "o1-2024-12-17": "openai/o1-2024-12-17",
    "o1-mini": "openai/o1-mini",
    "o1-mini-2024-09-12": "openai/o1-mini-2024-09-12",
    "o1-preview": "openai/o1-preview",
    "o1-preview-2024-09-12": "openai/o1-preview-2024-09-12",
    "o3": "openai/o3",
    "o3-2025-04-16": "openai/o3-2025-04-16",
    "o3-mini": "openai/o3-mini",
    "o3-mini-2025-01-31": "openai/o3-mini-2025-01-31",
    "o4-mini": "openai/o4-mini",
    "o4-mini-2025-04-16": "openai/o4-mini-2025-04-16",

    # Anthropic (existing)
    "haiku": "anthropic/claude-3-5-haiku-20241022",
    "opus": "anthropic/claude-3-opus-20240229",
    "sonnet": "anthropic/claude-3-7-sonnet-20250219",
}


ALL_SUPPORTED_MODELS = set(SUPPORTED_OPENAI_MODELS + SUPPORTED_ANTHROPIC_MODELS)
ALL_MODEL_ALIASES = set(MODEL_ALIASES.keys())

class Local:
    """
    Main class for interacting with Aider programmatically.

    This SDK allows you to easily use Aider to:
    - Perform AI coding tasks with specific files and prompts
    - List available AI models
    - Work with files in a git repository
    - Use architect mode for a two-model workflow (planner + editor)
    """

    # Constants
    LMSYS_API_URL = "https://lmsys-sdk-backend-4827e6075b7e.herokuapp.com"
    # LMSYS_API_URL = "http://localhost:8000"
    SUPPORTED_PROVIDERS = ["openai", "anthropic"]

    def __init__(
        self,
        working_dir: str,
        model: str = "gpt-4.1-nano",
        editor_model: Optional[str] = None,
        use_git: bool = False,
        api_key: Optional[str] = None,
        api_keys: Optional[Dict[str, str]] = None,  # For backward compatibility
        architect_mode: bool = False,
        weak_model: Optional[str] = None,
        session_id: Optional[str] = None  # Add session_id parameter
    ):
        """
        Initialize the Aider SDK.

        Args:
            working_dir: Path to the git repository directory where operations will occur
            model: The AI model to use for coding tasks (default: gpt-4)
            editor_model: Optional separate model for editing operations
            use_git: Whether to use git for tracking changes (default: True)
            api_key: LMSYS API key for authentication (preferred method)
            api_keys: Dictionary of API keys for various providers (legacy method)
            architect_mode: Whether to use architect mode (planner + editor workflow)
            weak_model: Optional planner model to use in architect mode (defaults to the main model if None)
            session_id: Optional session ID for tracking usage across API calls (auto-generated if None)
        """
        from aider.models import Model
        from aider.coders import Coder
        from aider.io import InputOutput

        self.working_dir = os.path.abspath(working_dir)
        self.original_dir = os.getcwd()  # Store the original working directory
        self.model_name = model
        self.editor_model_name = editor_model
        self.weak_model_name = weak_model
        self.use_git = use_git
        self.architect_mode = architect_mode
        self.session_token = None
        self.token_expires_at = None

        # Initialize or use provided session ID for usage tracking
        self.session_id = session_id or str(uuid.uuid4())

        # Initialize cost tracking
        self.cost_history = []

        # Initialize credit info
        self.credits = None
        self.credit_limit = None

        # Initialize secure key manager
        self.key_manager = SecureKeyManager()
        self.key_manager.save_environment()

        # Validate model provider
        self._validate_model_provider(model)
        if editor_model:
            self._validate_model_provider(editor_model)
        if weak_model:
            self._validate_model_provider(weak_model)

        # Authentication - either use LMSYS API key or legacy API keys
        if api_key:
            self._authenticate_with_lmsys(api_key)
        elif api_keys:
            # Legacy method: Set API keys directly but only from the provided dict
            self._set_api_keys(api_keys)
        else:
            # No API keys provided - must require authentication
            raise ValueError("API key must be provided to use the SDK. Please provide api_key parameter.")

        # Validate that working_dir is a git repository if use_git is True
        if use_git:
            self._validate_git_repo()

        # Set up the chat history file path
        self.chat_history_file = os.path.join(self.working_dir, ".aider.chat.history.md")

        # Initialize the model with appropriate settings
        if architect_mode:
            # In architect mode, we need to set up both the weak model (planner) and editor model
            self.model = Model(
                model=model,
                weak_model=weak_model if weak_model else model,
                editor_model=editor_model if editor_model else model
            )
        elif editor_model:
            # Regular mode with editor model specified
            self.model = Model(model=model, editor_model=editor_model)
        else:
            # Regular mode with just main model
            self.model = Model(model)

        # Initialize input/output handler
        self.io = InputOutput(yes=True, chat_history_file=self.chat_history_file)

        # Get initial credit information if authenticated
        if self.session_token:
            try:
                self._get_credit_info()
            except Exception as e:
                print(f"Warning: Failed to get credit information: {str(e)}")

    def _clear_provider_env_vars(self):
        """Clear provider API keys from environment variables to ensure we only use keys from the database."""
        provider_env_vars = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY", "E2B_API_KEY"]
        for var in provider_env_vars:
            if var in os.environ:
                del os.environ[var]

        # Also clear secure key manager
        self.key_manager.clear_keys()

    def _validate_model_provider(self, model_name: str) -> None:
        """
        Validate that the model is supported, including aliases.
        """
        model_name = model_name.lower()
        # Resolve alias if present
        resolved = MODEL_ALIASES.get(model_name, model_name)
        if resolved not in ALL_SUPPORTED_MODELS:
            raise ValueError(
                f"Model '{model_name}' is not supported. Supported models: {sorted(ALL_SUPPORTED_MODELS)}. "
                f"You may also use these aliases: {sorted(ALL_MODEL_ALIASES)}"
            )

    def _authenticate_with_lmsys(self, api_key: str) -> None:
        """
        Authenticate with the LMSYS API server and get a session token.

        Args:
            api_key: The LMSYS API key for authentication

        Raises:
            ValueError: If authentication fails
        """
        try:
            # Authenticate with LMSYS API
            response = requests.post(
                f"{self.LMSYS_API_URL}/authenticate",
                json={"api_key": api_key}
            )

            if response.status_code != 200:
                raise ValueError(f"Authentication failed: {response.text}")

            data = response.json()
            self.session_token = data.get("token")
            self.token_expires_at = datetime.datetime.fromisoformat(data.get("expires_at"))

            # Get provider API keys
            self._get_provider_keys()

            # Get credit information
            self._get_credit_info()

        except Exception as e:
            raise ValueError(f"Failed to authenticate with LMSYS API: {str(e)}")

    def _get_provider_keys(self) -> None:
        """
        Fetch provider API keys from the LMSYS API server using the session token.
        Will store keys securely in the key manager rather than exposing them as environment variables.

        Raises:
            ValueError: If fetching keys fails
        """
        if not self.session_token:
            raise ValueError("No session token available. Authentication is required to get provider keys.")

        try:
            # Check if token needs refresh
            if self.token_expires_at and datetime.datetime.now() >= self.token_expires_at:
                self._refresh_token()

            # Clear any existing provider API keys
            self._clear_provider_env_vars()

            # Fetch provider keys
            response = requests.get(
                f"{self.LMSYS_API_URL}/getKeys",
                params={"providers": self.SUPPORTED_PROVIDERS},
                headers={"Authorization": f"Bearer {self.session_token}"}
            )

            if response.status_code != 200:
                raise ValueError(f"Failed to fetch provider keys: {response.text}")

            provider_keys = response.json()

            # Store provider keys securely
            for provider, key in provider_keys.items():
                self.key_manager.set_key(provider, key)

                # Temporarily set environment variables for compatibility
                if provider == "openai":
                    os.environ["OPENAI_API_KEY"] = key
                elif provider == "anthropic":
                    os.environ["ANTHROPIC_API_KEY"] = key
                elif provider == "e2b":
                    os.environ["E2B_API_KEY"] = key

        except Exception as e:
            raise ValueError(f"Failed to fetch provider keys from database: {str(e)}")

    def _refresh_token(self) -> None:
        """
        Refresh the session token.

        Raises:
            ValueError: If token refresh fails
        """
        if not self.session_token:
            return

        try:
            response = requests.post(
                f"{self.LMSYS_API_URL}/refreshToken",
                headers={"Authorization": f"Bearer {self.session_token}"}
            )

            if response.status_code != 200:
                raise ValueError(f"Token refresh failed: {response.text}")

            data = response.json()
            self.session_token = data.get("token")
            self.token_expires_at = datetime.datetime.fromisoformat(data.get("expires_at"))

        except Exception as e:
            raise ValueError(f"Failed to refresh token: {str(e)}")

    def _set_api_keys(self, api_keys: Dict[str, str]):
        """
        Store API keys securely using the key manager.
        This is a legacy method and is only used if no LMSYS API key is provided.
        """
        # Common API key environment variable names
        supported_keys = [
            "OPENAI_API_KEY",
            "ANTHROPIC_API_KEY",
            "E2B_API_KEY"
        ]

        # Clear existing provider keys first
        self._clear_provider_env_vars()

        # Set keys in the secure key manager for all provided API keys
        for key, value in api_keys.items():
            # Ensure the key is in uppercase format
            env_key = key.upper()
            # If the key doesn't already include "_API_KEY", add it for standard format
            if not env_key.endswith("_API_KEY") and env_key not in ["OLLAMA_HOST"]:
                if "_" not in env_key:
                    env_key = f"{env_key}_API_KEY"

            # Map environment variable names to provider names
            provider_map = {
                "OPENAI_API_KEY": "openai",
                "ANTHROPIC_API_KEY": "anthropic",
                "E2B_API_KEY": "e2b"
            }

            # Only set supported provider keys
            if env_key in supported_keys:
                # Store in secure key manager
                provider = provider_map.get(env_key, env_key.lower().replace("_api_key", ""))
                self.key_manager.set_key(provider, value)

                # Temporarily set environment variable for compatibility
                os.environ[env_key] = value


    def _validate_git_repo(self):
        """Validate that the working directory is a git repository."""
        import subprocess

        try:
            result = subprocess.run(
                ["git", "-C", self.working_dir, "rev-parse", "--is-inside-work-tree"],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode != 0 or result.stdout.strip() != "true":
                raise ValueError(
                    f"The specified directory '{self.working_dir}' is not a git repository: {result.stderr.strip()}"
                )
        except subprocess.SubprocessError as e:
            raise ValueError(f"Error checking git repository: {str(e)}")

    def list_models(self, substring: str = "") -> List[str]:
        """
        List available AI models and aliases that match the provided substring.
        """
        models = list(ALL_SUPPORTED_MODELS) + list(ALL_MODEL_ALIASES)
        if substring:
            substring = substring.lower()
            return [m for m in models if substring in m.lower()]
        return sorted(models)

    def _extract_cost_info(self, result: Any) -> Optional[Dict[str, Any]]:
        """
        Extract cost information from the result object returned by Aider.

        Args:
            result: The result object from coder.run()

        Returns:
            Dictionary with cost information or None if not available
        """
        cost_info = {}

        # Check if we're in architect mode and have access to both planner and editor costs
        if hasattr(result, 'architect_costs') and result.architect_costs is not None:
            # Architect mode has separate costs for planner and editor
            planner_cost = result.architect_costs.get('planner_cost', 0)
            editor_cost = result.architect_costs.get('editor_cost', 0)

            cost_info['message_cost'] = planner_cost + editor_cost
            cost_info['planner_cost'] = planner_cost
            cost_info['editor_cost'] = editor_cost

            # If there's session cost information
            if 'planner_session_cost' in result.architect_costs and 'editor_session_cost' in result.architect_costs:
                cost_info['session_cost'] = result.architect_costs.get('planner_session_cost', 0) + result.architect_costs.get('editor_session_cost', 0)

            # Check for tokens
            if 'planner_tokens' in result.architect_costs and 'editor_tokens' in result.architect_costs:
                planner_tokens = result.architect_costs.get('planner_tokens', {})
                editor_tokens = result.architect_costs.get('editor_tokens', {})

                # Combine token counts
                combined_tokens = {}
                if isinstance(planner_tokens, dict) and isinstance(editor_tokens, dict):
                    combined_tokens['input'] = planner_tokens.get('input', 0) + editor_tokens.get('input', 0)
                    combined_tokens['output'] = planner_tokens.get('output', 0) + editor_tokens.get('output', 0)
                    cost_info['tokens'] = combined_tokens

            return cost_info

        # Standard mode cost extraction (non-architect)
        # Check if the result has a last_message_cost
        if hasattr(result, 'last_message_cost') and result.last_message_cost is not None:
            cost_info['message_cost'] = result.last_message_cost

        # Check if the result has a last_tokens
        if hasattr(result, 'last_tokens') and result.last_tokens is not None:
            if isinstance(result.last_tokens, dict):
                cost_info['tokens'] = result.last_tokens
            elif hasattr(result.last_tokens, '__dict__'):
                cost_info['tokens'] = result.last_tokens.__dict__

        # Check if the result has a session_cost
        if hasattr(result, 'session_cost') and result.session_cost is not None:
            cost_info['session_cost'] = result.session_cost

        # If we extracted any cost info, return it
        if cost_info:
            return cost_info

        # Try to parse cost information from the chat history
        try:
            with open(self.chat_history_file, 'r') as f:
                chat_history = f.read()
                import re
                # Look for cost information patterns in the chat history
                cost_matches = re.findall(r"Cost: \$([\d.]+) message, \$([\d.]+) session", chat_history)
                if cost_matches:
                    latest_match = cost_matches[-1]  # Get the most recent cost entry
                    return {
                        'message_cost': float(latest_match[0]),
                        'session_cost': float(latest_match[1])
                    }
        except Exception:
            pass

        return None if not cost_info else cost_info

    def _calculate_marked_up_cost(self, cost_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Apply a 20% markup to the cost information.

        Args:
            cost_info: Dictionary with original cost information

        Returns:
            Dictionary with original and marked-up cost information
        """
        if not cost_info:
            return {}

        marked_up = cost_info.copy()

        # Apply 20% markup to message_cost if present
        if 'message_cost' in marked_up:
            marked_up['marked_up_message_cost'] = marked_up['message_cost'] * 1.2

        # Apply 20% markup to session_cost if present
        if 'session_cost' in marked_up:
            marked_up['marked_up_session_cost'] = marked_up['session_cost'] * 1.2

        return marked_up

    def _log_usage_and_update_billing(self, cost_info: Dict[str, Any]) -> None:
        """
        Log usage and update billing information on the LMSYS API server.

        Args:
            cost_info: Dictionary with cost information (original and marked-up)
        """
        if not self.session_token or not cost_info:
            return

        try:
            # Check if token needs refresh
            if self.token_expires_at and datetime.datetime.now() >= self.token_expires_at:
                self._refresh_token()

            # Get provider and model information
            provider = self._get_provider_from_model(self.model_name)

            # Calculate total costs for the session (without markup, we'll apply it manually)
            total_costs = self.get_total_cost(include_current=True, current_cost=cost_info, include_markup=False)
            raw_combined_total = total_costs['total_cost']

            # Apply 20% markup for billing
            marked_up_combined_total = raw_combined_total * 1.2

            # For architect mode, we need to account for both planner and editor models
            model_info = self.model_name
            if self.architect_mode:
                model_info = f"{self.model_name} (planner) + {self.editor_model_name or self.model_name} (editor)"

            # Log usage with total session costs - use combined total as the primary cost
            usage_data = {
                "provider": provider,
                "model": model_info,
                "cost": raw_combined_total,  # Raw combined total
                "marked_up_cost": marked_up_combined_total,  # Marked-up combined total
                "total_session_cost": raw_combined_total,
                "marked_up_session_cost": marked_up_combined_total,
                "session_id": self.session_id
            }

            # Add tokens if available
            if 'tokens' in cost_info:
                tokens_info = cost_info['tokens']
                total_tokens = 0
                if isinstance(tokens_info, dict):
                    # Sum up input and output tokens if available
                    total_tokens = tokens_info.get('input', 0) + tokens_info.get('output', 0)
                usage_data["tokens"] = total_tokens

            # Send usage data to LMSYS API
            response = requests.post(
                f"{self.LMSYS_API_URL}/logUsage",
                json=usage_data,
                headers={"Authorization": f"Bearer {self.session_token}"}
            )

            if response.status_code != 200:
                print(f"Warning: Failed to log usage: {response.text}")
                return

            # Update billing with the combined total cost
            billing_data = {
                "cost": marked_up_combined_total  # Use marked-up combined total for billing
            }

            response = requests.post(
                f"{self.LMSYS_API_URL}/updateBilling",
                json=billing_data,
                headers={"Authorization": f"Bearer {self.session_token}"}
            )

            if response.status_code == 402:
                # Credit limit reached
                print("WARNING: Insufficient credits. Please purchase more credits to continue using the service.")
                print("Visit the account page to add more credits to your account.")
                raise ValueError("Insufficient credits. Please purchase more credits to continue using the service.")
            elif response.status_code != 200:
                print(f"Warning: Failed to update billing: {response.text}")
            else:
                # Update local credit info
                billing_response = response.json()
                self.credits = billing_response.get("credits", 0.0)
                self.credit_limit = billing_response.get("credit_limit", 0.0)

        except Exception as e:
            if "Insufficient credits" in str(e):
                raise  # Re-raise credit-related errors
            print(f"Warning: Failed to log usage or update billing: {str(e)}")

    def _get_provider_from_model(self, model_name: str) -> str:
        """
        Determine the provider from the model name or alias.
        """
        model_name = model_name.lower()
        resolved = MODEL_ALIASES.get(model_name, model_name)
        if resolved in SUPPORTED_OPENAI_MODELS:
            return "openai"
        if resolved in SUPPORTED_ANTHROPIC_MODELS:
            return "anthropic"
        # Default to openai if we can't determine
        return "openai"

    def code(
        self,
        prompt: str,
        editable_files: List[str],
        readonly_files: List[str] = None,
    ) -> Dict[str, Any]:
        """
        Run an AI coding task with the specified prompt and files.

        Args:
            prompt: Natural language instruction for the AI coding task
            editable_files: List of files that can be modified by the AI
            readonly_files: List of files that can be read but not modified

        Returns:
            Dictionary with 'success' boolean, 'diff' string showing changes, and cost information
        """
        from aider.coders import Coder
        from aider.llm import litellm
        import inspect

        # Ensure readonly_files is a list
        if readonly_files is None:
            readonly_files = []

        # Check if user has sufficient credits
        # We'll use a small estimated cost for the check
        estimated_cost = 0.1  # $0.10 estimated cost
        if not self.check_credits_sufficient(estimated_cost):
            raise ValueError(
                f"Insufficient credits. You have ${self.credits:.2f} remaining. "
                f"This operation requires approximately ${estimated_cost:.2f}. "
                f"Please purchase more credits to continue using the service."
            )

        # Convert relative paths to absolute paths
        abs_editable_files = [
            os.path.join(self.working_dir, file) if not os.path.isabs(file) else file
            for file in editable_files
        ]

        abs_readonly_files = [
            os.path.join(self.working_dir, file) if not os.path.isabs(file) else file
            for file in readonly_files
        ]

        # Configure secure API key handling for Aider
        # This is a key security improvement - we'll monkey patch litellm to use our secure keys
        if hasattr(litellm, "_construct_completion_url"):
            original_construct_fn = litellm._construct_completion_url

            def secure_construct_completion_url(*args, **kwargs):
                provider = kwargs.get("provider") or (args[0] if len(args) > 0 else None)
                # Check if we have a secure key for this provider
                if provider and self.key_manager.has_key(provider):
                    # We'll still use the environment variable approach but only temporarily
                    # This is safer than modifying internal litellm functions extensively
                    key = self.key_manager.get_key(provider)
                    env_var = f"{provider.upper()}_API_KEY"
                    if env_var not in os.environ:
                        os.environ[env_var] = key
                return original_construct_fn(*args, **kwargs)

            # Apply our patch
            litellm._construct_completion_url = secure_construct_completion_url

        # Always refresh provider keys before running a coding task to ensure we're using the latest keys
        if self.session_token:
            self._get_provider_keys()
        else:
            # No session token available, but we might have keys set directly
            if not any(self.key_manager.has_key(provider) for provider in ["openai", "anthropic"]):
                raise ValueError("No API keys available. Authentication is required to run coding tasks.")

        # Save the current working directory
        original_working_dir = os.getcwd()

        try:
            # Change to the specified working directory
            print(f"Changing working directory to: {self.working_dir}")
            os.chdir(self.working_dir)

            # Create the coder instance with appropriate settings
            if self.architect_mode:
                # In architect mode, we need to specify the edit_format
                coder = Coder.create(
                    main_model=self.model,
                    io=self.io,
                    fnames=abs_editable_files,
                    read_only_fnames=abs_readonly_files,
                    auto_commits=False,
                    suggest_shell_commands=False,
                    detect_urls=False,
                    use_git=self.use_git,
                    edit_format="architect"  # Enable architect workflow
                )
            else:
                # Regular mode
                coder = Coder.create(
                    main_model=self.model,
                    io=self.io,
                    fnames=abs_editable_files,
                    read_only_fnames=abs_readonly_files,
                    auto_commits=False,
                    suggest_shell_commands=False,
                    detect_urls=False,
                    use_git=self.use_git,
                )

            # Run the coding session
            result = coder.run(prompt)

            # Extract cost information if available
            cost_info = self._extract_cost_info(result)

            if cost_info:
                # Apply 20% markup
                marked_up_cost_info = self._calculate_marked_up_cost(cost_info)

                # Log usage and update billing if we have a session token
                if self.session_token:
                    self._log_usage_and_update_billing(marked_up_cost_info)

                # Record in cost history
                self.cost_history.append({
                    "timestamp": datetime.datetime.now().isoformat(),
                    "prompt": prompt,
                    "files": editable_files,
                    "cost": cost_info,
                    "marked_up_cost": marked_up_cost_info,
                    "architect_mode": self.architect_mode
                })

            # Check for changes in the files and create a diff
            diff = self._get_changes_diff()

            # Check if there were meaningful changes
            success = self._check_for_meaningful_changes(editable_files)

            # Clean up by restoring litellm's original function if we modified it
            if hasattr(litellm, "_construct_completion_url") and litellm._construct_completion_url != original_construct_fn:
                litellm._construct_completion_url = original_construct_fn

            return {
                "success": success,
                "diff": diff,
                "result": result,
                "cost": cost_info,
                "marked_up_cost": marked_up_cost_info if cost_info else None,
                "credits_remaining": self.credits
            }
        except Exception as e:
            # Clean up by restoring litellm's original function if we modified it
            if 'original_construct_fn' in locals() and hasattr(litellm, "_construct_completion_url"):
                litellm._construct_completion_url = original_construct_fn

            if "Insufficient credits" in str(e):
                # Special handling for credit-related errors
                return {
                    "success": False,
                    "error": str(e),
                    "credits_remaining": self.credits,
                    "needs_payment": True
                }
            # Re-raise other exceptions
            raise
        finally:
            # Restore the original working directory
            print(f"Restoring working directory to: {original_working_dir}")
            os.chdir(original_working_dir)

    def _get_changes_diff(self) -> str:
        """Get the git diff or file content if git fails."""
        import subprocess

        if not self.use_git:
            return "Git not enabled. File contents not shown."

        try:
            # Use absolute path with -C option to ensure git runs in the correct directory
            diff_cmd = f"git -C {self.working_dir} diff"
            diff = subprocess.check_output(
                diff_cmd, shell=True, text=True, stderr=subprocess.PIPE
            )
            return diff
        except subprocess.CalledProcessError as e:
            return f"Error getting git diff: {e.stderr.strip()}"

    def _check_for_meaningful_changes(self, relative_editable_files: List[str]) -> bool:
        """Check if the edited files contain meaningful content."""
        for file_path in relative_editable_files:
            full_path = os.path.join(self.working_dir, file_path) if not os.path.isabs(file_path) else file_path

            if os.path.exists(full_path):
                try:
                    with open(full_path, "r") as f:
                        content = f.read()
                        # Check if the file has more than just whitespace
                        stripped_content = content.strip()
                        if stripped_content and (
                            len(stripped_content.split("\n")) > 1
                            or any(
                                kw in content
                                for kw in [
                                    "def ",
                                    "class ",
                                    "import ",
                                    "from ",
                                    "async def",
                                ]
                            )
                        ):
                            return True
                except Exception:
                    continue

        return False

    def create_file(self, file_path: str, content: str) -> bool:
        """
        Create a new file with the specified content.

        Args:
            file_path: Path to the file to create (relative to working_dir)
            content: Content to write to the file

        Returns:
            True if successful, False otherwise
        """
        if isinstance(self, SandboxSDK):
            # If this is a SandboxSDK instance, write directly to the sandbox
            full_path = os.path.join(self.working_dir, file_path) if not os.path.isabs(file_path) else file_path
            try:
                # Ensure the directory exists
                dir_path = os.path.dirname(full_path)
                if dir_path:
                    self.sandbox.commands.run(f"mkdir -p {dir_path}")

                # Write the file using both methods to ensure it works
                # Method 1: Write using the SDK
                self.sandbox.files.write(full_path, content)

                # Method 2: Also write using a command for reliability
                # Create a temporary file with the content, then use cat to write it
                import tempfile
                with tempfile.NamedTemporaryFile(mode='w', delete=False) as temp:
                    temp.write(content)
                    temp_path = temp.name

                # Upload the temp file to the sandbox
                sandbox_temp = f"/tmp/{os.path.basename(temp_path)}"
                self.sandbox.files.write(sandbox_temp, open(temp_path, 'rb').read())

                # Use cat to write the file (more reliable for some environments)
                self.sandbox.commands.run(f"cat {sandbox_temp} > {full_path}")
                self.sandbox.commands.run(f"rm {sandbox_temp}")

                # Clean up the local temp file
                os.unlink(temp_path)

                # Verify the file exists
                if not self._file_exists_in_sandbox(full_path):
                    print(f"Warning: File {full_path} doesn't appear to exist after creation attempts.")
                    return False

                return True
            except Exception as e:
                print(f"Error creating file in sandbox: {str(e)}")
                return False
        else:
            # Original behavior for non-sandbox instance
            full_path = os.path.join(self.working_dir, file_path) if not os.path.isabs(file_path) else file_path

            try:
                # Create directories if they don't exist
                os.makedirs(os.path.dirname(full_path), exist_ok=True)

                with open(full_path, "w") as f:
                    f.write(content)

                return True
            except Exception:
                return False

    def read_file(self, file_path: str) -> Optional[str]:
        """
        Read the content of a file.

        Args:
            file_path: Path to the file to read (relative to working_dir)

        Returns:
            Content of the file, or None if the file doesn't exist
        """
        full_path = os.path.join(self.working_dir, file_path) if not os.path.isabs(file_path) else file_path

        try:
            with open(full_path, "r") as f:
                return f.read()
        except Exception:
            return None

    def search_files(self, query: str, file_patterns: List[str] = None) -> Dict[str, List[str]]:
        """
        Search for matches in files.

        Args:
            query: String to search for
            file_patterns: List of glob patterns to limit the search to

        Returns:
            Dictionary with file paths as keys and lists of matching lines as values
        """
        import glob
        import re

        results = {}

        if file_patterns is None:
            # Default to all files
            file_patterns = ["**/*"]

        for pattern in file_patterns:
            pattern_path = os.path.join(self.working_dir, pattern)
            for file_path in glob.glob(pattern_path, recursive=True):
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, "r") as f:
                            content = f.read()
                            matches = re.findall(r".*" + re.escape(query) + r".*", content, re.MULTILINE)
                            if matches:
                                rel_path = os.path.relpath(file_path, self.working_dir)
                                results[rel_path] = matches
                    except Exception:
                        continue

        return results

    def code_headless(
        self,
        prompt: str,
        editable_files: List[str],
        readonly_files: List[str] = None,
        task_id: str = None
    ) -> Dict[str, Any]:
        """
        Run an AI coding task in headless mode without waiting for the result.

        This function starts the coding process and immediately returns a task ID
        that can be used later to check the status or retrieve results.

        Args:
            prompt: Natural language instruction for the AI coding task
            editable_files: List of files that can be modified by the AI
            readonly_files: List of files that can be read but not modified
            task_id: Optional identifier for the task (auto-generated if None)

        Returns:
            Dictionary with 'task_id' string to identify the task and 'status' string
        """
        import threading
        import uuid
        import datetime

        # Generate a task ID if not provided
        if task_id is None:
            task_id = str(uuid.uuid4())

        # Store the task status in a shared dictionary
        if not hasattr(self, '_headless_tasks'):
            self._headless_tasks = {}

        self._headless_tasks[task_id] = {
            "status": "pending",
            "result": None,
            "started_at": datetime.datetime.now().isoformat(),
            "architect_mode": self.architect_mode,  # Track whether it's in architect mode
            "cost": None  # Will be populated when task completes
        }

        # Start the coding task in a separate thread
        def run_coding_task():
            try:
                result = self.code(prompt, editable_files, readonly_files)
                self._headless_tasks[task_id] = {
                    "status": "completed",
                    "result": result,
                    "architect_mode": self.architect_mode,
                    "completed_at": datetime.datetime.now().isoformat(),
                    "cost": result.get("cost")
                }
            except Exception as e:
                self._headless_tasks[task_id] = {
                    "status": "failed",
                    "error": str(e),
                    "architect_mode": self.architect_mode,
                    "completed_at": datetime.datetime.now().isoformat(),
                    "cost": None
                }

        # Start the thread
        thread = threading.Thread(target=run_coding_task)
        thread.daemon = True
        thread.start()

        return {
            "task_id": task_id,
            "status": "pending",
            "architect_mode": self.architect_mode
        }

    def get_headless_task_status(self, task_id: str) -> Dict[str, Any]:
        """
        Get the status of a headless coding task.

        Args:
            task_id: The ID of the task to check

        Returns:
            Dictionary with task status information
        """
        if not hasattr(self, '_headless_tasks') or task_id not in self._headless_tasks:
            return {
                "status": "not_found",
                "error": f"Task with ID {task_id} not found"
            }

        return self._headless_tasks[task_id]

    def get_cost_history(self) -> List[Dict[str, Any]]:
        """
        Get the history of costs for all runs.

        Returns:
            List of dictionaries with cost information for each run
        """
        return self.cost_history

    def get_total_cost(self, include_current: bool = False, current_cost: Optional[Dict[str, float]] = None, include_markup: bool = True) -> Dict[str, float]:
        """
        Calculate the total cost spent across all runs.

        Args:
            include_current: Whether to include current operation costs not yet in history
            current_cost: Current operation costs to include if include_current is True
            include_markup: Whether to include the standard markup in the returned costs

        Returns:
            Dictionary with total message cost and session cost
        """
        total_message_cost = 0.0
        total_session_cost = 0.0

        # Sum up costs from history
        for entry in self.cost_history:
            cost_info = entry.get('cost', {})
            if cost_info:
                total_message_cost += cost_info.get('message_cost', 0.0)
                total_session_cost += cost_info.get('session_cost', 0.0)

        # Add current operation costs if requested and not already in history
        if include_current and current_cost:
            total_message_cost += current_cost.get('message_cost', 0.0)
            total_session_cost += current_cost.get('session_cost', 0.0)

        # Calculate the combined total
        combined_total = total_message_cost + total_session_cost

        # Apply markup if requested
        if include_markup:
            markup_factor = 1.2  # 20% markup
            total_message_cost *= markup_factor
            total_session_cost *= markup_factor
            combined_total *= markup_factor

        return {
            'total_message_cost': total_message_cost,
            'total_session_cost': total_session_cost,
            'total_cost': combined_total
        }

    def _get_credit_info(self) -> None:
        """
        Get the user's credit information from the LMSYS API server.

        Raises:
            ValueError: If fetching credit info fails
        """
        if not self.session_token:
            return

        try:
            # Check if token needs refresh
            if self.token_expires_at and datetime.datetime.now() >= self.token_expires_at:
                self._refresh_token()

            # Fetch credit info
            response = requests.get(
                f"{self.LMSYS_API_URL}/stripe/getCredits",
                headers={"Authorization": f"Bearer {self.session_token}"}
            )

            if response.status_code != 200:
                raise ValueError(f"Failed to fetch credit information: {response.text}")

            credit_info = response.json()
            self.credits = credit_info.get("credits", 0.0)
            self.credit_limit = credit_info.get("credit_limit", 0.0)

        except Exception as e:
            raise ValueError(f"Failed to fetch credit information: {str(e)}")

    def get_credit_info(self) -> Dict[str, float]:
        """
        Get the user's current credit information.

        Returns:
            Dictionary with credit information including remaining credits and credit limit
        """
        # Refresh credit info from server if we have a session token
        if self.session_token:
            try:
                self._get_credit_info()
            except Exception as e:
                print(f"Warning: Failed to refresh credit information: {str(e)}")

        return {
            "credits": self.credits or 0.0,
            "credit_limit": self.credit_limit or 0.0,
            "credits_used": (self.credit_limit or 0.0) - (self.credits or 0.0)
        }

    def check_credits_sufficient(self, estimated_cost: float = 0.0) -> bool:
        """
        Check if the user has sufficient credits for an operation.

        Args:
            estimated_cost: Estimated cost of the operation

        Returns:
            True if user has sufficient credits, False otherwise
        """
        # Refresh credit info
        if self.session_token:
            try:
                self._get_credit_info()
            except:
                pass

        # If we don't have credit info or not using the LMSYS API, assume sufficient
        if self.credits is None:
            return True

        # Check if remaining credits are sufficient
        return self.credits >= estimated_cost

    def buy_credits(self, amount: float) -> Dict[str, Any]:
        """
        Get information needed to purchase credits (frontend should handle actual purchase).

        Args:
            amount: Dollar amount to add (minimum $5)

        Returns:
            Dictionary with payment information
        """
        if not self.session_token:
            raise ValueError("Authentication required to purchase credits")

        if amount < 5.0:
            raise ValueError("Minimum payment amount is $5.00")

        try:
            # Get Stripe configuration
            config_response = requests.get(
                f"{self.LMSYS_API_URL}/stripe/config",
                headers={"Authorization": f"Bearer {self.session_token}"}
            )

            if config_response.status_code != 200:
                raise ValueError(f"Failed to get payment configuration: {config_response.text}")

            config = config_response.json()

            return {
                "stripe_publishable_key": config.get("publishable_key"),
                "api_url": f"{self.LMSYS_API_URL}/stripe/createPaymentIntent",
                "amount": amount,
                "credits": amount,  # 1:1 ratio of dollars to credits
                "session_token": self.session_token
            }
        except Exception as e:
            raise ValueError(f"Failed to prepare credit purchase: {str(e)}")

    def get_payment_history(self) -> List[Dict[str, Any]]:
        """
        Get the user's payment history.

        Returns:
            List of payment records
        """
        if not self.session_token:
            raise ValueError("Authentication required to get payment history")

        try:
            response = requests.get(
                f"{self.LMSYS_API_URL}/stripe/paymentHistory",
                headers={"Authorization": f"Bearer {self.session_token}"}
            )

            if response.status_code != 200:
                raise ValueError(f"Failed to get payment history: {response.text}")

            return response.json().get("payments", [])
        except Exception as e:
            raise ValueError(f"Failed to get payment history: {str(e)}")

    def __del__(self):
        """Restore original environment variables and clean up when the object is deleted."""
        try:
            # Restore original environment variables
            if hasattr(self, 'key_manager'):
                self.key_manager.restore_environment()
        except:
            pass  # Ignore errors during cleanup


class SandboxSDK(Local):
    """
    Extension of the Local SDK that operates within an E2B sandbox environment.
    Allows running code, commands, and AI coding tasks in an isolated sandbox.
    """

    def __init__(
        self,
        model: str = "gpt-4.1-nano",
        editor_model: Optional[str] = None,
        api_key: Optional[str] = None,
        api_keys: Optional[Dict[str, str]] = None,  # For backward compatibility
        sandbox_timeout: int = 120,  # 2 minutes default
        sandbox_id: Optional[str] = None,  # Connect to existing sandbox if provided
        user_id: Optional[str] = None,  # For tracking and persistence
        architect_mode: bool = False,
        weak_model: Optional[str] = None
    ):
        """
        Initialize the Sandbox Aider SDK.

        Args:
            model: The AI model to use for coding tasks (default: gpt-4)
            editor_model: Optional separate model for editing operations
            api_key: LMSYS API key for authentication (preferred method)
            api_keys: Dictionary of API keys for various providers (legacy method)
            sandbox_timeout: Timeout in seconds for the sandbox (default: 300 seconds)
            sandbox_id: ID of existing sandbox to connect to (optional)
            user_id: User ID for tracking and persistence (optional)
            architect_mode: Whether to use architect mode (planner + editor workflow)
            weak_model: Optional planner model to use in architect mode (defaults to the main model if None)
        """
        # Initialize with a temporary working directory
        super().__init__(
            working_dir="/tmp",  # Temporary, will be overridden by sandbox workspace
            model=model,
            editor_model=editor_model,
            use_git=False,  # No git in sandbox by default
            api_key=api_key,
            api_keys=api_keys,
            architect_mode=architect_mode,
            weak_model=weak_model
        )

        # Import E2B SDK
        try:
            from e2b import Sandbox
            self.Sandbox = Sandbox
        except ImportError:
            raise ImportError("E2B SDK is required. Install it with 'pip install e2b'.")

        self.user_id = user_id or str(uuid.uuid4())
        self._initialize_sandbox(sandbox_id, sandbox_timeout)

    def _initialize_sandbox(self, sandbox_id=None, timeout=300):
        """
        Initialize the E2B sandbox or connect to an existing one.

        Args:
            sandbox_id: ID of existing sandbox to connect to (optional)
            timeout: Timeout in seconds for the sandbox

        Returns:
            The initialized sandbox instance
        """
        # Get E2B API key through LMSYS API if we have a session token
        if self.session_token:
            try:
                # Check if token needs refresh
                if self.token_expires_at and datetime.datetime.now() >= self.token_expires_at:
                    self._refresh_token()

                # Clear any existing E2B API key from environment
                if "E2B_API_KEY" in os.environ:
                    del os.environ["E2B_API_KEY"]

                response = requests.get(
                    f"{self.LMSYS_API_URL}/getKeys",
                    params={"providers": ["e2b"]},
                    headers={"Authorization": f"Bearer {self.session_token}"}
                )

                if response.status_code == 200:
                    e2b_key = response.json().get("e2b")
                    if e2b_key:
                        # Store the key in our secure key manager
                        self.key_manager.set_key("e2b", e2b_key)

                        # Temporarily set as environment variable for compatibility
                        os.environ["E2B_API_KEY"] = e2b_key
                    else:
                        raise ValueError("E2B API key not found in database. Please add an E2B API key through the admin interface.")
                else:
                    raise ValueError(f"Failed to get E2B API key from LMSYS API: {response.text}")
            except Exception as e:
                raise ValueError(f"Failed to get E2B API key from LMSYS API: {str(e)}")
        else:
            # Check if we have an E2B key in our secure key manager
            if not self.key_manager.has_key("e2b"):
                raise ValueError("Authentication required to use sandbox. Please provide api_key parameter.")

            # Temporarily set E2B key from our secure manager
            e2b_key = self.key_manager.get_key("e2b")
            if e2b_key:
                os.environ["E2B_API_KEY"] = e2b_key

        # Validate E2B API key is available
        if "E2B_API_KEY" not in os.environ:
            raise ValueError("E2B_API_KEY not set. Authentication with valid LMSYS API key is required.")

        # Connect to existing sandbox or create a new one
        if sandbox_id:
            self.sandbox = self.Sandbox.connect(sandbox_id)
        else:
            # Create a new sandbox with our template that has Aider pre-installed
            # Use metadata to track the user session
            self.sandbox = self.Sandbox(
                template="z7uk9vvklc16ttoijkdy",  # Template ID with Aider pre-installed
                timeout=timeout,
                metadata={
                    "user_id": self.user_id,
                    "session_start": datetime.datetime.now().isoformat()
                }
            )

        # Store sandbox info for persistence
        self.sandbox_id = self.sandbox.sandbox_id

        # Override working directory to point to sandbox workspace
        self.working_dir = "/home/user"  # Default workspace in E2B sandbox

        return self.sandbox

    def upload_file(self, local_path: str, sandbox_path: Optional[str] = None) -> str:
        """
        Upload a local file to the sandbox.

        Args:
            local_path: Path to local file
            sandbox_path: Path in sandbox (defaults to same filename in working_dir)

        Returns:
            Path to the file in the sandbox
        """
        if not sandbox_path:
            sandbox_path = os.path.join(self.working_dir, os.path.basename(local_path))

        with open(local_path, "rb") as f:
            content = f.read()

        self.sandbox.files.write(sandbox_path, content)
        return sandbox_path

    def write_to_sandbox(
        self,
        content: Union[str, bytes, List[Dict[str, Union[str, bytes]]], str],
        path: Optional[str] = None,
        local_directory: Optional[str] = None,
        sandbox_directory: Optional[str] = None
    ) -> List[str]:
        """
        Write file(s) to the sandbox filesystem.

        This method supports multiple ways of writing files:
        1. Single file: Provide content and path
        2. Multiple files: Provide a list of dictionaries with path and data
        3. Directory: Provide a local directory path to upload all files from that directory

        Args:
            content: File content or list of file objects with 'path' and 'data' keys,
                    or ignored if local_directory is provided
            path: Path in the sandbox for a single file upload (required if content is str/bytes)
            local_directory: Local directory path containing files to upload
            sandbox_directory: Target directory in sandbox for directory uploads (defaults to working_dir)

        Returns:
            List of paths written to the sandbox
        """
        written_paths = []

        # Create a function to ensure directory exists
        def ensure_directory_exists(dir_path):
            if dir_path:
                try:
                    self.sandbox.commands.run(f"mkdir -p {dir_path}")
                except Exception as e:
                    print(f"Warning: Could not create directory {dir_path}: {e}")

        # Case 1: Upload a directory
        if local_directory:
            if not os.path.isdir(local_directory):
                raise ValueError(f"Directory not found: {local_directory}")

            sandbox_dir = sandbox_directory or self.working_dir
            # Ensure the sandbox directory exists
            ensure_directory_exists(sandbox_dir)

            files_to_write = []

            # Iterate through all files in the directory
            for root, _, filenames in os.walk(local_directory):
                for filename in filenames:
                    local_file_path = os.path.join(root, filename)

                    # Calculate relative path from local_directory
                    rel_path = os.path.relpath(local_file_path, local_directory)
                    sandbox_file_path = os.path.join(sandbox_dir, rel_path)

                    # Ensure the directory for this file exists
                    ensure_directory_exists(os.path.dirname(sandbox_file_path))

                    # Read file contents in binary mode
                    with open(local_file_path, "rb") as file:
                        file_data = file.read()
                        files_to_write.append({
                            'path': sandbox_file_path,
                            'data': file_data
                        })
                        written_paths.append(sandbox_file_path)

            # Write all files to sandbox
            if files_to_write:
                # Try to write files individually for better reliability
                for file_obj in files_to_write:
                    try:
                        self.sandbox.files.write(file_obj['path'], file_obj['data'])

                        # Verify the file exists
                        if not self._file_exists_in_sandbox(file_obj['path']):
                            print(f"Warning: File {file_obj['path']} doesn't appear to exist after creation.")
                    except Exception as e:
                        print(f"Error writing file {file_obj['path']}: {e}")

        # Case 2: Multiple files as list of objects
        elif isinstance(content, list):
            for file_obj in content:
                if 'path' not in file_obj or 'data' not in file_obj:
                    raise ValueError("Each file object must contain 'path' and 'data' keys")

                # Ensure the directory for this file exists
                ensure_directory_exists(os.path.dirname(file_obj['path']))

                try:
                    self.sandbox.files.write(file_obj['path'], file_obj['data'])
                    written_paths.append(file_obj['path'])

                    # Verify the file exists
                    if not self._file_exists_in_sandbox(file_obj['path']):
                        print(f"Warning: File {file_obj['path']} doesn't appear to exist after creation.")
                except Exception as e:
                    print(f"Error writing file {file_obj['path']}: {e}")

        # Case 3: Single file
        elif path:
            # Ensure the directory for this file exists
            ensure_directory_exists(os.path.dirname(path))

            try:
                self.sandbox.files.write(path, content)
                written_paths.append(path)

                # Verify the file exists
                if not self._file_exists_in_sandbox(path):
                    print(f"Warning: File {path} doesn't appear to exist after creation.")
            except Exception as e:
                print(f"Error writing file {path}: {e}")

        else:
            raise ValueError("Either path (for single file) or a list of file objects or local_directory must be provided")

        return written_paths

    def download_file(self, sandbox_path: str, local_path: Optional[str] = None) -> str:
        """
        Download a file from the sandbox to local filesystem.

        Args:
            sandbox_path: Path to file in sandbox
            local_path: Path to download to (defaults to same filename)

        Returns:
            Path to the downloaded file
        """
        if not local_path:
            local_path = os.path.basename(sandbox_path)

        content = self.sandbox.files.read(sandbox_path)

        # Handle both string and bytes content types
        if isinstance(content, str):
            with open(local_path, "w", encoding="utf-8") as f:
                f.write(content)
        else:
            with open(local_path, "wb") as f:
                f.write(content)

        return local_path

    def read_sandbox_file(self, sandbox_path: str, as_string: bool = True, encoding: str = "utf-8") -> Union[str, bytes]:
        """
        Read a file from the sandbox.

        Args:
            sandbox_path: Path to the file in the sandbox
            as_string: Whether to return the content as a string (True) or bytes (False)
            encoding: Encoding to use when converting bytes to string (default: utf-8)

        Returns:
            File content as string or bytes depending on as_string parameter
        """
        try:
            content = self.sandbox.files.read(sandbox_path)

            # If content is bytes and as_string is True, decode to string
            if isinstance(content, bytes) and as_string:
                return content.decode(encoding)
            # If content is string and as_string is False, encode to bytes
            elif isinstance(content, str) and not as_string:
                return content.encode(encoding)
            # Otherwise return as is
            else:
                return content
        except Exception as e:
            raise ValueError(f"Error reading file '{sandbox_path}': {str(e)}")

    def run_command(self, command: str) -> Dict[str, Any]:
        """
        Run a command in the sandbox.

        Args:
            command: Command to run

        Returns:
            Dictionary with command result info
        """
        result = self.sandbox.commands.run(command)

        return {
            "exit_code": result.exit_code,
            "stdout": result.stdout,
            "stderr": result.stderr,
        }

    def _file_exists_in_sandbox(self, file_path: str) -> bool:
        """
        Check if a file exists in the sandbox.

        Args:
            file_path: Path to file in sandbox

        Returns:
            True if file exists, False otherwise
        """
        try:
            # More reliable approach: try to list the directory and check if the file exists
            # Extract the directory and filename
            import os
            directory = os.path.dirname(file_path) or "/"
            filename = os.path.basename(file_path)

            # Run a command to check if the file exists (more reliable than stat)
            result = self.sandbox.commands.run(f"ls -la {directory} | grep {filename}")
            return result.exit_code == 0 and filename in result.stdout
        except Exception as e:
            print(f"Error checking if file exists: {str(e)}")
            # Fallback to the original approach
            try:
                self.sandbox.files.stat(file_path)
                return True
            except Exception:
                return False

    def sandbox_code(
        self,
        prompt: str,
        editable_files: List[str],
        readonly_files: List[str] = None,
    ) -> Dict[str, Any]:
        """
        Run an AI coding task in the sandbox with the specified prompt and files.

        Args:
            prompt: Natural language instruction for the AI coding task
            editable_files: List of files in the sandbox that can be modified by the AI
            readonly_files: List of files in the sandbox that can be read but not modified

        Returns:
            Dictionary with 'success' boolean, 'diff' string showing changes, and cost information
        """
        if readonly_files is None:
            readonly_files = []

        # First verify all files exist in the sandbox using commands
        missing_files = []
        all_files = editable_files + readonly_files

        # Use a more direct command to check all files at once
        if all_files:
            file_list_str = " ".join(all_files)
            result = self.sandbox.commands.run(f"ls -la {file_list_str} 2>&1 || echo 'FILES_MISSING'")

            if "FILES_MISSING" in result.stdout or "No such file or directory" in result.stdout:
                # Some files might be missing, check each one individually
                for path in all_files:
                    # Get absolute path if not already
                    abs_path = path if os.path.isabs(path) else os.path.join(self.working_dir, path)
                    # Check file existence with a direct command
                    check_result = self.sandbox.commands.run(f"[ -f '{abs_path}' ] && echo 'EXISTS' || echo 'MISSING'")

                    if "MISSING" in check_result.stdout:
                        missing_files.append(path)
                        print(f"Warning: File '{path}' does not appear to exist in the sandbox")

        # If files are missing, try to create them with empty content as a fallback
        if missing_files:
            print(f"Attempting to create missing files: {missing_files}")
            for path in missing_files:
                try:
                    # Create empty file
                    abs_path = path if os.path.isabs(path) else os.path.join(self.working_dir, path)
                    dir_path = os.path.dirname(abs_path)
                    if dir_path:
                        self.sandbox.commands.run(f"mkdir -p '{dir_path}'")
                    self.sandbox.commands.run(f"touch '{abs_path}'")

                    # Verify it was created
                    check_result = self.sandbox.commands.run(f"[ -f '{abs_path}' ] && echo 'EXISTS' || echo 'MISSING'")
                    if "MISSING" in check_result.stdout:
                        raise ValueError(f"Failed to create missing file: {path}")
                except Exception as e:
                    raise ValueError(f"Error creating missing file '{path}': {str(e)}")

        # Run the coding task with sandbox paths
        result = self._run_sandbox_coding_task(prompt, editable_files, readonly_files)

        return result

    def _run_sandbox_coding_task(self, prompt, editable_files, readonly_files):
        """
        Helper to run coding tasks in sandbox context.

        Args:
            prompt: Natural language instruction for the AI coding task
            editable_files: List of files in the sandbox that can be modified by the AI
            readonly_files: List of files in the sandbox that can be read but not modified

        Returns:
            Dictionary with task result information
        """
        # Download files from sandbox to temporary local directory
        temp_dir = tempfile.mkdtemp()
        local_editable_files = []
        local_readonly_files = []

        try:
            # Download editable files
            for file in editable_files:
                local_path = os.path.join(temp_dir, os.path.basename(file))
                content = self.sandbox.files.read(file)
                if isinstance(content, str):
                    content = content.encode()
                with open(local_path, "wb") as f:
                    f.write(content)
                local_editable_files.append(local_path)

            # Download readonly files
            for file in readonly_files:
                local_path = os.path.join(temp_dir, os.path.basename(file))
                content = self.sandbox.files.read(file)
                if isinstance(content, str):
                    content = content.encode()
                with open(local_path, "wb") as f:
                    f.write(content)
                local_readonly_files.append(local_path)

            # Temporarily override working directory for local operation
            original_working_dir = self.working_dir
            self.working_dir = temp_dir

            # Preserve architect mode settings
            original_architect_mode = self.architect_mode
            original_model = self.model

            # Ensure we have provider keys available through the secure key manager
            # This is essential for sandbox operations to work with proper security
            from aider.llm import litellm
            if hasattr(litellm, "_construct_completion_url"):
                original_construct_fn = litellm._construct_completion_url

                def secure_construct_completion_url(*args, **kwargs):
                    provider = kwargs.get("provider") or (args[0] if len(args) > 0 else None)
                    # Check if we have a secure key for this provider
                    if provider and self.key_manager.has_key(provider):
                        # Temporarily set the environment variable
                        key = self.key_manager.get_key(provider)
                        env_var = f"{provider.upper()}_API_KEY"
                        if env_var not in os.environ:
                            os.environ[env_var] = key
                    return original_construct_fn(*args, **kwargs)

                # Apply our patch
                litellm._construct_completion_url = secure_construct_completion_url

            # Perform coding task locally
            try:
                result = self.code(prompt, [os.path.basename(f) for f in local_editable_files],
                                 [os.path.basename(f) for f in local_readonly_files])
            finally:
                # Restore working directory and architect mode settings
                self.working_dir = original_working_dir
                self.architect_mode = original_architect_mode
                self.model = original_model

                # Clean up by restoring litellm's original function if we modified it
                if 'original_construct_fn' in locals() and hasattr(litellm, "_construct_completion_url"):
                    litellm._construct_completion_url = original_construct_fn

            # Upload modified files back to sandbox
            for local_file, sandbox_file in zip([os.path.join(temp_dir, os.path.basename(f)) for f in editable_files],
                                              editable_files):
                if os.path.exists(local_file):
                    with open(local_file, "rb") as f:
                        content = f.read()
                    self.sandbox.files.write(sandbox_file, content)

            return result

        finally:
            # Clean up temp directory
            shutil.rmtree(temp_dir)

    def extend_sandbox_timeout(self, seconds: int = 300) -> None:
        """
        Extend the sandbox timeout.

        Args:
            seconds: Number of seconds to extend the timeout by
        """
        # Ensure E2B API key is available for this operation
        if not "E2B_API_KEY" in os.environ and self.key_manager.has_key("e2b"):
            os.environ["E2B_API_KEY"] = self.key_manager.get_key("e2b")

        self.sandbox.set_timeout(seconds)

    def get_sandbox_info(self) -> Dict[str, Any]:
        """
        Get information about the current sandbox.

        Returns:
            Dictionary with sandbox information
        """
        # Ensure E2B API key is available
        if not "E2B_API_KEY" in os.environ and self.key_manager.has_key("e2b"):
            os.environ["E2B_API_KEY"] = self.key_manager.get_key("e2b")

        # Access sandbox properties directly instead of using get_info()
        return {
            "sandbox_id": self.sandbox.sandbox_id,
            "template_id": getattr(self.sandbox, "template_id", None),
            "started_at": getattr(self.sandbox, "started_at", None),
            "end_at": getattr(self.sandbox, "end_at", None),
            "metadata": getattr(self.sandbox, "metadata", {})
        }

    def kill_sandbox(self) -> Dict[str, Any]:
        """
        Shutdown the sandbox immediately.

        This will terminate the sandbox regardless of its remaining timeout.
        Once killed, the sandbox cannot be restarted.

        Returns:
            Dictionary with kill status information
        """
        try:
            # Ensure E2B API key is available for this operation
            if not "E2B_API_KEY" in os.environ and self.key_manager.has_key("e2b"):
                os.environ["E2B_API_KEY"] = self.key_manager.get_key("e2b")

            self.sandbox.kill()
            return {
                "success": True,
                "sandbox_id": self.sandbox_id,
                "message": f"Sandbox {self.sandbox_id} has been successfully terminated."
            }
        except Exception as e:
            return {
                "success": False,
                "sandbox_id": self.sandbox_id,
                "error": str(e),
                "message": f"Failed to terminate sandbox {self.sandbox_id}."
            }