from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('single/<int:pk>/', views.single_page_view, name='single_page_view'),
    path('add_review/<int:pk>/', views.add_review, name='add_review'),
    path('health_data_form/', views.health_data_form, name='health_data_form'),
    path('index_data_form/', views.index_data_form, name='index_data_form'),
    path('index_data_results/', views.index_data_results, name='index_data_results'),
]


