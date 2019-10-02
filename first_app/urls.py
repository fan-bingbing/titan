from django.urls import path

from . import views

urlpatterns = [
                path('', views.index, name='index'),
                path('fep/', views.fep, name='fep'),
                path('mad/', views.mad, name='mad'),
                path('output/', views.output, name='output'),
                path('acp/', views.acp, name='acp'),
]
