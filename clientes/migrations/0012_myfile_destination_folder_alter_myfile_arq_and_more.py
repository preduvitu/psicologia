# Generated by Django 4.0.1 on 2023-11-16 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clientes', '0011_myfile2'),
    ]

    operations = [
        migrations.AddField(
            model_name='myfile',
            name='destination_folder',
            field=models.CharField(choices=[('media', 'Media'), ('prontuario', 'Prontuário')], default='media', max_length=20),
        ),
        migrations.AlterField(
            model_name='myfile',
            name='arq',
            field=models.FileField(upload_to='uploads/'),
        ),
        migrations.AlterField(
            model_name='myfile',
            name='title',
            field=models.CharField(max_length=255),
        ),
    ]
