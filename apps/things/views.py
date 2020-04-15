from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView

from .models import Thing


class ThingList(ListView):
    model = Thing
    template_name = "things/list.html"
    context_object_name = "things"


class ThingCreate(CreateView):
    model = Thing
    template_name = "things/create.html"
    fields = ['name']
    success_url = reverse_lazy("things:create")


class ThingRetrieve(DetailView):
    model = Thing
    template_name = "things/detail.html"
    context_object_name = "thing"


class ThingUpdate(UpdateView):
    model = Thing
    template_name = "things/update.html"
    context_object_name = "thing"
    success_url = reverse_lazy('things:list')
    fields = ['name']


class ThingDelete(DeleteView):
    model = Thing
    template_name = "things/confirm_delete.html"
    context_object_name = "thing"
    success_url = reverse_lazy('things:list')
