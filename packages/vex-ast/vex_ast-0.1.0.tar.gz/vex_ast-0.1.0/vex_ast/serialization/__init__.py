"""
Serialization package for VEX AST.

This package provides functionality for serializing and deserializing AST nodes
to and from JSON format, as well as generating JSON schema for the AST structure.
"""

from .json_serializer import (
    SerializationVisitor,
    serialize_ast_to_dict,
    serialize_ast_to_json
)
from .json_deserializer import (
    DeserializationFactory,
    deserialize_ast_from_dict,
    deserialize_ast_from_json
)
from .schema import (
    generate_ast_schema,
    export_schema_to_file
)

__all__ = [
    # Serialization
    "SerializationVisitor",
    "serialize_ast_to_dict",
    "serialize_ast_to_json",
    
    # Deserialization
    "DeserializationFactory",
    "deserialize_ast_from_dict",
    "deserialize_ast_from_json",
    
    # Schema
    "generate_ast_schema",
    "export_schema_to_file"
]
