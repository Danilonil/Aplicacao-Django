# Generated by Django 4.2.2 on 2023-10-01 04:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whatsappbot', '0004_cliente_status_conversa'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='timestamp',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
    ]
