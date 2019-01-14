import collections
import copy

import graphene

from graphene_django.types import DjangoObjectType
from graphene_django.debug import DjangoDebug

from .models import Category, Article
from graphql.execution.base import collect_fields


fields_all = set()


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class ArticleType(DjangoObjectType):
    articles_count = graphene.String(source='articles_count')

    class Meta:
        model = Article


class Query:
    category = graphene.Field(CategoryType,
                              id=graphene.Int(),
                              name=graphene.String())
    article = graphene.Field(ArticleType,
                             id=graphene.Int(),
                             name=graphene.String())

    all_categories = graphene.List(CategoryType, first=graphene.Int(), last=graphene.Int())
    all_articles = graphene.List(ArticleType, first=graphene.Int(), last=graphene.Int())

    debug = graphene.Field(DjangoDebug, name='__debug')

    @staticmethod
    def fields_from_request_info(request_info):
        query_fields = []
        for query in request_info.field_asts:
            fields = collect_fields(
                request_info.context,
                request_info.parent_type,
                query.selection_set,
                collections.defaultdict(list),
                set()
            )
            for key, value in fields.items():
                query_fields.append(key)
        return query_fields

    def resolve_all_categories(self, info, first=None, last=None):
        query_fields = Query.fields_from_request_info(info)

        categories = Category.objects.only(*query_fields)[:5]
        return categories[len(categories) - last:first] if last else categories[:first]

    def resolve_category(self, info, **kwargs):
        id = kwargs.get('id')
        name = kwargs.get('name')

        if id is not None:
            return Category.objects.get(pk=id)

        if name is not None:
            return Category.objects.get(name=name)

        return None

    @staticmethod
    def rec(field, name):
        if hasattr(field, 'selection_set') and hasattr(field.selection_set, 'selections'):
            for inner_field in field.selection_set.selections:
                Query.rec(field.selection_set.selections, f"{name}__{inner_field.name.value}")
        fields_all.add(name)

    @staticmethod
    def recursive_fields(request_info):
        fields = request_info.field_asts[0]

        for field in fields.selection_set.selections:
            if hasattr(field, 'selection_set') and hasattr(field.selection_set, 'selections'):
                Query.rec(field, field.name.value)
                continue
            fields_all.add(field.name.value)
        return fields_all

    def resolve_all_articles(self, info, first=None, last=None):
        query_fields = Query.recursive_fields(info)

        articles = Article.objects.only(*query_fields)

        if 'category' in query_fields:
            articles = articles.select_related('category')

        return articles[len(articles) - last:first] if last else articles[:first]

    def resolve_article(self, info, **kwargs):
        id = kwargs.get('id')
        title = kwargs.get('title')

        if id is not None:
            return Article.objects.get(pk=id)

        if title is not None:
            return Article.objects.get(name=title)

        return None


class CreateCategory(graphene.Mutation):
    class Arguments:
        name = graphene.String()

    category = graphene.Field(CategoryType)

    def mutate(self, info, name=None):
        category = Category(name=name)
        category.save()
        return CreateCategory(category=category)


class CreateArticle(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        content = graphene.String()
        category_name = graphene.String()

    article = graphene.Field(ArticleType)

    def mutate(self, info, title=None, content=None, category_name=None):
        category = Category.objects.get_or_create(name=category_name)[0]

        article = Article(title=title, content=content, category=category)
        article.save()
        return CreateArticle(article=article)


class DeleteCategory(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    category = graphene.Field(CategoryType)

    def mutate(self, info, id=None):
        category = Category.objects.get(id=id)
        obj = copy.copy(category)
        category.delete()
        return DeleteCategory(category=obj)


class DeleteArticle(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    article = graphene.Field(ArticleType)

    def mutate(self, info, id=None):
        article = Article.objects.get(id=id)
        obj = copy.copy(article)
        article.delete()
        return DeleteArticle(article=obj)


class UpdateCategory(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        name = graphene.String()

    category = graphene.Field(CategoryType)

    def mutate(self, info, id=None, name=None):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return UpdateCategory(category=category)


class UpdateArticle(graphene.Mutation):
    class Arguments:
        id = graphene.Int()
        title = graphene.String()
        content = graphene.String()
        category_id = graphene.Int()

    article = graphene.Field(ArticleType)

    def mutate(self, info, id=None, title=None, content=None, category_id=None):
        article = Article.objects.get(id=id)
        if title:
            article.title = title
        if content:
            article.content = content
        if category_id:
            article.category = Category.objects.get(id=category_id)
        article.save()

        return UpdateArticle(article=article)


class Mutation(graphene.ObjectType):
    create_category = CreateCategory.Field()
    create_article = CreateArticle.Field()
    delete_category = DeleteCategory.Field()
    delete_article = DeleteArticle.Field()
    update_category = UpdateCategory.Field()
    update_article = UpdateArticle.Field()


"""
mutation {
  createCategory(name: "name"){
    category{
	    name
    }
  }
}
"""
