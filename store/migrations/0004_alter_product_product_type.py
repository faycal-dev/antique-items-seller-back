# Generated by Django 4.1.1 on 2022-12-26 10:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_type',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.RESTRICT, to='store.producttype'),
        ),
    ]
