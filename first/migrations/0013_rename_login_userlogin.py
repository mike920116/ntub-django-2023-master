# Generated by Django 4.1.7 on 2023-06-01 13:22

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("first", "0012_login"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Login",
            new_name="UserLogin",
        ),
    ]
