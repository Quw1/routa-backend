# Generated by Django 5.0.3 on 2024-03-20 13:43

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_user_auth_provider'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='personal_token_secret',
            field=models.UUIDField(default=uuid.UUID('26c9ba38-4550-445d-9df8-71f10e4f9656')),
        ),
    ]
