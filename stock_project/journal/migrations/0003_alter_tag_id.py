# Generated by Django 3.2.9 on 2022-01-06 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0002_auto_20220106_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
