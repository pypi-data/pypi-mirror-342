from django.urls import path
from .views import GetCliente

urlpatterns = [
    # path('gsheets/authorize/', AuthorizeView.as_view(), name='gsheets_authorize'),
    path('gsheets/cliente/', GetCliente.as_view(), name='gsheets_cliente')
]
