# Generated by Django 5.1.6 on 2025-06-05 09:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20250605_0609'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['-created_at']},
        ),
    ]
