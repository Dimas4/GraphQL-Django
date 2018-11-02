import graphene
import json

from datetime import datetime


class User(graphene.ObjectType):
    id = graphene.ID()
    username = graphene.String()
    last_login = graphene.DateTime(required=False)


class CreateUser(graphene.Mutation):
    class Arguments:
        username = graphene.String()

    user = graphene.Field(User)

    def mutate(self, info, username):
        user = User(username=username)
        return CreateUser(user=user)


class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()


schema = graphene.Schema(mutation=Mutation)

# result = schema.execute(
#     """
#     {
#         users(last: 2) {
#             username
#             lastLogin
#         }
#     }
#     """
# )

result = schema.execute(
    """
    mutation createUser($username: String) {
        createUser(username: $username){
            user {
                username
            }
        }
    }
    """,
    variable_values={'username': "Bob"}
)

items = dict(result.data.items())
print(json.dumps(items, indent=4))
