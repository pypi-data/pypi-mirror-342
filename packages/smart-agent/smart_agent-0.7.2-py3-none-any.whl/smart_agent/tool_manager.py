"""
Configuration management for Smart Agent.
Handles loading, configuration, and initialization of tools from YAML configuration.
"""

import os
import yaml
import logging
from typing import Dict, List, Optional, Any
from pathlib import Path

# Set up logging
logger = logging.getLogger(__name__)

# Use direct print statements during initialization, then switch to logger
# This avoids the chicken-and-egg problem of needing to log before we know the log level
USE_PRINT_DURING_INIT = True

def update_logger_level(level_str: str):
    """Update the logger level based on the config."""
    log_level = getattr(logging, level_str.upper(), logging.INFO)
    
    # Update the root logger level
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Update this module's logger level
    logger.setLevel(log_level)
    
    # Update handlers format to ensure consistent logging
    for handler in root_logger.handlers:
        handler.setLevel(log_level)

def log_message(message: str, level: str = "INFO"):
    """
    Log a message at the specified level, respecting the configured log level.
    
    Args:
        message: The message to log
        level: The level to log at (INFO, WARNING, ERROR, DEBUG)
    """
    # During initialization, use print for WARNING and above
    if USE_PRINT_DURING_INIT:
        if level.upper() in ["WARNING", "ERROR", "CRITICAL"]:
            print(message)
        return
        
    # After initialization, use the logger
    log_method = getattr(logger, level.lower(), logger.info)
    log_method(message)


