# Generated by Django 5.0 on 2023-12-26 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_room_password'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-created', '-updated']},
        ),
    ]
