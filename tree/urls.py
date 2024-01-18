from django.urls import path, include
from .views import *
app_name = 'tree'

urlpatterns = [
    path('', HomePage.as_view(), name='welcome_page'), 
    path('create-node/', CreateParentNode.as_view(), name='create_node'), 
    path('search-node/', SearchNode.as_view(), name='search_node'),   
      
]
