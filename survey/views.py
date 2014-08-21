# -*- encoding: utf-8 -*-

import random
import json
import csv
from StringIO import StringIO
from collections import defaultdict

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView, View

from survey.models import Item, ItemSet, Filler, Participant, ResultItem


class IndexView(TemplateView):
    template_name = 'index.html'


class ItemView(View):
    template_name = 'item.html'

    def get(self, request):
        item_set = random.choice(list(ItemSet.objects.filter(is_active=True)))
        items = list(Item.objects\
                .filter(item_set=item_set)\
                .select_related('description', 'image'))
        fillers = list(Filler.objects\
                .select_related('description', 'image'))
        all_items = items + fillers
        random.shuffle(all_items)
        first_item = all_items[0]
        return render(request, self.template_name, {
            'item': self._serialize_item(first_item),
            'state_json': json.dumps({
                'item_set': item_set.id,
                'n': 0,
                'items': map(self._serialize_item, all_items)
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
            if state.get('participant'):
                participant = Participant.objects.get(pk=state['participant'])
            else:
                participant = Participant.objects.create(
                        item_set=ItemSet.objects.get(pk=state['item_set']))
                state['participant'] = participant.id
            item = state['items'][state['n']]
            ResultItem.objects.create(
                    participant=participant,
                    filler_id=item.get('filler'),
                    item_id=item.get('item'),
                    answer=answer == 'yes',
                    n=state['n'])
            state['n'] += 1
            if state['n'] == len(state['items']):
                finished = True
        return render(request, self.template_name, {
            'finished': finished,
            'error': error,
            'item': None if finished else state['items'][state['n']],
            'state_json': json.dumps(state),
            })

    def _serialize_item(self, item):
        return {
            'id': item.id,
            'description': item.description.text,
            'image': item.image.name,
            'filler': item.id if isinstance(item, Filler) else None,
            'item': item.id if isinstance(item, Item) else None,
            }


class RawResultView(View):
    def get(self, request):
        rows = [[
            'participant',
            'n',
            'item_set',
            'filler_id',
            'filler_image',
            'filler_description',
            'filler_answer',
            'filler_is_correct',
            'item_id',
            'item_image',
            'item_description',
            'answer',
            'dt',
            ]]
        for ri in ResultItem.objects\
                .order_by('participant', 'n')\
                .select_related('participant', 'filler', 'item'):
            row = [
                ri.participant.id,
                ri.n,
                ri.participant.item_set_id,
                ]
            if ri.filler:
                row.extend([
                    ri.filler.id,
                    ri.filler.image.name,
                    ri.filler.description.text,
                    ri.filler.answer,
                    int(ri.filler.answer == ri.answer),
                    ])
            else:
                row.extend([''] * 5)
            if ri.item:
                row.extend([
                    ri.item.id,
                    ri.item.image.name,
                    ri.item.description,
                    ])
            else:
                row.extend([''] * 3)
            row.extend([
                int(ri.answer == 0),
                ri.dt,
                ])
            rows.append([unicode(x).encode('utf-8') for x in row])
        f = StringIO()
        writer = csv.writer(f)
        writer.writerows(rows)
        return HttpResponse(f.getvalue(), mimetype='text/csv')


class ResultView(View):
    template_name = 'result.html'

    def get(self, request):
        filler_correctness = {}
        participants_filler_rating = defaultdict(int)
        item_answers = {}
        per_participant_answers = defaultdict(list)
        for ri in ResultItem.objects.select_related('filler'):
            if ri.filler:
                filler_is_correct = ri.answer == ri.filler.answer
                participants_filler_rating[ri.participant_id] += \
                        not filler_is_correct
                account(filler_correctness, ri.filler, filler_is_correct)
        for ri in ResultItem.objects.select_related('item'):
            if ri.item and participants_filler_rating\
                    .get(ri.participant_id, 100) <= 1:
                account(item_answers, ri.item, ri.answer)
                per_participant_answers[ri.participant_id].append(
                        (ri.item.image.name, ri.answer))
        participants_per_item_tuple = defaultdict(int)
        for answers in per_participant_answers.itervalues():
            if len(answers) == 4:
                answers.sort()
                participants_per_item_tuple[tuple(answers)] += 1
        _sorted = lambda d: [(
                k, y, c, '%.3f' % (1.0 * y / c,))
            for k, (y, c) in sorted(
                d.iteritems(), key=lambda (k, _): unicode(k))]
        filler_hist = defaultdict(int)
        for n_wrong in participants_filler_rating.itervalues():
            filler_hist[n_wrong] += 1
        n_per_participant_items = sum(participants_per_item_tuple.itervalues())
        return render(request, self.template_name, {
            'filler_correctness': _sorted(filler_correctness),
            'item_answers': _sorted(item_answers),
            'filler_hist': sorted(filler_hist.iteritems(),
                key=lambda (n, _): n),
            'participants_per_item_tuple': [(
                u', '.join(u'%s: %d' % (image, a) for image, a in answers),
                n,
                '%.3f' % (1.0 * n / n_per_participant_items,)
                ) for answers, n in sorted(
                    participants_per_item_tuple.iteritems(),
                    key=lambda (k, _): k)],
            })


def account(d, key, answer):
    try:
        yes, count = d[key]
    except KeyError:
        yes, count = d[key] = (0, 0)
    yes += answer
    count += 1
    d[key] = (yes, count)
