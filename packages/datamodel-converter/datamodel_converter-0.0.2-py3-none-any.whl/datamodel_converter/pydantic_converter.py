"""Convert Pydantic models to JSON schemas."""

from __future__ import annotations
import copy
from typing import Any, Literal
from pydantic import BaseModel


Flavors = Literal["vanilla", "openai_output_schema", "openai_tool_schema"]


def inline_schema(
    schema: dict[str, Any], include_title: bool = False
) -> dict[str, Any]:
    """Recursively inline $ref from $defs in a Pydantic JSON schema.

    Args:
        schema: The Pydantic JSON schema to inline.
        include_title: Whether to include the `title` fields in the schema.

    Returns:
        The inline JSON schema.
    """
    defs = schema.pop("$defs", {})
    schema_title = schema["title"]

    def resolve_refs(obj: dict[str, Any]) -> dict[str, Any]:
        if isinstance(obj, dict):
            if "$ref" in obj:
                ref_path = obj["$ref"]
                assert ref_path.startswith("#/$defs/")
                def_key = ref_path.split("/")[-1]
                resolved = copy.deepcopy(defs.get(def_key, {}))
                return resolve_refs(resolved)
            else:
                result = {}
                for k, v in obj.items():
                    if k == "title":
                        if include_title:
                            result[k] = v
                    else:
                        result[k] = resolve_refs(v)
                return result
        elif isinstance(obj, list):
            return [resolve_refs(item) for item in obj]
        else:
            return obj

    schema = resolve_refs(schema)
    schema["title"] = schema_title
    return schema


def recursive_add_additional_properties(schema: dict[str, Any]) -> None:
    """Recursively add `additionalProperties` to a Pydantic JSON schema.

    Args:
        schema: The Pydantic JSON schema to add `additionalProperties` to.
    """
    # Only add additionalProperties to objects
    if schema.get("type") == "object" and "additionalProperties" not in schema:
        schema["additionalProperties"] = False

    # Recursively process all values
    for value in schema.values():
        if isinstance(value, dict):
            recursive_add_additional_properties(value)


def pydantic_converter(
    model: BaseModel, include_title: bool = False, flavor: Flavors = "vanilla"
) -> dict[str, Any]:
    """Convert a Pydantic model to an inline JSON schema.

    Args:
        model: The Pydantic model to convert.
        include_title: Whether to include the `title` fields in the schema.
        flavor: The flavor of the output schema.

    Returns:
        The inline JSON schema.
    """
    schema = inline_schema(model.model_json_schema(), include_title)
    match flavor:
        case "openai_output_schema":
            schema["name"] = schema.pop("title")
            schema["strict"] = True
            recursive_add_additional_properties(schema)
            schema["schema"] = {
                "type": schema.pop("type"),
                "properties": schema.pop("properties"),
                "additionalProperties": schema.pop("additionalProperties"),
                "required": schema.pop("required"),
            }
        case "openai_tool_schema":
            schema["name"] = schema.pop("title")
            schema["strict"] = True
            recursive_add_additional_properties(schema)
            schema["parameters"] = {
                "type": schema.pop("type"),
                "properties": schema.pop("properties"),
                "additionalProperties": schema.pop("additionalProperties"),
                "required": schema.pop("required"),
            }
        case _:
            pass

    return schema
