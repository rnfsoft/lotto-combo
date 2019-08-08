import itertools
import operator
import re
from functools import reduce

from django.db import models
from django.db.models import Q


# Create your models here.
class LottoComboQuerySet(models.query.QuerySet):      
    def other_combinations(self, game, numbers, number, occurrence):      
        if numbers and number: 
            numbers = re.findall(r'\d+', numbers)       
            field = '{}__icontains'.format('numbers')
            queryset = [Q(**{field:n}) for n in numbers]
            return self.filter(reduce(operator.or_, queryset, Q(numbers__icontains='00')) | Q(number__icontains=number), game=game, occurrence__gte= occurrence).order_by('-occurrence')  

        elif number:
            return None # Results already displayed in the exact match
        
        else:
            numbers = re.findall(r'\d+', numbers)
            field = '{}__icontains'.format('numbers')      
            queryset = [Q(**{field:n}) for n in numbers]
            return self.filter(reduce(operator.or_, queryset, Q(numbers__icontains='00')), game=game, occurrence__gte= occurrence).order_by('-occurrence')       

class LottoCombo(models.Model):
    GAMES = (
        ('M', 'MEGA Millions®'),
        ('P', 'POWERBALL®'),
    )
    game = models.CharField(max_length=1, choices=GAMES, null=True, blank=True)
    numbers = models.CharField(max_length=20, null=True, blank=True)
    number = models.CharField(max_length=5, null=True, blank=True) 
    occurrence = models.IntegerField(null=True, blank=True)
    count_numbers = models.IntegerField(null=True, blank=True)
    count_numbers_number = models.IntegerField(null=True, blank=True)
  
    def __str__(self):
        return 'game:{} numbers:{} number:{} occurrence:{}'.format(self.game, self.numbers, self.number, self.occurrence)
    
    def save(self, *args, **kwargs):
        self.count_numbers = len(re.findall(r'\d+', self.numbers))
        self.count_numbers_number = len(re.findall(r'\d+', self.numbers + self.number))
        return super(LottoCombo, self).save(*args, **kwargs)

    objects = LottoComboQuerySet.as_manager()

class TaskHistory(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    game = models.CharField(max_length=1, choices=LottoCombo.GAMES, null=True, blank=True)
    count = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return 'date:{} game:{} records:{}'.format(self.updated_at, self.game, self.count)

class SearchHistory(models.Model):
    searched_at = models.DateTimeField(auto_now=True)
    client_ip = models.CharField(max_length=25, null=True, blank=True)
    game = models.CharField(max_length=1, choices=LottoCombo.GAMES, null=True, blank=True)
    numbers = models.CharField(max_length=20, null=True, blank=True)
    number = models.CharField(max_length=5, null=True, blank=True) 

    def __str__(self):
        return 'searched_at:{} client_ip:{} game:{} numbers:{} number:{}'.format(self.searched_at, self.client_ip, self.game, self.numbers, self.number)

