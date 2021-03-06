# Generated by Django 2.1.2 on 2018-11-01 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('graphql_start', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='graphql_start.Category')),
            ],
        ),
        migrations.RemoveField(
            model_name='ingredient',
            name='category',
        ),
        migrations.DeleteModel(
            name='Ingredient',
        ),
    ]
