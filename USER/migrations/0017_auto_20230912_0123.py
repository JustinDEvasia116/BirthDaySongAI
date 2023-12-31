# Generated by Django 3.2.21 on 2023-09-11 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('USER', '0016_alter_accounts_uid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounts',
            name='uid',
            field=models.CharField(default='<function uuid4 at 0x00000224D9ACDE40>', max_length=200),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='angry',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='funny',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='generated_lyrics',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='movie',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='petname',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='smile',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='profiles',
            name='sport',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
