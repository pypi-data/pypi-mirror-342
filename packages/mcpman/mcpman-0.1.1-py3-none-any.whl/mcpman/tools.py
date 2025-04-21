import re
import logging
import json
from typing import Dict, Any, List, Optional, Tuple


def sanitize_name(name: str) -> str:
    """
    Sanitize a name to be a valid identifier.
    
    Args:
        name: Input name to sanitize
        
    Returns:
        Sanitized name with non-alphanumeric characters replaced with underscores
    """
    # Replace non-alphanumeric characters with underscores
    sanitized = re.sub(r"[^a-zA-Z0-9_]", "_", name)
    # Ensure it doesn't start with a digit
    if sanitized and sanitized[0].isdigit():
        sanitized = "_" + sanitized
    # Replace multiple consecutive underscores with a single one
    sanitized = re.sub(r"_+", "_", sanitized)
    return sanitized


class Tool:
    """
    Represents a tool with its properties and formatting capabilities.
    
    A tool is a function that can be called by an LLM to perform an action.
    Each tool has a name, description, and input schema.
    """

    def __init__(
        self,
        name: str,
        description: str,
        input_schema: Dict[str, Any],
        original_name: str,
    ) -> None:
        """
        Initialize a Tool instance.
        
        Args:
            name: Prefixed tool name (e.g., "calculator_add")
            description: Human-readable description of what the tool does
            input_schema: JSON schema describing the tool's input parameters
            original_name: Tool name without prefix (e.g., "add")
        """
        self.name: str = name  # Prefixed name (e.g., calculator_add)
        self.description: str = description
        self.input_schema: Dict[str, Any] = input_schema
        self.original_name: str = original_name  # Original name (e.g., add)

    def to_openai_schema(self) -> Dict[str, Any]:
        """
        Format the tool definition for the OpenAI API 'tools' parameter.
        
        Returns:
            Dictionary matching OpenAI's tool schema format
        """
        parameters_schema = {"type": "object", "properties": {}, "required": []}
        
        if isinstance(self.input_schema, dict):
            # Extract and sanitize properties
            input_props = self.input_schema.get("properties")
            if isinstance(input_props, dict):
                sanitized_props = {}
                for name, prop_info in input_props.items():
                    if isinstance(prop_info, dict) and "type" in prop_info:
                        sanitized_props[name] = prop_info
                    else:
                        sanitized_props[name] = {
                            "type": "string",
                            "description": str(
                                prop_info.get(
                                    "description", "Parameter without defined type"
                                )
                            ),
                        }
                        logging.warning(
                            f"Property '{name}' in tool '{self.name}' schema missing type, defaulting to string."
                        )
                parameters_schema["properties"] = sanitized_props
            
            # Extract required fields
            input_required = self.input_schema.get("required")
            if isinstance(input_required, list):
                parameters_schema["required"] = [
                    req
                    for req in input_required
                    if req in parameters_schema["properties"]
                ]

        # Construct the final schema
        tool_schema = {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": parameters_schema,
            },
        }
        
        logging.debug(
            f"Generated OpenAI schema for tool '{self.name}': {json.dumps(tool_schema)}"
        )
        return tool_schema


def parse_tool_call(
    tool_call: Dict[str, Any], 
    prefixed_tool_name: Optional[str] = None
) -> Tuple[Optional[str], Optional[str], Dict[str, Any]]:
    """
    Parse a tool call from the LLM response.
    
    Args:
        tool_call: Tool call object from the LLM response
        prefixed_tool_name: Optional prefixed tool name (if already known)
        
    Returns:
        Tuple of (server_name, tool_name, arguments)
    """
    # Extract tool call details
    if not prefixed_tool_name:
        prefixed_tool_name = tool_call["function"]["name"]
    
    # Parse arguments
    try:
        arguments_str = tool_call["function"]["arguments"]
        arguments = json.loads(arguments_str)
    except json.JSONDecodeError as e:
        logging.error(f"Error decoding arguments JSON for {prefixed_tool_name}: {e}")
        arguments = {}
    
    # Parse server and tool names from the prefixed name
    server_name = None
    tool_name = None
    
    # The splitting logic might depend on your naming convention
    parts = prefixed_tool_name.split("_", 1)
    if len(parts) == 2:
        server_name, tool_name = parts
    
    return server_name, tool_name, arguments