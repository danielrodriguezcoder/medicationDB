
from django.contrib import admin
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
User = get_user_model()


# Create your models here.
class Prescription(models.Model):
    prescription_text = models.CharField(max_length=100)
    user = models.ForeignKey(User, models.CASCADE, default=1)
    creation_date = models.DateTimeField('date created')
    expiration_date = models.DateTimeField('date expired')

    class Meta:
        ordering = ['-creation_date']

    def __str__(self):
        return self.prescription_text

    @admin.display(
        boolean=True,
        ordering='creation_date',
        description='Valid?'
    )
    def is_valid(self):
        now = timezone.now()
        return now <= self.expiration_date


class MedicationName(models.Model):
    medication_name = models.CharField(max_length=100)

    class Meta:
        ordering = ['medication_name']

    def __str__(self):
        return self.medication_name


class Medication(models.Model):
    chosen_medication = models.ForeignKey(MedicationName, on_delete=models.PROTECT)
    medication_dose = models.CharField(max_length=100, default='None')
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)

    class Meta:
        ordering = ['chosen_medication']

    def __str__(self):
        return self.chosen_medication.medication_name



