# Generated by Django 4.1 on 2023-05-03 14:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("caim_base", "0029_fostererprofile_is_complete_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="zip_code",
            field=models.CharField(blank=True, max_length=10, verbose_name="ZIP code"),
        ),
    ]
