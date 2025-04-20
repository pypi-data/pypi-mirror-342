from django.db import models


class Clienteacesso(models.Model):
    client_email = models.CharField(max_length=255)
    token_uri = models.CharField(max_length=255)
    private_key = models.CharField(max_length=255)
    created_time = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.token_uri}'
