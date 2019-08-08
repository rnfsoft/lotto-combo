from django import forms

from lottocombo.models import LottoCombo

class SearchForm(forms.Form):
    game = forms.ChoiceField(required=True, label="", help_text="Game", initial='M', choices=LottoCombo.GAMES, \
                            widget=forms.Select(attrs={'class':'form-control'}) )
    numbers = forms.CharField(required=False, label="",  help_text="Numbers", \
                            # widget=forms.TextInput(attrs={'class':'form-control','pattern':'((?:\d+[.,;\s]*)+)'}))
                            widget=forms.TextInput(attrs={'placeholder': 'e.g. 10, 18', 'pattern':'(?:[,;.\s]*\d+[,;.\s]*)+', 'oninvalid':"setCustomValidity('Please enter numbers separated by a comma or space')", 'oninput':"setCustomValidity('')", 'class':'form-control'}))
    number = forms.CharField(required=False, label="",  help_text="* Number", \
                            widget=forms.TextInput(attrs={'placeholder': 'e.g. 7', 'pattern':'\d+$', 'oninvalid':"setCustomValidity('Please enter a number')", 'oninput':"setCustomValidity('')", 'class':'form-control'}))
    occurrence = forms.ChoiceField(required=False, label="", help_text="Min # of occurrence", \
                            # initial=10, choices=[(x, x) for x in range(2, 55, 5)], 
                            initial=10, choices=[(2, 2), (5, 5), (10, 10), (15, 15), (20,20), (25, 25)],     
                            widget=forms.Select(attrs={'class':'form-control'}))

