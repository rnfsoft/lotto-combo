import itertools
import json
import operator
import os
import re
import time

import requests
from django.conf import settings

from .models import LottoCombo, TaskHistory

from celery import shared_task

def count_occurrence(store, combos):
    for combo in combos:
        try:
            store[combo] += 1
        except :
            store[combo] = 1

def get_winning_numbers(url):
    request = requests.get(url) 
    get_winning_numbers = [(l[9], str(l[10]).zfill(2))  for l in json.loads(request.content.decode('utf-8'))["data"]]
    return get_winning_numbers

def insert_lottocombo(game, store):
    data = (LottoCombo(game=game, numbers=seperate_numbers(str(k))[0], number=seperate_numbers(str(k))[1], occurrence=v, \
                        count_numbers=len(re.findall(r'\d+', seperate_numbers(str(k))[0])), \
                            count_numbers_number=len(re.findall(r'\d+', str(k))) if len(seperate_numbers(str(k))[1]) > 0 else 0) \
                                for k, v in store.items())
    LottoCombo.objects.bulk_create(data)

def insert_taskhistory(game, count):
    TaskHistory.objects.create(game=game, count=count)

def seperate_numbers(numbers):
    numbers = numbers[1:-1].split('),')
    nums = ' '.join(re.findall(r'\d+', numbers[0]))
    num = ' '.join(re.findall(r'\d+', numbers[1])) if len(numbers) > 1 else ''
    return [nums, num]

@shared_task
def update_lottocombo_daily():
    games = {'M': 'https://data.ny.gov/api/views/5xaw-6ayf/rows.json?accessType=DOWNLOAD',
             'P': 'https://data.ny.gov/api/views/d6yy-54nr/rows.json?accessType=DOWNLOAD'}
    LottoCombo.objects.all().delete()
    print('records deleted')
    for game, url in games.items():
        numbers = get_winning_numbers(url) # e.g. [('15 18 25 33 47', '30')]
        store = {}
        combo_all_nums = ((c, n[1]) \
                for n in numbers \
                    for r in range(len(n[0].split(' '))+1) \
                        for c in itertools.combinations(n[0].split(' '), r) if len(c) > 0) # e.g. combo numbers and number [(('15',), '30'), ..., (('15', 18',), '30'), ..., (('15', '18', '25', '33', '47'), '30')]
        count_occurrence(store, combo_all_nums)	
        combo_nums = (c \
                for n in numbers \
                    for r in range(len(n[0].split(' '))+1) \
                        for c in itertools.combinations(n[0].split(' '), r) if len(c) > 0) # e.g. numbers [('15',), ..., ('15', '18'), ..., ('15', '18', '25', '33', '47')] 
        count_occurrence(store, combo_nums)
        insert_lottocombo(game, store)
        print('insert_lottocombo completed')
        insert_taskhistory(game, len(store))
        print('insert_taskhistory completed')
        time.sleep(10)


