# Generated by Django 3.2.2 on 2021-06-16 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_orderupdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='o_json',
            field=models.CharField(default='', max_length=5000),
        ),
    ]
