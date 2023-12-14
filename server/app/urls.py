from django.contrib import admin
from django.urls import path,include
from .views import *
urlpatterns = [

    path('',base,name='base'),
    path('send',send_data_to_node,name='send_data'),
    path('stats',get_data_node_stats,name='stats_data'),
    path('receive',receive_data_from_node,name='receive_data'),
    path('add_node/', add_node, name='add_node'),
    path('get_nodes/', get_nodes, name='get_nodes'),
    path('remove_node/', remove_node, name='remove_node'),
]
