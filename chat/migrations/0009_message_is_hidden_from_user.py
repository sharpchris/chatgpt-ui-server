# Generated by Django 4.1.7 on 2023-11-27 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_message_message_type_message_user_embeddingdocument_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='is_hidden_from_user',
            field=models.BooleanField(default=False),
        ),
    ]