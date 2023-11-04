# Generated by Django 4.2.5 on 2023-11-03 21:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('barcode', models.ImageField(upload_to='barcode_images/')),
                ('code', models.CharField(max_length=100)),
                ('quant_bag', models.CharField(blank=True, max_length=100)),
                ('quant_box', models.CharField(blank=True, max_length=100)),
                ('about', models.CharField(blank=True, max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='store',
            name='store_img',
            field=models.ImageField(upload_to='store_images/'),
        ),
        migrations.CreateModel(
            name='Sheet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=50)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('store', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='project_app.store')),
            ],
        ),
    ]
