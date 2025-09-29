import logging

import graphene
from graphene_django.types import DjangoObjectType

from ..models import Coordinates

logger = logging.getLogger(__name__)


class CoordinatesType(DjangoObjectType):
    class Meta:
        model = Coordinates
        exclude = ("zoom", "hotel_fact_address")


class coordinatesInput(graphene.InputObjectType):
    latitude = graphene.Float(required=True)
    longitude = graphene.Float(required=True)
    address = graphene.String(required=True)
    label = graphene.String(required=True)
