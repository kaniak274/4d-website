# Generated by Django 3.0.8 on 2020-07-12 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('login', models.CharField(max_length=30, unique=True, verbose_name='Login / username')),
                ('password', models.CharField(max_length=45, verbose_name='Password')),
                ('email', models.EmailField(max_length=64, unique=True, verbose_name='E-mail')),
                ('social_id', models.CharField(max_length=7, verbose_name='Kod usunięcia postaci')),
                ('powod', models.TextField(blank=True, null=True, verbose_name='Powód banu')),
                ('banlength', models.CharField(blank=True, choices=[('SECOND', 'SECOND'), ('MINUTE', 'MINUTE'), ('HOUR', 'HOUR'), ('DAY', 'DAY'), ('WEEK', 'WEEK'), ('MONTH', 'MONTH'), ('YEAR', 'YEAR'), ('PERM', 'PERM')], max_length=30, null=True, verbose_name='Długość banu')),
                ('coins', models.IntegerField(default=0, verbose_name='SM')),
                ('admin', models.BooleanField(default=False, verbose_name='Admin?')),
            ],
            options={
                'db_table': 'account',
            },
        ),
    ]
