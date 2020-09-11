# Generated by Django 3.0.6 on 2020-05-18 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0011_book_external_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='readinglist',
            name='series',
            field=models.ManyToManyField(related_name='reading_lists', to='library.BookSeries'),
        ),
    ]