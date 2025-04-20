"""
Deleashes SDK client module.
"""

import requests
from enum import Enum
from typing import Any, Dict, Optional, Union

from .logging import get_logger

logger = get_logger()


class Environment(str, Enum):
    """Valid environments for feature flags."""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"


class Deleashes:
    """
    Deleashes SDK client for feature flag management.
    
    Examples:
        >>> from deleashes import Deleashes
        >>> 
        >>> # Initialize the client
        >>> client = Deleashes(
        ...     base_url="https://your-deleashes-url.com",
        ...     api_key="YOUR_PROJECT_API_KEY",
        ...     environment=Environment.DEVELOPMENT
        ... )
        >>> 
        >>> # Check if feature flag is enabled
        >>> if client.is_enabled("new-feature"):
        ...     # Your feature code here
        ...     print("Feature is enabled!")
        >>> 
        >>> # Get the value of a feature flag
        >>> feature_value = client.get_value("feature-with-value")
        >>> print(f"Feature value: {feature_value}")
    """

    def __init__(
        self,
        api_key: str,
        base_url: str,
        environment: Union[Environment, str] = Environment.DEVELOPMENT,
        timeout: int = 2,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize the Deleashes client.

        Args:
            api_key: The project API key from Deleashes.
            base_url: The base URL of the Deleashes API (e.g., "https://your-deleashes-url.com").
            environment: The environment to check flags in (development, staging, production).
            timeout: Request timeout in seconds.
            context: Default context for flag evaluations (user_id and additional data).
        """
        self.api_key = api_key
        
        # Validate and set environment
        if isinstance(environment, str):
            try:
                environment = Environment(environment)
            except ValueError:
                valid_envs = [e.value for e in Environment]
                logger.warning(
                    f"Invalid environment '{environment}'. Must be one of: {', '.join(valid_envs)}. "
                    f"Using default: {Environment.DEVELOPMENT.value}"
                )
                environment = Environment.DEVELOPMENT
        
        self.environment = environment
        
        # Validate base URL
        if not base_url:
            logger.warning("No base_url provided. You must specify the URL of your Deleashes instance.")
            base_url = ""
        
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.context = context or {}
        
        logger.debug(f"Deleashes client initialized for environment: {self.environment}")

    def is_enabled(self, flag_key: str, context: Optional[Dict[str, Any]] = None) -> bool:
        """
        Check if a feature flag is enabled.

        Args:
            flag_key: The key of the feature flag to check.
            context: Optional context for flag evaluation (overrides default context).

        Returns:
            True if the flag is enabled, False otherwise.
        """
        result = self._evaluate_flag(flag_key, context)
        return result.get('enabled', False) if result else False

    def get_value(self, flag_key: str, default_value: Any = None, context: Optional[Dict[str, Any]] = None) -> Any:
        """
        Get the value of a feature flag.

        Args:
            flag_key: The key of the feature flag to check.
            default_value: The default value to return if the flag is disabled or not found.
            context: Optional context for flag evaluation (overrides default context).

        Returns:
            The value of the feature flag if enabled, otherwise the default_value.
        """
        result = self._evaluate_flag(flag_key, context)
        
        if not result or not result.get('enabled', False):
            return default_value
            
        # Return the flag value or default if the value is None
        return result.get('value', default_value)

    def _evaluate_flag(self, flag_key: str, context: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Evaluate a feature flag.

        Args:
            flag_key: The key of the feature flag to evaluate.
            context: Optional context for flag evaluation.

        Returns:
            The evaluation result dict or None if evaluation failed.
        """
        merged_context = {**self.context, **(context or {})}
        url = f"{self.base_url}/api/v1/flags/client/evaluate/{self.api_key}/{flag_key}"
        
        params = {'environment': self.environment.value}
        data = {'context': merged_context}
        
        if 'user_id' in merged_context:
            data['user_id'] = merged_context['user_id']
            
        try:
            logger.debug(f"Evaluating flag '{flag_key}' in environment '{self.environment.value}'")
            response = requests.post(
                url, 
                params=params, 
                json=data, 
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return response.json()
                
            logger.warning(
                f"Failed to evaluate flag '{flag_key}'. "
                f"Status code: {response.status_code}, Response: {response.text}"
            )
            return None
            
        except requests.RequestException as e:
            logger.error(f"Error evaluating flag '{flag_key}': {str(e)}")
            return None
