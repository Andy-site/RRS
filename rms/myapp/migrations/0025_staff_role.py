# Generated by Django 5.0.3 on 2024-04-20 09:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0024_order11'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='role',
            field=models.CharField(default='Admin', max_length=100),
        ),
    ]
