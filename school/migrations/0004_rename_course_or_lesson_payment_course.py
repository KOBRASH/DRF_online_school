# Generated by Django 4.0 on 2024-03-06 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0003_alter_subscription_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='payment',
            old_name='course_or_lesson',
            new_name='course',
        ),
    ]