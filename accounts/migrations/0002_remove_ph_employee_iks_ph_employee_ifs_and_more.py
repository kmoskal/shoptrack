# Generated by Django 4.2.4 on 2023-09-10 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ph',
            name='employee_iks',
        ),
        migrations.AddField(
            model_name='ph',
            name='employee_ifs',
            field=models.IntegerField(blank=True, default=None, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ph',
            name='employee_id',
            field=models.CharField(blank=True, max_length=11, unique=True),
        ),
    ]
