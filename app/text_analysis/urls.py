from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from text_analysis import views

urlpatterns = [
    path('person_infos/<str:text>', views.person_infos, name="person_infos_get"),
]
