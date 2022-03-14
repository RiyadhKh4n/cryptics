from . import views
from django.urls import path

urlpatterns = [
    path('', views.get_portfolio_list, name='get_portfolio_list'),
    path('create', views.create_portfolio, name='create_portfolio_url'),
    path('edit/<portfolio_id>', views.edit_portfolio, name='edit_portfolio'),
]
