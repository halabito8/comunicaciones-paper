from django.urls import path

from . import views

urlpatterns = [
    path('dos-rayos', views.dos_rayos.as_view()),
    path('okumura', views.okumura.as_view()),
    path('okumura-hata', views.okumura_hata.as_view()),
]