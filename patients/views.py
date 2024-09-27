
from django.db.models import F
from django.http import HttpResponseRedirect, request
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from .models import Medication, Prescription

# Create your views here.
decorators = [never_cache, login_required]


@method_decorator(login_required, name='dispatch')
class IndexView(generic.ListView):
    template_name = 'patients/index.html'
    context_object_name = 'prescription_list'

    def get_queryset(self):
        # Will display the prescriptions of the user
        active_user = self.request.user.id
        return Prescription.objects.filter(creation_date__lte=timezone.now(),
                                           user=active_user).order_by('-creation_date')


@method_decorator(login_required, name='dispatch')
class DetailView(generic.DetailView):
    model = Prescription
    template_name = 'patients/detail.html'

    def get_queryset(self):
        # removes un published questions
        return Prescription.objects.order_by("-creation_date")
