"""AI service for generating social media posts across supported LLM providers."""

import os
from typing import Dict, List, Optional


class AIService:
    """Handle AI generation using configurable LLM providers."""

    PROVIDER_INFO: Dict[str, Dict[str, str]] = {
        "openai": {
            "display_name": "OpenAI",
            "env_var": "OPENAI_API_KEY",
            "signup_url": "https://platform.openai.com/api-keys",
        },
        "groq": {
            "display_name": "Groq",
            "env_var": "GROQ_API_KEY",
            "signup_url": "https://console.groq.com/keys",
        },
        "openrouter": {
            "display_name": "OpenRouter",
            "env_var": "OPENROUTER_API_KEY",
            "signup_url": "https://openrouter.ai/settings/keys",
        }
    }

    DEFAULT_MODELS: Dict[str, str] = {
        "openai": "gpt-4o-mini",
        "groq": "qwen/qwen3-32b",
<<<<<<< HEAD
=======
        "openrouter": "openai/gpt-4o-mini"
>>>>>>> 66d8d3bb903ce35015a5b91a7bd39ebb8407fcce
    }

    def __init__(
        self,
        provider: str = "openai",
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ):
        """
        Initialize AI service for the selected provider.

        Args:
            provider: LLM provider identifier ('openai', 'groq')
            api_key: API key for the provider. Falls back to provider env var.
            model: Model name to use. Falls back to provider defaults.

        Raises:
            ValueError: If provider is not supported or no API key is found.
        """
        provider = provider or "openai"
        if provider not in self.PROVIDER_INFO:
            raise ValueError(
                f"Unsupported provider '{provider}'. "
                f"Supported providers: {', '.join(self.supported_providers())}"
            )

        self.provider = provider
        info = self.get_provider_info(provider)
        env_value = os.getenv(info["env_var"])
        self.api_key = api_key or env_value

        if not self.api_key:
            raise ValueError(
                f"No API key found for {info['display_name']}.\n\n"
                f"Get your API key at: {info['signup_url']}\n\n"
                "Then set it using one of these methods:\n"
                f"  1. buildpost config set-key --provider {provider} YOUR_API_KEY\n"
                f"  2. export {info['env_var']}=YOUR_API_KEY\n"
                "  3. buildpost --api-key YOUR_API_KEY"
            )

        self.model_name = model or self.DEFAULT_MODELS.get(provider)
        if not self.model_name:
            raise ValueError(
                f"No default model configured for provider '{provider}'. "
                "Set one via configuration."
            )

        if provider == "openai":
            from openai import OpenAI

            self.client = OpenAI(api_key=self.api_key)
        elif provider == "groq":
            from groq import Groq

            self.client = Groq(api_key=self.api_key)
<<<<<<< HEAD
=======
        elif provider == "openrouter":
            from openai import OpenAI

            self.client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=self.api_key
            )
>>>>>>> 66d8d3bb903ce35015a5b91a7bd39ebb8407fcce

    def generate_post(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int = 500,
        temperature: float = 0.7,
    ) -> str:
        """
        Generate a social media post using AI.

        Args:
            system_prompt: System instructions for the AI
            user_prompt: User prompt with commit information
            max_tokens: Maximum tokens in response
            temperature: Creativity level (0.0 to 1.0)

        Returns:
            Generated post text

        Raises:
            Exception: If generation fails
        """
        if self.provider == "openai":
            return self._generate_with_openai(
                system_prompt, user_prompt, max_tokens, temperature
            )
<<<<<<< HEAD
        if self.provider == "groq":
            return self._generate_with_groq(
                system_prompt, user_prompt, max_tokens, temperature
            )
=======
        elif self.provider == "groq":
            return self._generate_with_groq(
                system_prompt, user_prompt, max_tokens, temperature
            )
        elif self.provider == "openrouter":
            return self._generate_with_openrouter(
                system_prompt, user_prompt, max_tokens, temperature
            )
>>>>>>> 66d8d3bb903ce35015a5b91a7bd39ebb8407fcce

        raise Exception(f"Unsupported provider '{self.provider}'.")

    def _generate_with_openai(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
        temperature: float,
    ) -> str:
        """Generate content using OpenAI chat completions."""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            choices = getattr(response, "choices", [])
            if not choices:
                raise Exception("No text generated.")

            message = choices[0].message
            content = getattr(message, "content", None)
            if isinstance(content, str):
                return content.strip()
            if isinstance(content, list):
                parts = [
                    part.get("text", "") for part in content if isinstance(part, dict)
                ]
                return " ".join(parts).strip()

            raise Exception("No text generated.")
        except Exception as exc:
            raise Exception(f"Failed to generate post: {str(exc)}")

    def _generate_with_groq(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
        temperature: float,
    ) -> str:
        """Generate content using Groq chat completions."""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            choices = getattr(response, "choices", [])
            if not choices:
                raise Exception("No text generated.")

            message = choices[0].message
            content = getattr(message, "content", None)
            if isinstance(content, str):
                return content.strip()

            raise Exception("No text generated.")
        except Exception as exc:
            raise Exception(f"Failed to generate post: {str(exc)}")
<<<<<<< HEAD
=======
        
    def _generate_with_openrouter(
        self,
        system_prompt: str,
        user_prompt: str,
        max_tokens: int,
        temperature: float,
    ) -> str:
        """Generate content using OpenRouter chat completions."""
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                max_tokens=max_tokens,
                temperature=temperature,
            )
            choices = getattr(response, "choices", [])
            if not choices:
                raise Exception("No text generated.")

            message = choices[0].message
            content = getattr(message, "content", None)
            if isinstance(content, str):
                return content.strip()
            if isinstance(content, list):
                parts = [
                    part.get("text", "") for part in content if isinstance(part, dict)
                ]
                return " ".join(parts).strip()

            raise Exception("No text generated.")
        except Exception as exc:
            raise Exception(f"Failed to generate post: {str(exc)}")
>>>>>>> 66d8d3bb903ce35015a5b91a7bd39ebb8407fcce

    def test_connection(self) -> bool:
        """
        Test if API key is valid and service is accessible.

        Returns:
            True if connection successful, False otherwise
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a concise assistant."},
                    {"role": "user", "content": "Say 'hello' in one word."},
                ],
                max_tokens=5,
                temperature=0,
            )
            choices = getattr(response, "choices", [])
            return bool(choices and choices[0].message.content)
        except Exception:
            return False

    @staticmethod
    def validate_api_key(api_key: str, provider: str = "openai") -> bool:
        """
        Validate if an API key format is correct.

        Args:
            api_key: API key to validate
            provider: Provider identifier

        Returns:
            True if key format appears valid
        """
        if not api_key:
            return False

        provider = provider or "openai"
        if provider == "openai":
            return api_key.startswith("sk-")
<<<<<<< HEAD
        if provider == "groq":
            return api_key.startswith("gsk_") or api_key.startswith("sk-")
=======
        elif provider == "groq":
            return api_key.startswith("gsk_") or api_key.startswith("sk-")
        elif provider == "openrouter":
            return api_key.startswith("sk-or-v1-")
>>>>>>> 66d8d3bb903ce35015a5b91a7bd39ebb8407fcce
        return True

    @classmethod
    def supported_providers(cls) -> List[str]:
        """Return supported provider identifiers."""
        return list(cls.PROVIDER_INFO.keys())

    @classmethod
    def get_provider_info(cls, provider: str) -> Dict[str, str]:
        """Get metadata for a provider."""
        return cls.PROVIDER_INFO.get(
            provider, {"display_name": provider, "env_var": "", "signup_url": ""}
        )
