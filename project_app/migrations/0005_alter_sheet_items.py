# Generated by Django 4.2.5 on 2023-11-03 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0004_sheet_items'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sheet',
            name='items',
            field=models.ManyToManyField(blank=True, related_name='sheets', to='project_app.item'),
        ),
    ]
