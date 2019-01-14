from django.views.decorators.csrf import csrf_exempt
from django.urls import path

from graphene_django.views import GraphQLView

from Graphql_Django.schema import schema


urlpatterns = [
    path('', GraphQLView.as_view(graphiql=True, schema=schema)),
]
