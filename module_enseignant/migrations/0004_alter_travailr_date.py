# Generated by Django 3.2 on 2021-12-14 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module_enseignant', '0003_travailr_is_terminated'),
    ]

    operations = [
        migrations.AlterField(
            model_name='travailr',
            name='date',
            field=models.DateField(blank=True, null=True),
        ),
    ]