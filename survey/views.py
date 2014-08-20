import random

from django.shortcuts import render
from django.views.generic import TemplateView, View

from survey.models import Item, ItemSet, Filler


class IndexView(TemplateView):
    template_name = 'index.html'


class ItemView(View):
    template_name = 'item.html'

    def get(self, request):
        item_set = random.choice(list(ItemSet.objects.all()))
        items = list(Item.objects\
                .filter(item_set=item_set)\
                .select_related('description', 'image'))
        fillers = list(Filler.objects\
                .select_related('description', 'image'))
        all_items = items + fillers
        random.shuffle(all_items)
        first_item = all_items[0]
        return render(request, self.template_name, {
            'item': first_item,
            })



