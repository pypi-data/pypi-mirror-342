from __future__ import annotations
import copy
from pydantic import BaseModel, Field
from datamodel_converter.pydantic_converter import pydantic_converter


class MathResponse(BaseModel):
    """A response to a math problem"""

    steps: list[Step]
    final_answer: str


class Step(BaseModel):
    explanation: str = Field(..., description="The explanation of the step")
    output: str = Field(..., description="The output of the step")


step_schema_with_title = Step.model_json_schema()

plain_schema = {
    "title": "MathResponse",
    "description": "A response to a math problem",
    "type": "object",
    "properties": {
        "steps": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "explanation": {
                        "type": "string",
                        "description": "The explanation of the step",
                    },
                    "output": {
                        "type": "string",
                        "description": "The output of the step",
                    },
                },
                "required": ["explanation", "output"],
            },
        },
        "final_answer": {"type": "string"},
    },
    "required": ["steps", "final_answer"],
}

child_properties = copy.deepcopy(plain_schema["properties"])
child_properties["steps"]["items"]["additionalProperties"] = False
openai_output_schema = {
    "name": plain_schema["title"],
    "description": plain_schema["description"],
    "strict": True,
    "schema": {
        "type": "object",
        "properties": {
            **child_properties,
        },
        "additionalProperties": False,
        "required": plain_schema["required"],
    },
}

openai_tool_schema = {
    "name": plain_schema["title"],
    "description": plain_schema["description"],
    "strict": True,
    "parameters": {
        "type": "object",
        "properties": {
            **child_properties,
        },
        "additionalProperties": False,
        "required": plain_schema["required"],
    },
}


def test_pydantic_converter():
    assert pydantic_converter(MathResponse) == plain_schema


def test_pydantic_converter_openai_output_schema():
    assert (
        pydantic_converter(MathResponse, flavor="openai_output_schema")
        == openai_output_schema
    )


def test_pydantic_converter_openai_tool_schema():
    assert (
        pydantic_converter(MathResponse, flavor="openai_tool_schema")
        == openai_tool_schema
    )


def test_pydantic_converter_simple_schema_with_title():
    assert pydantic_converter(Step, include_title=True) == step_schema_with_title
