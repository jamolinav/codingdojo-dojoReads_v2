# Generated by Django 2.2.4 on 2021-05-27 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dojo_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='raiting',
            field=models.IntegerField(default=3),
            preserve_default=False,
        ),
    ]
