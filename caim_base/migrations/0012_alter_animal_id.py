# Generated by Django 4.1 on 2022-09-16 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("caim_base", "0011_awg_is_exact_location_shown"),
    ]

    operations = [
        migrations.AlterField(
            model_name="animal",
            name="id",
            field=models.AutoField(
                primary_key=True, serialize=False, verbose_name="CAIM ID"
            ),
        ),
    ]
