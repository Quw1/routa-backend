# Generated by Django 5.0.3 on 2024-03-29 16:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_user_personal_token_secret'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='personal_token_secret',
            field=models.CharField(default='d6fe76a4-a3e1-48d8-8327-020f20ce2888', max_length=36),
        ),
    ]
