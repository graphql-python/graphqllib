from typing import Optional, overload

from ..language import TypeNode, NamedTypeNode, ListTypeNode, NonNullTypeNode
from ..type import (
    GraphQLType,
    GraphQLSchema,
    GraphQLNamedType,
    GraphQLList,
    GraphQLNonNull,
)

__all__ = ["type_from_ast"]


def type_from_ast(schema, type_node):  # noqa: F811
    """Get the GraphQL type definition from an AST node.

    Given a Schema and an AST node describing a type, return a GraphQLType
    definition which applies to that type. For example, if provided the parsed
    AST node for `[User]`, a GraphQLList instance will be returned, containing
    the type called "User" found in the schema. If a type called "User" is not
    found in the schema, then None will be returned.
    """
    if isinstance(type_node, ListTypeNode):
        inner_type = type_from_ast(schema, type_node.type)
        return GraphQLList(inner_type) if inner_type else None
    if isinstance(type_node, NonNullTypeNode):
        inner_type = type_from_ast(schema, type_node.type)
        return GraphQLNonNull(inner_type) if inner_type else None
    if isinstance(type_node, NamedTypeNode):
        return schema.get_type(type_node.name.value)
    raise TypeError("Unexpected type kind: {}".format(type_node.kind))