# Generated by Django 4.2.2 on 2023-10-02 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('whatsappbot', '0018_remove_contato_endereco_cliente_endereco_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contato',
            name='timestamp_msg',
            field=models.BigIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='endereco',
            name='cep',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
