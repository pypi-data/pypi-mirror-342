from django.contrib import admin
from .models import Clienteacesso


@admin.register(Clienteacesso)
class AccessCliente(admin.ModelAdmin):
    fields = ('client_email', 'token_uri', 'private_key', 'created_time' )
    readonly_fields = ('client_email',  'created_time')
