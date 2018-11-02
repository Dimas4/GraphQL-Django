import graphene
import copy

from graphene_django.types import DjangoObjectType

from .models import Category, Article


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category


class ArticleType(DjangoObjectType):
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

    def resolve_all_articles(self, info, first=None, last=None):
        articles = Article.objects.all()
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
