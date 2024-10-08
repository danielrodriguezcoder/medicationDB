# Generated by Django 5.1.1 on 2024-09-22 21:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_prescription_medication_delete_choice_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MedicationName',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medication_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='medication',
            name='medication_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='patients.medicationname'),
        ),
    ]
