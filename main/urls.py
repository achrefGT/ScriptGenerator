from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('CreateLLD/', views.create_LLD, name='create_LLD'),
    path('CreateRouter/', views.create_router, name='create_router'),
    path('CreateRadioSite/', views.create_radioSite, name='create_radioSite'),
    path('upload/', views.upload_lld, name='upload_lld'),
    path('success/', views.success_view, name='file_upload_success'), 
    path('download-script/', views.download_script, name='download_script'),
]