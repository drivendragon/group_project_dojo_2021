# Generated by Django 2.2 on 2021-06-18 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('solo_app', '0007_auto_20210617_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_testimony',
            field=models.TextField(blank=True),
        ),
    ]