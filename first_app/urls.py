from django.urls import path

from . import views

urlpatterns = [
                path('', views.index, name='index'),
                path('fep/', views.fep, name='fep'),
                path('mad/', views.mad, name='mad'),
                path('output/', views.output, name='output'),
                path('acp/', views.acp, name='acp'),
                path('cs/', views.cs, name='cs'),
                path('csh/', views.csh, name='csh'),
                path('sen/', views.sen, name='sen'),
                path('acs/', views.acs, name='acs'),
                path('blk/', views.blk, name='blk'),
                path('sr/', views.sr, name='sr'),
]
