from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:landmark_id>/', views.detail, name = 'detail'),
    path('<int:landmark_id>/results/', views.results, name = 'results'),
    path('<int:landmark_id>/vote/', views.vote, name = 'vote')
    ]