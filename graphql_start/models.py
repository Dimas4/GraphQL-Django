from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    category = models.ForeignKey(Category, related_name='ingredients', on_delete=models.CASCADE)

    def articles_count(self):
        print('qqqq')
        return 'qq'

    def __str__(self):
        return self.title


