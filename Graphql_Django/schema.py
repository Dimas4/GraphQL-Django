import graphene

from graphql_start.schema import Query as Q, Mutation as M


class Query(Q, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=M)
