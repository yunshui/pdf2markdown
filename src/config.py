"""Configuration management for PDF to Markdown converter."""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """Configuration manager for the PDF to Markdown converter."""

    DEFAULT_CONFIG: Dict[str, Any] = {
        "model": {
            "name": "qwen3.5-27b",
            "api_url": "",
            "api_key": "",
            "timeout": 200
        },
        "conversion": {
            "max_retries": 3,
            "single_page_prompt": "请将这张图片中的内容转换为Markdown格式，保持原有的格式和结构。",
            "multi_page_summary_prompt": "请总结这张图片中的关键信息，用简短的中文描述。"
        },
        "paths": {
            "output_dir": "output",
            "logs_dir": "logs"
        }
    }

    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration.

        Args:
            config_path: Optional path to config file. If not provided, uses default.
        """
        self.config_path = config_path or self._get_default_config_path()
        self.config = self._load_config()

    def _get_default_config_path(self) -> str:
        """Get default config file path."""
        # Check if running from script directory
        script_dir = Path(__file__).parent.parent
        config_file = script_dir / "conf" / "setting.json"
        return str(config_file)

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file or create default."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                # Merge with default config to ensure all keys exist
                config = self._deep_merge(self.DEFAULT_CONFIG.copy(), loaded_config)
                return config
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Failed to load config from {self.config_path}: {e}")
                print("Using default configuration.")
                return self.DEFAULT_CONFIG.copy()
        else:
            # Create default config file
            self._save_config(self.DEFAULT_CONFIG.copy())
            return self.DEFAULT_CONFIG.copy()

    def _save_config(self, config: Dict[str, Any]) -> None:
        """Save configuration to file."""
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    @staticmethod
    def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
        """Deep merge two dictionaries.

        Args:
            base: Base dictionary to merge into
            override: Dictionary with override values

        Returns:
            Merged dictionary
        """
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = Config._deep_merge(result[key], value)
            else:
                result[key] = value
        return result

    def update(self, **kwargs) -> None:
        """Update configuration with keyword arguments.

        Args:
            **kwargs: Configuration key-value pairs to update
        """
        for key, value in kwargs.items():
            if '.' in key:
                # Handle nested keys like 'model.name'
                parts = key.split('.')
                current = self.config
                for part in parts[:-1]:
                    if part not in current:
                        current[part] = {}
                    current = current[part]
                current[parts[-1]] = value
            else:
                self.config[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by key.

        Args:
            key: Configuration key (supports dot notation like 'model.name')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        parts = key.split('.')
        current = self.config
        try:
            for part in parts:
                current = current[part]
            return current
        except (KeyError, TypeError):
            return default

    def save(self) -> None:
        """Save current configuration to file."""
        self._save_config(self.config)

    @property
    def model_name(self) -> str:
        """Get model name."""
        return self.get('model.name', 'qwen3.5-27b')

    @property
    def api_url(self) -> str:
        """Get API URL."""
        return self.get('model.api_url', '')

    @property
    def api_key(self) -> str:
        """Get API key."""
        return self.get('model.api_key', '')

    @property
    def timeout(self) -> int:
        """Get timeout in seconds."""
        return self.get('model.timeout', 200)

    @property
    def max_retries(self) -> int:
        """Get max retries."""
        return self.get('conversion.max_retries', 3)

    @property
    def single_page_prompt(self) -> str:
        """Get single page prompt."""
        return self.get('conversion.single_page_prompt', '请将这张图片中的内容转换为Markdown格式，保持原有的格式和结构。')

    @property
    def multi_page_summary_prompt(self) -> str:
        """Get multi page summary prompt."""
        return self.get('conversion.multi_page_summary_prompt', '请总结这张图片中的关键信息，用简短的中文描述。')

    @property
    def output_dir(self) -> str:
        """Get output directory."""
        return self.get('paths.output_dir', 'output')

    @property
    def logs_dir(self) -> str:
        """Get logs directory."""
        return self.get('paths.logs_dir', 'logs')