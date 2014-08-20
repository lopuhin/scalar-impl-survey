# -*- encoding: utf-8 -*-

import random
import json

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
            'item': serialize_item(first_item),
            'state_json': json.dumps({
                'item_set': item_set.id,
                'n': 0,
                'items': map(serialize_item, all_items)
                }),
            })

    def post(self, request):
        state = json.loads(request.POST['state_json'])
        answer = request.POST.get('answer')
        error = None
        finished = False
        if answer not in ['yes', 'no']:
            error = u'Вы должны ответить Да или Нет'
        else:
            # TODO - save
            state['n'] += 1
            if state['n'] == len(state['items']):
                finished = True
        return render(request, self.template_name, {
            'finished': finished,
            'error': error,
            'item': None if finished else state['items'][state['n']],
            'state_json': json.dumps(state),
            })


def serialize_item(item):
    return {
        'id': item.id,
        'description': item.description.text,
        'image': item.image.name,
        'type': 'filler' if isinstance(item, Filler) else 'item',
        'answer': item.answer if isinstance(item, Filler) else None,
        }

