# Generated by Django 4.2.7 on 2024-11-11 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('categoria', models.CharField(max_length=50)),
                ('color', models.CharField(default='#FFFFFF', max_length=7)),
                ('medicamentos', models.ManyToManyField(related_name='grupos', to='dashboard.producto')),
            ],
        ),
    ]
