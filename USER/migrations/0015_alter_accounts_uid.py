# Generated by Django 4.2.5 on 2023-09-11 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('USER', '0014_alter_accounts_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x0000015F82F16DE0>', max_length=200),
        ),
    ]
