# Generated by Django 5.0 on 2023-12-21 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_works_not_ended'),
    ]

    operations = [
        migrations.AddField(
            model_name='works',
            name='ERORR',
            field=models.BooleanField(default=False),
        ),
    ]
