# Generated by Django 3.0.8 on 2020-07-15 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20200713_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('OK', 'Konto aktywne'), ('WEBBLK', 'Brak aktywacji email'), ('BLOCK', 'Zbanowane')], default='WEBBLK', max_length=8, verbose_name='Status'),
        ),
    ]
