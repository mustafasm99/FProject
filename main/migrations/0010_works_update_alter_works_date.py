# Generated by Django 4.2.5 on 2023-11-04 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_teacher_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='works',
            name='update',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='works',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
