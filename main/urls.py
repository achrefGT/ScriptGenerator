from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('CreateLLD/', views.create_LLD, name='create_LLD'),
    path('CreateRouter/', views.create_router, name='create_router'),
    path('CreateRadioSite/', views.create_radioSite, name='create_radioSite'),
]