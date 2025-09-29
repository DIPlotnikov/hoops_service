from typing import (
    Any,
    Dict,
    Optional,
)

from graphql.language.ast import EnumValueDefinitionNode
from graphql.pyutils import is_description


class MonkeyPathingGraphQLEnumValue:
    def __init__(
        self,
        value: Any = None,
        description: Optional[str] = None,
        deprecation_reason: Optional[str] = None,
        extensions: Optional[Dict[str, Any]] = None,
        ast_node: Optional[EnumValueDefinitionNode] = None,
    ) -> None:
        if description is not None and not is_description(description):
            raise TypeError("The description of the enum value must be a string.")
        if deprecation_reason is not None and not is_description(deprecation_reason):
            raise TypeError("The deprecation reason for the enum value must be a string.")
        if extensions is None:
            extensions = {}
        elif not isinstance(extensions, dict) or not all(isinstance(key, str) for key in extensions):
            raise TypeError("Enum value extensions must be a dictionary with string keys.")
        if ast_node and not isinstance(ast_node, EnumValueDefinitionNode):
            raise TypeError("AST node must be an EnumValueDefinitionNode.")
        self.value = value.value
        self.description = description
        self.deprecation_reason = deprecation_reason
        self.extensions = extensions
        self.ast_node = ast_node
