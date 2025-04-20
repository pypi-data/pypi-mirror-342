

# gsheets3

Conecte seu projeto Django ao Google Sheets de forma simples e eficiente.

`gsheets3` é um pacote Python que permite sincronizar modelos Django com planilhas do Google Sheets.  
Ideal para quem precisa armazenar ou visualizar dados em tempo real diretamente no Google Sheets, sem complicações.

---

## 🔧 Instalação

```bash
pip install gsheets3
```

---

## 🚀 Como Usar

---



### 1. Configure as credenciais no `settings.py`:

```python
SPERADSHEET_ID = getenv("KEY")

GSHEETS = {
    "service": {
        "private_key": getenv("PRIVATE_KEY"),
        "client_email": getenv("CLIENT_EMAIL"),
        "token_uri": getenv("TOKEN_URI"),
    }
}
```

---

### 2. Inclua a URL no `urls.py` (do projeto principal):

```python
from django.urls import path, include

urlpatterns = [
    path('', include('gsheets3.urls')),
]
```



---

### 3. Primeira utilização
Antes de usar em seus modelos, faça as migrações do gsheets3 e depois acesse a rota:


```
/gsheets/cliente/
```



### 4. Crie seu modelo com o mixin `SheetSyncableMixin`:
# Somente crie um moledo utilizado o mixins.SheetSyncableMixin após ter conseguido êxito acesasndo a rota /gsheets/cliente/ (vai direto para o admin do django. Tenha um superuser criado (py manage.py createsuperuser)) 
```python
from django.db import models
from django.conf import settings
from gsheets3 import mixins

class Exemplo(mixins.SheetSyncableMixin, models.Model):
    spreadsheet_id = settings.GSHEETS.get("KEY")
    sheet_name = 'nome do worksheet'

    data_range = 'A1:Z'
    model_id_field = 'id'
    sheet_id_field = 'Django GUID'
    batch_size = 500
    max_rows = 300
    max_col = 'Z'

    Nome = models.CharField(max_length=255)
    Tom = models.CharField(max_length=50)

    def __str__(self):
        return self.Nome
```


---

## 📦 Pré-requisitos

- [`gspread`](https://pypi.org/project/gspread/)
- [`google-api-python-client`](https://pypi.org/project/google-api-python-client/)

---

## 🔗 Links Úteis

- [Página do PyPI](https://pypi.org/project/django-gsheets/)

---

Desenvolvido para facilitar a integração de dados entre seu backend Django e as planilhas do Google!
Este pacote foi criado a partir do django-sheets 
https://pypi.org/project/django-gsheets/