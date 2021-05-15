from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class SankeyView(TemplateView):
    template_name = 'sankey.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['hello'] = 'world'
        return ctx

class MapView(TemplateView):
    template_name = 'map.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        ctx['hello'] = 'world'
        return ctx

