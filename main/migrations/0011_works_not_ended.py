# Generated by Django 5.0 on 2023-12-21 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_works_update_alter_works_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='works',
            name='Not_Ended',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
