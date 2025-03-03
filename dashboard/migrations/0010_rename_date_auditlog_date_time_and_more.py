# Generated by Django 4.2.7 on 2025-01-17 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0009_entrega_alter_venta_destinatario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='auditlog',
            old_name='date',
            new_name='date_time',
        ),
        migrations.AddField(
            model_name='auditlog',
            name='element_delivered',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='auditlog',
            name='quantity',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='auditlog',
            name='recipient',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
