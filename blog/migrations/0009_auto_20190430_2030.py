# Generated by Django 2.1 on 2019-04-30 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_remove_blog_readed_num'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='readnum',
            name='blog',
        ),
        migrations.DeleteModel(
            name='ReadNum',
        ),
    ]
