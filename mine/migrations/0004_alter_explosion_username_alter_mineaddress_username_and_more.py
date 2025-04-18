# Generated by Django 5.0.7 on 2024-08-31 04:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mine', '0003_remove_minedetail_latitude_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='explosion',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='explos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='mineaddress',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='address', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='emissions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_emissions', models.FloatField(default=0)),
                ('extraction_emissions', models.FloatField(default=0)),
                ('transport_emissions', models.FloatField(default=0)),
                ('pros_emissions', models.FloatField(default=0)),
                ('tool_emissions', models.FloatField(default=0)),
                ('mine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='emissions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
