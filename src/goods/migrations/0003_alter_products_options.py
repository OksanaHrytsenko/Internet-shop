# Generated by Django 4.2.13 on 2024-06-13 00:13

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("goods", "0002_alter_categories_options_alter_categories_name_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="products",
            options={
                "ordering": ("id",),
                "verbose_name": "Продукт",
                "verbose_name_plural": "Продукты",
            },
        ),
    ]
