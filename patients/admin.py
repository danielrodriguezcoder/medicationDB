from django.contrib import admin

from .models import Prescription, Medication, MedicationName


# Register your models here.
class MedicationInline(admin.TabularInline):
    model = Medication
    extra = 3


class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ('prescription_text', 'user', 'creation_date', "is_valid")
    list_filter = ['creation_date']
    search_fields = ['question_text']

    fieldsets = [
        (None, {'fields': ['prescription_text', 'user']}),
        ("Date information", {'fields': ['creation_date', 'expiration_date']}),
    ]
    inlines = [MedicationInline]


admin.site.register(Prescription, PrescriptionAdmin)
admin.site.register(MedicationName)

