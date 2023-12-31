# Generated by Django 4.2.2 on 2023-10-02 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('whatsappbot', '0013_remove_contato_timestamp_remove_endereco_cep_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=30)),
                ('whatsapp', models.CharField(max_length=15, unique=True)),
                ('status_conversa', models.TextField()),
                ('endereco', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='whatsappbot.endereco')),
            ],
        ),
        migrations.DeleteModel(
            name='Contato',
        ),
    ]
