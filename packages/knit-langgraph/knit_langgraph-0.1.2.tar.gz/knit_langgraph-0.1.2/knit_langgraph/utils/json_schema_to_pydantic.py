# json_schema_to_pydantic.py

import json
import re
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, create_model, constr


def convert_json_schema_to_pydantic_model(
    schema_json: str, model_name: str = "RootModel"
) -> BaseModel:
    """
    Convert a JSON schema string to a Pydantic BaseModel class.

    Args:
        schema_json: The JSON schema as a string
        model_name: The name for the root model class

    Returns:
        A Pydantic BaseModel class
    """
    if isinstance(schema_json, str):
        schema = json.loads(schema_json)
    else:
        schema = schema_json

    # If we have an input_schema property, use that as the schema
    if "input_schema" in schema:
        schema = schema["input_schema"]

    # Get a better model name if available
    if "id" in schema and not model_name:
        id_parts = re.split(r"[_\-.]", schema["id"])
        model_name = "".join(part.capitalize() for part in id_parts)

    return create_pydantic_model(schema, model_name)


def create_pydantic_model(schema: Dict[str, Any], model_name: str) -> BaseModel:
    """Recursively create Pydantic models from a JSON schema."""
    
    print(schema, model_name)
    
    model_fields = {}

    if schema.get("type") == "object" and "properties" in schema:
        required_fields = set(schema.get("required", []))

        for prop_name, prop_schema in schema["properties"].items():
            print("Model Fields", model_fields)
            
            print(prop_name, prop_schema)
            
            is_required = prop_name in required_fields

            # Handle nested objects
            if prop_schema.get("type") == "object" and "properties" in prop_schema:
                nested_model_name = f"{model_name}{prop_name.capitalize()}"
                nested_model = create_pydantic_model(prop_schema, nested_model_name)

                model_fields[prop_name] = (
                    Optional[nested_model] if not is_required else nested_model,
                    Field(... if is_required else None),
                )

            # Handle arrays
            elif prop_schema.get("type") == "array" and "items" in prop_schema:
                items = prop_schema["items"]

                if items.get("type") == "object" and "properties" in items:
                    # Array of objects
                    nested_model_name = f"{model_name}{prop_name.capitalize()}Item"
                    nested_model = create_pydantic_model(items, nested_model_name)

                    model_fields[prop_name] = (
                        (
                            Optional[List[nested_model]]
                            if not is_required
                            else List[nested_model]
                        ),
                        Field(... if is_required else None),
                    )
                else:
                    # Array of primitives
                    item_type = get_python_type(items.get("type", "string"))

                    model_fields[prop_name] = (
                        (
                            Optional[List[item_type]]
                            if not is_required
                            else List[item_type]
                        ),
                        Field(... if is_required else None),
                    )

            # Handle primitive types with validation
            elif prop_schema.get("type") == "string" and "pattern" in prop_schema:
                pattern = prop_schema["pattern"]

                model_fields[prop_name] = (
                    (
                        Optional[constr(pattern=pattern)]
                        if not is_required
                        else constr(pattern=pattern)
                    ),
                    Field(... if is_required else None),
                )

            # Handle primitive types and other cases
            else:
                field_type = get_python_type(prop_schema.get("type", "string"))
                field_args = {}

                # Add validation constraints
                if "minimum" in prop_schema:
                    field_args["ge"] = prop_schema["minimum"]
                if "maximum" in prop_schema:
                    field_args["le"] = prop_schema["maximum"]
                if "minLength" in prop_schema:
                    field_args["min_length"] = prop_schema["minLength"]
                if "maxLength" in prop_schema:
                    field_args["max_length"] = prop_schema["maxLength"]

                model_fields[prop_name] = (
                    Optional[field_type] if not is_required else field_type,
                    Field(... if is_required else None, **field_args),
                )

    # Create the model class
    model = create_model(model_name, **model_fields)

    # Add docstring if available
    if "description" in schema or "summary" in schema:
        model.__doc__ = schema.get("description", schema.get("summary", ""))

    return model


def get_python_type(json_type: str) -> type:
    """Convert JSON schema type to Python type."""
    type_mapping = {
        "string": str,
        "integer": int,
        "number": float,
        "boolean": bool,
        "null": None,
        "array": list,
        "object": dict,
    }
    return type_mapping.get(json_type, Any)
