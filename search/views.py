import re
import datetime

from django.views.generic import FormView

from lottocombo.models import LottoCombo, TaskHistory, SearchHistory

from django.db.models.functions import Length

from .forms import SearchForm

# Create your views here.

class SearchFormView(FormView):

    template_name = 'search.html'
    form_class = SearchForm

    def get_initial(self):
        self.initial = super(SearchFormView, self).get_initial()
        self.initial = self.request.GET.dict() #input values game, numbers, number, occcurence
        #self.request.META.get('HTTP_X_FORWARDED_FOR', self.request.META.get('REMOTE_ADDR')).split(',')[-1].strip()
        return self.initial

    def get_context_data(self, **kwagrs):
        context = super(SearchFormView, self).get_context_data(**kwagrs)
        client_ip = self.request.META.get('HTTP_X_FORWARDED_FOR', self.request.META.get('REMOTE_ADDR')).split(',')[-1].strip()
        
        game = self.initial.get('game')
        numbers = self.initial.get('numbers')
        number = self.initial.get('number')
        occurrence = self.initial.get('occurrence')
        context["updated_at"] = TaskHistory.objects.last().updated_at.strftime('%m/%d/%Y')
        if game and (numbers or number):
            numbers = self.sorted_zfill(numbers)        
            number = self.sorted_zfill(number) 

            context["match_all_numbers"] = self.match_all_numbers(game, numbers, number, occurrence)
            context["other_combinations"] = self.other_combinations(game, numbers, number, occurrence)

            SearchHistory.objects.create(client_ip=client_ip, game=game, numbers=numbers, number=number)   
        return context
    
    def sorted_zfill(self, numbers):
        return  ' '.join(sorted(str(n).zfill(2) for n in re.findall(r'\d+', numbers)))

    def match_all_numbers(self, game, numbers, number, occurrence): 
        if numbers and number:
            return LottoCombo.objects.filter(game=game, numbers__iexact=numbers, number__iexact=number, occurrence__gte = occurrence).order_by('-occurrence')
        elif number:
            return LottoCombo.objects.filter(game=game, number__iexact=number, occurrence__gte = occurrence).order_by('-occurrence')    
        else:
            return LottoCombo.objects.filter(game=game, numbers__iexact=numbers, occurrence__gte = occurrence).order_by('-occurrence')
            

    def other_combinations(self, game, numbers, number, occurrence):
        return LottoCombo.objects.other_combinations(game, numbers, number, occurrence=occurrence)

    # def count_numbers(self, game, count):
    #     return [LottoCombo.objects.filter(game=game, count_numbers=i+1).order_by('-occurrence')[:count] for i in range(5)]
    
    # def count_numbers_number(self, game, count):
    #     return [LottoCombo.objects.filter(game=game, count_numbers_number=i+1).exclude(count_numbers__isnull=True).order_by('-occurrence')[:count] for i in range(6)]

