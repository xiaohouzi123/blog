# Generated by Django 2.0 on 2018-01-17 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20180116_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='cilck',
            field=models.IntegerField(default=0),
        ),
    ]
