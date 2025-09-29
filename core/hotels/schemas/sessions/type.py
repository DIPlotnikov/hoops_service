from graphene import String, ID, ObjectType


class SessionType(ObjectType):
    id = ID(required=True)
    user_agent = String(required=True)
