# Generated by Django 4.0.1 on 2023-11-14 03:07

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0002_myfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='file_upload',
            fields=[
                ('ids', models.AutoField(primary_key=True, serialize=False)),
                ('file_name', models.CharField(max_length=255)),
                ('my_file', models.FileField(upload_to='')),
            ],
        ),
        migrations.AlterField(
            model_name='cliente',
            name='telefone',
            field=models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="O número precisa estar neste formato:                         '9999990000'.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Telefone'),
        ),
        migrations.AlterField(
            model_name='myfile',
            name='arq',
            field=models.FileField(upload_to='media'),
        ),
    ]
