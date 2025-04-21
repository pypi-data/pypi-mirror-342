"""Example usage of the datamodel_converter."""

import json
from pydantic import BaseModel
from datamodel_converter import pydantic_converter


class Address(BaseModel):
    """Address model."""

    street: str
    city: str
    state: str
    zip: str


class Person(BaseModel, use_attribute_docstrings=True):
    """Person model."""

    name: str
    age: int
    addresses: list[Address]
    """Person might have multiple addresses."""


print("Pydantic schema:")
print(json.dumps(Person.model_json_schema(), indent=2))
print()

print("Pydantic converter:")
print(json.dumps(pydantic_converter(Person, flavor="openai_output_schema"), indent=2))
print()
