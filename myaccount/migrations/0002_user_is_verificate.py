# Generated by Django 2.2.7 on 2019-12-14 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myaccount', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_verificate',
            field=models.BooleanField(default=False),
        ),
    ]
