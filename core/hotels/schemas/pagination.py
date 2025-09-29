from graphene import Connection
from graphene.relay.connection import ConnectionOptions, PageInfo
import re
from collections import OrderedDict

try:
    from collections.abc import Iterable
except ImportError:
    from collections import Iterable
from graphene.types import Enum, Int, Interface, List, NonNull, Scalar, String, Union
from graphene.types.field import Field
from graphene.types.objecttype import ObjectType


class ExtendedConnection(Connection):
    class Meta:
        abstract = True

    total_count = Int(required=True)
    edge_count = Int(required=True)

    def resolve_total_count(root, info, **kwargs):
        return root.length

    def resolve_edge_count(root, info, **kwargs):
        return len(root.edges)

    @classmethod
    def __init_subclass_with_meta__(cls, node=None, name=None, **options):
        _meta = ConnectionOptions(cls)
        assert node, "You have to provide a node in {}.Meta".format(cls.__name__)
        assert isinstance(node, NonNull) or issubclass(
            node, (Scalar, Enum, ObjectType, Interface, Union, NonNull)
        ), ('Received incompatible node "{}" for Connection {}.').format(
            node, cls.__name__
        )

        base_name = re.sub("Connection$", "", name or cls.__name__) or node._meta.name
        if not name:
            name = "{}Connection".format(base_name)

        edge_class = getattr(cls, "Edge", None)
        _node = node

        class EdgeBase(object):
            node = Field(_node, description="Кастомная нода", required=True)
            cursor = String(required=True, description="A cursor for use in pagination")

        class EdgeMeta:
            description = "A Relay edge containing a `{}` and its cursor.".format(
                base_name
            )

        edge_name = "{}Edge".format(base_name)
        if edge_class:
            edge_bases = (edge_class, EdgeBase, ObjectType)
        else:
            edge_bases = (EdgeBase, ObjectType)

        edge = type(edge_name, edge_bases, {"Meta": EdgeMeta})
        cls.Edge = edge

        options["name"] = name
        _meta.node = node
        _meta.fields = OrderedDict(
            [
                (
                    "page_info",
                    Field(
                        PageInfo,
                        name="pageInfo",
                        required=True,
                        description="Информация о пагинации текущего линка",
                    ),
                ),
                (
                    "edges",
                    Field(
                        NonNull(List(NonNull(edge))),
                        description="Список нод",
                    ),
                ),
            ]
        )
        return super(Connection, cls).__init_subclass_with_meta__(
            _meta=_meta, **options
        )
