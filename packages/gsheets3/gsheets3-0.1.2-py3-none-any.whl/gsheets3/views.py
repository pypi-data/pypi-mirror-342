from django.shortcuts import HttpResponse, redirect
from django.urls import reverse



from django.views.generic import TemplateView
from gspread import service_account_from_dict
from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings
from .models import Clienteacesso

class GetCliente(TemplateView):
    def get(self, request, *args, **kwargs):


        credenciais_dic = settings.GSHEETS.get('service')

        # Store credentials in the session.
        try:
            client = service_account_from_dict(info = credenciais_dic, scopes = ['https://www.googleapis.com/auth/spreadsheets'])
        except Exception as e:
            return HttpResponse(f'Erro ao criar cliente: {e}')

        try:
            ac = Clienteacesso.objects.get(client_email=credenciais_dic.get('client_email'))
        except ObjectDoesNotExist:
            
            ac = Clienteacesso.objects.create(
                client_email = credenciais_dic.get('client_email'),
                token_uri = credenciais_dic.get('token_uri'),
                private_key = credenciais_dic.get('private_key'),
            )
                

        # logger.debug(f'access credential {ac} init')

        # redirect to admin page for the AC
        return redirect(reverse('admin:gsheets3_clienteacesso_change', args=(ac.id,)))
        # return redirect('/')
    