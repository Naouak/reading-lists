# Generated by Django 3.0.6 on 2020-05-17 10:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0008_bookreadinghistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookreadinghistory',
            name='book',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='last_read_history', to='library.Book'),
        ),
    ]
