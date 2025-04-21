# Datamodel Converter

[![CI](https://github.com/ShaojieJiang/datamodel-converter/actions/workflows/ci.yml/badge.svg?event=push)](https://github.com/ShaojieJiang/datamodel-converter/actions/workflows/ci.yml?query=branch%3Amain)
[![Coverage](https://coverage-badge.samuelcolvin.workers.dev/ShaojieJiang/datamodel-converter.svg)](https://coverage-badge.samuelcolvin.workers.dev/redirect/ShaojieJiang/datamodel-converter)
[![PyPI](https://img.shields.io/pypi/v/datamodel-converter.svg)](https://pypi.python.org/pypi/datamodel-converter)

Every time I need to specify output schema for LLMs, I need to write a converter from Pydantic models to the schema.
Pydantic V2's `model_json_schema` is not supported by some platforms like OpenAI or n8n.
This package provides a converter for this purpose.

## Installation

```bash
pip install datamodel-converter
```

## Example

```python
import json
from pydantic import BaseModel
from datamodel_converter.pydantic_converter import pydantic_converter


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

print("OpenAI output schema:")
print(json.dumps(pydantic_converter(Person, flavor="openai_output_schema"), indent=2))
print()
```
Output:
```json
Pydantic schema:
{
  "$defs": {
    "Address": {
      "description": "Address model.",
      "properties": {
        "street": {
          "title": "Street",
          "type": "string"
        },
        "city": {
          "title": "City",
          "type": "string"
        },
        "state": {
          "title": "State",
          "type": "string"
        },
        "zip": {
          "title": "Zip",
          "type": "string"
        }
      },
      "required": [
        "street",
        "city",
        "state",
        "zip"
      ],
      "title": "Address",
      "type": "object"
    }
  },
  "description": "Person model.",
  "properties": {
    "name": {
      "title": "Name",
      "type": "string"
    },
    "age": {
      "title": "Age",
      "type": "integer"
    },
    "addresses": {
      "description": "Person might have multiple addresses.",
      "items": {
        "$ref": "#/$defs/Address"
      },
      "title": "Addresses",
      "type": "array"
    }
  },
  "required": [
    "name",
    "age",
    "addresses"
  ],
  "title": "Person",
  "type": "object"
}

OpenAI output schema:
{
  "description": "Person model.",
  "name": "Person",
  "strict": true,
  "schema": {
    "type": "object",
    "properties": {
      "name": {
        "type": "string"
      },
      "age": {
        "type": "integer"
      },
      "addresses": {
        "description": "Person might have multiple addresses.",
        "items": {
          "description": "Address model.",
          "properties": {
            "street": {
              "type": "string"
            },
            "city": {
              "type": "string"
            },
            "state": {
              "type": "string"
            },
            "zip": {
              "type": "string"
            }
          },
          "required": [
            "street",
            "city",
            "state",
            "zip"
          ],
          "type": "object",
          "additionalProperties": false
        },
        "type": "array"
      }
    },
    "additionalProperties": false,
    "required": [
      "name",
      "age",
      "addresses"
    ]
  }
}
```

## Related works

- [datamodel-code-generator](https://github.com/koxudaxi/datamodel-code-generator/): Generate Pydantic models from JSON Schema (opposite direction of this package).
