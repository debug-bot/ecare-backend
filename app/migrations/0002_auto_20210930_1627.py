# Generated by Django 3.2 on 2021-09-30 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='patient',
            old_name='contact',
            new_name='city',
        ),
        migrations.RemoveField(
            model_name='patient',
            name='email',
        ),
        migrations.AddField(
            model_name='patient',
            name='phone',
            field=models.CharField(blank=True, default=None, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patient',
            name='address',
            field=models.CharField(blank=True, default=None, max_length=1000, null=True),
        ),
    ]
