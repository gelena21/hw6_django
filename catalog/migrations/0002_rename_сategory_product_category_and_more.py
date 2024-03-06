# Generated by Django 5.0.2 on 2024-03-06 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='сategory',
            new_name='category',
        ),
        migrations.AlterField(
            model_name='category',
            name='category_description',
            field=models.TextField(max_length=200, verbose_name='Описание категории'),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=100, verbose_name='Наименование категории'),
        ),
        migrations.AlterField(
            model_name='product',
            name='description',
            field=models.TextField(max_length=200, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(max_length=100, verbose_name='Наименование'),
        ),
    ]
