from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from text_analysis import views

urlpatterns = [
    path('person_infos/<str:text>', views.person_infos, name="person_infos_get"),
    path('all_person_listing', views.person_listing, name="person_listing"),
    path('all_frequency_listing', views.freq_listing, name="freq_listing"),
]
