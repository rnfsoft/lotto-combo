from django.urls import path

from .views import SearchFormView

urlpatterns = [
	path('', SearchFormView.as_view(), name='home'),
]

