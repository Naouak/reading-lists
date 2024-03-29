# Generated by Django 4.1.4 on 2022-12-19 18:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0012_readinglist_series'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('linkText', models.TextField(default='')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='source', to='library.book')),
                ('target', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='target', to='library.book')),
            ],
        ),
    ]
