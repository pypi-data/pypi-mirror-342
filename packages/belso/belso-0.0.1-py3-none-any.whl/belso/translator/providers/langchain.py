from typing import Any, Dict, Type

from belso.schemas import Schema, Field
from belso.utils.logging import get_logger
from belso.utils.schema_helpers import (
    map_json_to_python_type,
    build_properties_dict,
    create_fallback_schema
)

# Get a module-specific logger
logger = get_logger(__name__)

def to_langchain(schema: Type[Schema]) -> Dict[str, Any]:
    """
    Translate a standard schema to LangChain format.\n
    ---
    ### Args
    - `schema`: the schema to convert.\n
    ---
    ### Returns
    - `Dict[str, Any]`: the converted schema as a dictionary for LangChain.
    """
    try:
        schema_name = schema.__name__ if hasattr(schema, "__name__") else "unnamed"
        logger.debug(f"Starting translation of schema '{schema_name}' to LangChain format...")

        properties = build_properties_dict(schema)
        required_fields = schema.get_required_fields()

        logger.debug(f"Found {len(schema.fields)} fields, {len(required_fields)} required.")

        # Create the schema in LangChain format
        langchain_schema = {
            "title": schema_name,
            "type": "object",
            "properties": properties,
            "required": required_fields
        }

        logger.debug("Successfully created LangChain schema.")
        return langchain_schema

    except Exception as e:
        logger.error(f"Error translating schema to LangChain format: {e}")
        logger.debug("Translation error details", exc_info=True)
        return {}

def from_langchain(schema: Dict[str, Any]) -> Type[Schema]:
    """
    Convert a LangChain schema to belso Schema format.\n
    ---
    ### Args
    - `schema`: the schema to convert.\n
    ---
    ### Returns
    - `Type`: the converted schema as a belso Schema subclass.
    """
    try:
        logger.debug("Starting conversion from LangChain schema to belso format...")

        # Create a new Schema class
        class ConvertedSchema(Schema):
            name = schema.get("title", "ConvertedFromLangChain")
            fields = []

        # Extract properties
        properties = schema.get("properties", {})
        required_fields = schema.get("required", [])

        logger.debug(f"Found {len(properties)} properties, {len(required_fields)} required fields.")

        # Convert each property
        for name, prop in properties.items():
            prop_type = prop.get("type", "string")
            field_type = map_json_to_python_type(prop_type)
            description = prop.get("description", "")
            required = name in required_fields
            default = prop.get("default") if not required else None

            logger.debug(f"Converting property '{name}' of JSON Schema type '{prop_type}' to Python type '{field_type.__name__}'...")
            logger.debug(f"Property '{name}' is {'required' if required else 'optional'}.")

            if default is not None:
                logger.debug(f"Property '{name}' has default value: {default}.")

            ConvertedSchema.fields.append(
                Field(
                    name=name,
                    type=field_type,
                    description=description,
                    required=required,
                    default=default
                )
            )

        logger.debug(f"Successfully converted LangChain schema to belso schema with {len(ConvertedSchema.fields)} fields.")
        return ConvertedSchema

    except Exception as e:
        logger.error(f"Error converting LangChain schema to belso format: {e}")
        logger.debug("Conversion error details", exc_info=True)
        # Return a minimal schema if conversion fails
        return create_fallback_schema()
