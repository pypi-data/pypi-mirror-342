import json
from os import PathLike
from pathlib import Path
from typing import Dict, Any, Optional, Type, Union

from belso.schemas import Schema, Field
from belso.utils.logging import get_logger

# Get a module-specific logger
logger = get_logger(__name__)

def schema_to_json(
        schema: Type[Schema],
        file_path: Optional[Union[str, Path, PathLike]] = None
    ) -> Dict[str, Any]:
    """
    Convert a belso Schema to a standardized JSON format and optionally save to a file.\n
    ---
    ### Args
    - `schema` (`Type[Schema]`): the schema to convert.\n
    - `file_path` (`Optional[Union[str, Path, PathLike]]`): path to save the JSON to a file.\n
    ---
    ### Returns
    - `Dict[str, Any]`: the schema in JSON format.
    """
    try:
        schema_name = schema.name if hasattr(schema, "name") else "unnamed"
        logger.debug(f"Starting conversion of schema '{schema_name}' to JSON format...")

        fields_json = []
        logger.debug(f"Processing {len(schema.fields)} fields...")

        for field in schema.fields:
            # Convert Python type to string representation
            type_str = field.type.__name__ if hasattr(field.type, "__name__") else str(field.type)
            logger.debug(f"Processing field '{field.name}' of type '{type_str}'...")

            field_json = {
                "name": field.name,
                "type": type_str,
                "description": field.description,
                "required": field.required
            }

            # Only include default if it exists
            if field.default is not None:
                field_json["default"] = field.default
                logger.debug(f"Field '{field.name}' has default value: {field.default}.")

            fields_json.append(field_json)

        schema_json = {
            "name": schema.name,
            "fields": fields_json
        }

        # Save to file if path is provided
        if file_path:
            logger.debug(f"Saving JSON schema to file: {file_path}.")
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(schema_json, f, indent=2)
                logger.debug(f"Successfully saved JSON schema to {file_path}.")
            except Exception as e:
                logger.error(f"Failed to save JSON schema to file: {e}")
                logger.debug("File saving error details", exc_info=True)

        logger.debug("Successfully converted schema to JSON format.")
        return schema_json

    except Exception as e:
        logger.error(f"Error converting schema to JSON format: {e}")
        logger.debug("Conversion error details", exc_info=True)
        return {"name": "ErrorSchema", "fields": []}

def json_to_schema(json_input: Union[Dict[str, Any], str]) -> Type[Schema]:
    """
    Convert a standardized JSON format or JSON file to a belso Schema.\n
    ---
    ### Args
    - `json_input`: either a JSON dictionary or a file path to a JSON file.\n
    ---
    ### Returns
    - `Type[Schema]`: the belso Schema.
    """
    try:
        # Check if input is a file path
        if isinstance(json_input, str):
            # Try to load as a file
            logger.debug(f"Attempting to load JSON from file: {json_input}.")
            try:
                with open(json_input, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
                logger.debug(f"Successfully loaded JSON from file: {json_input}.")
            except (FileNotFoundError, json.JSONDecodeError) as e:
                logger.error(f"Failed to load JSON from file: {e}")
                logger.debug("File loading error details", exc_info=True)
                raise ValueError(f"Failed to load JSON from file: {e}")
        else:
            # Assume it's already a JSON dictionary
            logger.debug("Processing provided JSON dictionary...")
            json_data = json_input

        # Create a new Schema class
        schema_name = json_data.get("name", "LoadedSchema")
        logger.debug(f"Creating new Schema class with name: {schema_name}.")

        class LoadedSchema(Schema):
            name = schema_name
            fields = []

        # Type mapping from string to Python types
        type_mapping = {
            "str": str,
            "int": int,
            "float": float,
            "bool": bool,
            "list": list,
            "dict": dict,
            "any": Any
        }

        # Process each field
        fields_data = json_data.get("fields", [])
        logger.debug(f"Processing {len(fields_data)} fields from JSON...")

        for field_data in fields_data:
            field_name = field_data.get("name", "")
            field_type_str = field_data.get("type", "str")
            field_type = type_mapping.get(field_type_str.lower(), str)

            logger.debug(f"Processing field '{field_name}' with type '{field_type_str}'...")

            # Get required status
            required = field_data.get("required", True)
            required_status = "required" if required else "optional"
            logger.debug(f"Field '{field_name}' is {required_status}")

            # Get default value if present
            default = field_data.get("default")
            if default is not None:
                logger.debug(f"Field '{field_name}' has default value: {default}")

            field = Field(
                name=field_name,
                type=field_type,
                description=field_data.get("description", ""),
                required=required,
                default=default
            )

            LoadedSchema.fields.append(field)

        logger.debug(f"Successfully created Schema with {len(LoadedSchema.fields)} fields.")
        return LoadedSchema

    except Exception as e:
        logger.error(f"Error converting JSON to schema: {e}")
        logger.debug("Conversion error details", exc_info=True)
        # Return a minimal schema if conversion fails
        logger.warning("Returning fallback schema due to conversion error.")
        class FallbackSchema(Schema):
            name = "FallbackSchema"
            fields = [Field(name="text", type=str, description="Fallback field", required=True)]
        return FallbackSchema
