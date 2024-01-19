# Generated by Django 5.0 on 2024-01-11 02:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecom_app', '0004_cart'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='pid',
            field=models.ForeignKey(db_column='pid', on_delete=django.db.models.deletion.CASCADE, to='ecom_app.product'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='uid',
            field=models.ForeignKey(db_column='uid', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