class ConfigManager:
    """
    Manages configuration for Smart Agent based on YAML configuration.
    """

    def __init__(self, config_path: Optional[str] = None, tools_path: Optional[str] = None):
        """
        Initialize the ConfigManager.

        Args:
            config_path: Path to the YAML configuration file. If None, will look in default locations.
            tools_path: Path to the tools configuration file. If None, will use the path specified in the config file.
        """
        self.config = {}
        self.config_path = config_path
        self.tools_path = tools_path
        self.tools_config = {}
        self.litellm_config = {}
        self._load_config()

    def _load_config(self):
        """
        Load configuration from YAML file.
        """
        # Default config paths to check
        default_paths = [
            self.config_path,
            os.path.join(os.getcwd(), "config", "config.yaml"),
            os.path.join(os.getcwd(), "config.yaml"),
            os.path.expanduser("~/.config/smart-agent/config.yaml"),
        ]

        # Filter out None values
        default_paths = [p for p in default_paths if p is not None]

        # Try to load from each path
        for path in default_paths:
            if os.path.exists(path):
                try:
                    with open(path, "r") as f:
                        self.config = yaml.safe_load(f) or {}
                    log_message(f"Loaded configuration from {path}", "INFO")

                    # Load tools configuration
                    tools_config_path = self.tools_path or self.config.get("tools_config")
                    if tools_config_path:
                        if not os.path.isabs(tools_config_path):
                            # Make path relative to the config file
                            config_dir = os.path.dirname(path)

                            # Fix for config/tools.yaml style paths when config file is already in the config directory
                            if tools_config_path.startswith("config/") and os.path.basename(config_dir) == "config":
                                # Remove the "config/" prefix to avoid duplication
                                tools_config_path = tools_config_path[7:]  # length of "config/"

                            tools_config_path = os.path.join(
                                config_dir, tools_config_path
                            )

                        if os.path.exists(tools_config_path):
                            with open(tools_config_path, "r") as f:
                                self.tools_config = yaml.safe_load(f).get("tools", {})
                            log_message(
                                f"Loaded tools configuration from {tools_config_path}", "INFO"
                            )
                        else:
                            log_message(
                                f"Tools configuration file not found: {tools_config_path}", "WARNING"
                            )
                            # Try an alternative path construction as fallback
                            alternate_path = os.path.join(os.path.dirname(config_dir), tools_config_path)
                            if os.path.exists(alternate_path):
                                with open(alternate_path, "r") as f:
                                    self.tools_config = yaml.safe_load(f).get("tools", {})
                                log_message(
                                    f"Loaded tools configuration from alternate path: {alternate_path}", "INFO"
                                )

                    # Load LiteLLM configuration if available
                    self.litellm_config = self._load_litellm_config()
                    
                    # Now that we've loaded the config, we can switch to using the logger
                    global USE_PRINT_DURING_INIT
                    USE_PRINT_DURING_INIT = False
                    
                    # Update logger level based on config - do this before any logging
                    log_level = self.get_log_level()
                    update_logger_level(log_level)
                    
                    # Force reconfiguration of logging
                    handlers = [logging.StreamHandler()]
                    log_file = self.get_log_file()
                    if log_file:
                        handlers.append(logging.FileHandler(log_file))
                    
                    # Reset root logger handlers
                    for handler in logging.root.handlers[:]:
                        logging.root.removeHandler(handler)
                    
                    # Set up basic config with the correct level
                    numeric_level = getattr(logging, log_level.upper(), logging.INFO)
                    logging.basicConfig(
                        level=numeric_level,
                        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                        handlers=handlers,
                    )

                    return
                except Exception as e:
                    log_message(f"Error loading configuration from {path}: {e}", "ERROR")

        log_message("No configuration file found. Using default settings.", "WARNING")
        self.config = {}

    def _load_litellm_config(self):
        """
        Load LiteLLM configuration from the path specified in the config.

        Returns:
            Dictionary containing LiteLLM configuration
        """
        litellm_config_path = self.config.get("llm", {}).get("config_file")
        if not litellm_config_path:
            return {}

        # Handle relative paths
        if not os.path.isabs(litellm_config_path):
            if self.config_path:
                litellm_config_path = os.path.join(os.path.dirname(self.config_path), litellm_config_path)
            else:
                litellm_config_path = os.path.join(os.getcwd(), litellm_config_path)

        if not os.path.exists(litellm_config_path):
            log_message(f"LiteLLM config file not found at {litellm_config_path}", "WARNING")
            return {}

        try:
            with open(litellm_config_path, "r") as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            log_message(f"Error loading LiteLLM config: {e}", "ERROR")
            return {}

    def get_config(
        self,
        section: Optional[str] = None,
        key: Optional[str] = None,
        default: Any = None,
    ) -> Any:
        """
        Get configuration value.

        Args:
            section: Configuration section (e.g., 'api', 'model')
            key: Configuration key within section
            default: Default value if not found

        Returns:
            Configuration value or default
        """
        if section is None:
            return self.config

        section_data = self.config.get(section, {})

        if key is None:
            return section_data

        return section_data.get(key, default)

    def get_tool_config(self, tool_id: str) -> Dict:
        """
        Get configuration for a specific tool.

        Args:
            tool_id: The ID of the tool to get configuration for

        Returns:
            Tool configuration dictionary
        """
        # First check if the tool is directly in the tools_config (new format)
        if tool_id in self.tools_config:
            return self.tools_config.get(tool_id, {})

        # Then check if it's under the 'tools' key (old format)
        tools = self.tools_config.get("tools", {})
        return tools.get(tool_id, {})

    def get_all_tools(self) -> Dict:
        """
        Get configuration for all tools.

        Returns:
            Dictionary of all tool configurations
        """
        # Check if tools are under a 'tools' key (old format) or directly at the root (new format)
        tools = self.tools_config.get("tools", None)
        if tools is not None:
            return tools

        # If no 'tools' key, assume the entire config is the tools dictionary
        return self.tools_config

    def get_tools_config(self) -> Dict:
        """
        Get configuration for all tools.
        Alias for get_all_tools() for backward compatibility.

        Returns:
            Dictionary of all tool configurations
        """
        return self.get_all_tools()

    def is_tool_enabled(self, tool_id: str) -> bool:
        """
        Check if a tool is enabled.

        Args:
            tool_id: The ID of the tool to check

        Returns:
            True if the tool is enabled, False otherwise
        """
        tool_config = self.get_tool_config(tool_id)

        # Check environment variable override
        env_enabled = os.getenv(f"ENABLE_{tool_id.upper()}")
        if env_enabled is not None:
            return env_enabled.lower() == "true"

        # Fall back to configuration
        return tool_config.get("enabled", False)

    def get_env_prefix(self, tool_id: str) -> str:
        """
        Get the environment variable prefix for a tool.

        Args:
            tool_id: The ID of the tool

        Returns:
            Environment variable prefix
        """
        tool_config = self.get_tool_config(tool_id)
        # Use env_prefix if provided, otherwise generate from tool_id
        return tool_config.get("env_prefix", f"SMART_AGENT_TOOL_{tool_id.upper()}")

    def get_tool_url(self, tool_id: str) -> str:
        """
        Get the URL for a tool.

        Args:
            tool_id: The ID of the tool to get the URL for

        Returns:
            Tool URL
        """
        tool_config = self.get_tool_config(tool_id)
        env_prefix = self.get_env_prefix(tool_id)

        # Check environment variable override
        env_url = os.getenv(f"{env_prefix}_URL")
        if env_url:
            return env_url

        # Fall back to configuration
        return tool_config.get("url", "")

    def get_tool_repository(self, tool_id: str) -> str:
        """
        Get the repository for a tool.

        Args:
            tool_id: The ID of the tool to get the repository for

        Returns:
            Tool repository
        """
        tool_config = self.get_tool_config(tool_id)
        env_prefix = self.get_env_prefix(tool_id)

        # Check environment variable override
        env_repo = os.getenv(f"{env_prefix}_REPO")
        if env_repo:
            return env_repo

        # Fall back to configuration
        return tool_config.get("repository", "")

    def get_tool_command(self, tool_id: str) -> str:
        """
        Get the command to start a tool.

        This method retrieves the explicit command from the tool configuration.

        Args:
            tool_id: The ID of the tool to get the command for

        Returns:
            Command to start the tool, or empty string if no command is specified
        """
        tool_config = self.get_tool_config(tool_id)
        env_prefix = self.get_env_prefix(tool_id)

        # Check environment variable override
        env_command = os.getenv(f"{env_prefix}_COMMAND")
        if env_command:
            return env_command

        # Get the command from the configuration
        return tool_config.get("command", "")

    def initialize_tools(self) -> List:
        """
        Initialize all enabled tools.

        Returns:
            List of initialized server objects
        """
        servers = []

        for tool_id, tool_config in self.tools_config.items():
            if not self.is_tool_enabled(tool_id):
                continue

            tool_name = tool_config.get("name", tool_id)
            log_message(f"Initializing {tool_name}...", "INFO")

            # TODO: Implement tool initialization

        return servers

    def get_api_key(self) -> str:
        """
        Get API key.

        Returns:
            API key
        """
        # Prioritize configuration
        return self.get_config("llm", "api_key", "")

    def get_api_base_url(self) -> str:
        """
        Get API base URL for the LLM provider.

        Returns:
            API base URL as a string
        """
        # Prioritize configuration
        return self.get_config("llm", "base_url", "http://0.0.0.0:4000")

    def get_model_name(self) -> str:
        """
        Get the model name to use.

        Returns:
            Model name
        """
        # Prioritize configuration
        return self.get_config("model", "name", "claude-3-7-sonnet-20240229")

    def get_model_temperature(self) -> float:
        """
        Get the model temperature to use.

        Returns:
            Model temperature
        """
        # Prioritize configuration
        return self.get_config("model", "temperature", 0.0)

    def get_log_level(self) -> str:
        """
        Get the log level to use.

        Returns:
            Log level
        """
        # Prioritize configuration
        log_level = self.get_config("logging", "level", "INFO")
        return log_level

    def get_log_file(self) -> Optional[str]:
        """
        Get the log file path to use.

        Returns:
            Log file path or None
        """
        # Prioritize configuration
        return self.get_config("logging", "file", None)

    def get_langfuse_config(self) -> Dict:
        """
        Get the Langfuse configuration.

        Returns:
            Langfuse configuration dictionary
        """
        config = self.get_config("monitoring", "langfuse", {})

        # Set enabled flag if keys are present
        if "public_key" in config and "secret_key" in config:
            config["enabled"] = True

        return config

    def get_llm_config(self) -> Dict:
        """
        Get the LLM configuration combining info from both config.yaml and litellm_config.yaml.

        Returns:
            Dictionary with complete LLM configuration
        """
        # First check for legacy model configuration
        if "model" in self.config and "name" in self.config.get("model", {}) and "temperature" in self.config.get("model", {}):
            return {
                "name": self.config.get("model", {}).get("name"),
                "temperature": self.config.get("model", {}).get("temperature", 1.0),
            }

        # Get LLM-specific configuration
        llm_config = self.config.get("llm", {})
        temperature = llm_config.get("temperature", 1.0)

        # Check for direct model specification (decoupled from litellm)
        if "model" in llm_config:
            return {
                "name": llm_config.get("model"),
                "temperature": temperature,
            }

        # Backward compatibility: check for litellm config
        if not self.litellm_config:
            return {
                "name": None,
                "temperature": temperature,
            }

        # Get the preferred model from the config or use first model
        preferred_model = llm_config.get("preferred_model")

        # Extract models from litellm config
        all_models = set()
        model_variant_configs = []

        if "model_list" in self.litellm_config:
            for model in self.litellm_config.get("model_list", []):
                all_models.add(model.get("model_name"))

                # Check if this is the preferred model
                if model.get("model_name") == preferred_model:
                    model_variant_configs.append(model)

        # Sort model variants by position in the list (priority)
        if not model_variant_configs and all_models:
            # Find all variants of the first model
            first_model = list(all_models)[0]
            for model in self.litellm_config.get("model_list", []):
                if model.get("model_name") == first_model:
                    model_variant_configs.append(model)

        # Choose first model variant
        model_config = None
        if model_variant_configs:
            model_config = model_variant_configs[0]

        # If preferred model not found but we have models, use the first one
        if not model_config and self.litellm_config.get("model_list"):
            model_config = self.litellm_config.get("model_list")[0]

        # Get server config for base_url
        server_config = self.litellm_config.get("server", {})
        host = server_config.get("host", "0.0.0.0")
        port = server_config.get("port", 4000)
        base_url = f"http://{host if host != '0.0.0.0' else 'localhost'}:{port}"

        return {
            "name": model_config.get("model_name") if model_config else None,
            "temperature": temperature,
            "base_url": base_url,
            "api_key": "sk-any-key",  # Default for local LiteLLM proxy
            "model_config": model_config,
            "all_models": list(all_models),
            "model_variants": model_variant_configs,
        }

    # Compatibility methods for existing code
    def get_api_key(self) -> str:
        """Get the API key for the LLM provider."""
        # Check for API key in llm section (new format)
        llm_api_key = self.config.get("llm", {}).get("api_key")
        if llm_api_key:
            return llm_api_key

        # Check for API key in api section (legacy format)
        legacy_api_key = self.config.get("api", {}).get("api_key")
        if legacy_api_key:
            return legacy_api_key

        # New method using get_llm_config()
        return self.get_llm_config().get("api_key")

    def get_api_base_url(self) -> str:
        """Get the base URL for the LLM API."""
        # Check for base URL in llm section (new format)
        llm_base_url = self.config.get("llm", {}).get("base_url")
        if llm_base_url:
            return llm_base_url

        # Check for base URL in api section (legacy format)
        legacy_base_url = self.config.get("api", {}).get("base_url")
        if legacy_base_url:
            return legacy_base_url

        # New method using get_llm_config()
        return self.get_llm_config().get("base_url")

    def get_model_name(self) -> str:
        """Get the name of the LLM model."""
        # Legacy method
        legacy_model_name = self.config.get("model", {}).get("name")
        if legacy_model_name:
            return legacy_model_name

        # New method using get_llm_config()
        return self.get_llm_config().get("name")

    def get_model_temperature(self) -> float:
        """Get the temperature setting for the LLM model."""
        # Legacy method
        legacy_temperature = self.config.get("model", {}).get("temperature")
        if legacy_temperature is not None:
            return legacy_temperature

        # New method using get_llm_config()
        return self.get_llm_config().get("temperature", 1.0)

    def get_litellm_config(self):
        """
        Get the full LiteLLM configuration.

        Returns:
            Dictionary containing LiteLLM configuration
        """
        return self.litellm_config

    def get_litellm_config_path(self):
        """
        Get the path to the LiteLLM configuration file.

        Returns:
            String path to the LiteLLM configuration file
        """
        litellm_config_path = self.config.get("llm", {}).get("config_file")
        if not litellm_config_path:
            # Default fallback path
            return os.path.join(os.getcwd(), "config", "litellm_config.yaml")

        # Handle relative paths
        if not os.path.isabs(litellm_config_path):
            # If the main config path is known, make path relative to it
            if self.config_path:
                config_dir = os.path.dirname(self.config_path)
                return os.path.join(config_dir, litellm_config_path)
            else:
                # Otherwise relative to current directory
                return os.path.join(os.getcwd(), litellm_config_path)

        return litellm_config_path


    def init_config(self) -> str:
        """
        Initialize the config file.

        Returns:
            Path to the config file
        """
        config_dir = os.path.dirname(self.config_path) if self.config_path else os.path.join(os.getcwd(), "config")
        os.makedirs(config_dir, exist_ok=True)
        config_file = os.path.join(config_dir, "config.yaml")

        # Create a default config file if it doesn't exist
        if not os.path.exists(config_file):
            with open(config_file, "w") as f:
                f.write("# Smart Agent Configuration\n")
                f.write("api:\n")
                f.write("  key: \"\"  # Your API key\n")
                f.write("  base_url: \"https://api.openai.com/v1\"\n")
                f.write("model:\n")
                f.write("  name: \"gpt-4o\"\n")
                f.write("  temperature: 0.7\n")

        return config_file

    def init_tools(self) -> str:
        """
        Initialize the tools config file.

        Returns:
            Path to the tools config file
        """
        config_dir = os.path.dirname(self.config_path) if self.config_path else os.path.join(os.getcwd(), "config")
        os.makedirs(config_dir, exist_ok=True)
        tools_file = os.path.join(config_dir, "tools.yaml")

        # Create a default tools file if it doesn't exist
        if not os.path.exists(tools_file):
            with open(tools_file, "w") as f:
                f.write("# Smart Agent Tools Configuration\n")
                f.write("search_tool:\n")
                f.write("  enabled: false\n")
                f.write("  name: \"Search Tool\"\n")
                f.write("  description: \"Search the web for information\"\n")
                f.write("  command: \"npx search-tool --port {port}\"\n")
                f.write("  url: \"http://localhost:{port}/sse\"\n")

        return tools_file


# For backward compatibility
class ToolManager(ConfigManager):
    """
    Legacy class for backward compatibility.
    """

    def __init__(self, config_path: Optional[str] = None):
        super().__init__(config_path)

    def get_mcp_servers(self) -> List:
        """
        Get all initialized MCP servers.

        Returns:
            List of MCP server objects
        """
        return []
