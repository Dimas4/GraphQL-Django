import graphene

from graphene_django.types import DjangoObjectType

from .models import Category, Ingredient


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class Query:
    category = graphene.Field(CategoryType,
                              id=graphene.Int(),
                              name=graphene.String())

    all_categories = graphene.List(CategoryType, first=graphene.Int(), last=graphene.Int())

    def resolve_all_categories(self, info, first=None, last=None):
        categories = Category.objects.all()
        return categories[len(categories) - last:first] if last else categories[:first]

    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Category.objects.get(pk=id)

        if name is not None:
            return Category.objects.get(name=name)

        return None


class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    category = graphene.Field(CategoryType)

    def mutate(self, info, name=None):
        category = Category(name=name)
        category.save()
        return CreateCategory(category=category)


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()


"""
mutation {
  createCategory(name: "name"){
    category{
	    name
    }
  }
}
"""
