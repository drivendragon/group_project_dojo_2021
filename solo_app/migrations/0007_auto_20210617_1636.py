# Generated by Django 2.2 on 2021-06-17 16:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('solo_app', '0006_delete_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wall_message',
            old_name='group_id',
            new_name='group',
        ),
    ]