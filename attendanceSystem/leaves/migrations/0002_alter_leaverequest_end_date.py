# Generated by Django 5.1.7 on 2025-03-18 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leaves', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leaverequest',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
