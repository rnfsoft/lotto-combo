from django.contrib import admin
from .models import LottoCombo, TaskHistory, SearchHistory

# Register your models here.
admin.site.register(LottoCombo)
admin.site.register(TaskHistory)
admin.site.register(SearchHistory)
