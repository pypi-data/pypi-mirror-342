
from .gsheets import SheetPullInterface,SheetFindInterface
from gspread import service_account_from_dict



class BaseGoogleSheetMixin(object):
    """ base mixin for google sheets """
    # ID of a Google Sheets spreadsheet
    spreadsheet_id = None
    # name of the sheet inside the spreadsheet to use
    sheet_name = 'cifrasdjango'
    # range of data in the sheet
    data_range = 'A1:Z'
    # name of the field to use as the ID field for model instances in the sync'd sheet
    model_id_field = 'id'
    # name of the sheet column to use to store the ID of the Django model instance
    sheet_id_field = 'Django GUID'
    # the batch size determines at what point sheet data is written-out to the Google sheet
    batch_size = 500
    # the max rows to support in the sheet
    max_rows = 300
    # max column to support in the sheet
    max_col = 'Z'



class SheetPullableMixin(BaseGoogleSheetMixin):
    """ mixes in functionality to pull data from a google sheet and use that data to keep model data updated. Notes:
    * won't delete rows that are in the DB but not in the sheet
    * won't delete rows that are in the sheet but not the DB
    * will update existing row values with values from the sheet
    """
    @classmethod
    def pull_sheet(cls,sheet_name):
        interface = SheetPullInterface(
            cls, 
            cls.spreadsheet_id, 
            sheet_name=cls.sheet_name, 
            data_range=cls.data_range,
            model_id_field=cls.model_id_field, 
            sheet_id_field=cls.sheet_id_field,
            batch_size=cls.batch_size, 
            max_rows=cls.max_rows, 
            max_col=cls.max_col, 
            pull_fields=cls.get_sheet_pull_fields())

        return interface.pull_sheet(sheet_name)

    @classmethod
    def get_sheet_pull_fields(cls):
        """ get the field names from the sheet which are to be pulled. MUST INCLUDE THE sheet_id_field """
        return 'all'

# class SheetSyncableMixin(SheetPushableMixin, SheetPullableMixin):
class SheetSyncableMixin:
    """ mixes in ability to 2-way sync data from/to a google sheet """

    _interface = None  # Cache para a instância da interface
    _client = None

    # @classmethod
    # def sync_sheet(cls):
    #     cls.pull_sheet()
    #     cls.push_to_sheet()



    @classmethod
    def reset_interface(cls):
        cls._interface = None

    @classmethod
    def _Criar_client(cls):
        from .models import Clienteacesso
        ac = Clienteacesso.objects.order_by('-created_time').first()
        if ac is None:
            raise ValueError('you must authenticate gsheets at /gsheets/cliente/ before usage')

        credenciais_dic = {
            "client_email": ac.client_email,
            "token_uri": ac.token_uri,
            "private_key": ac.private_key,
        }
        cls._client = service_account_from_dict(info = credenciais_dic, scopes = ['https://www.googleapis.com/auth/spreadsheets'])

    

    @classmethod
    def _Get_sheet(cls):
        if cls._client is None:
            cls._Criar_client()
        return cls._client.open_by_key(cls.spreadsheet_id)
    



    @classmethod
    def _Gerar_interface(cls):
        sheet = cls._Get_sheet()
        cls._interface = SheetFindInterface(
            cls,
            cls.spreadsheet_id,
            sheet_name=cls.sheet_name,
            data_range=cls.data_range,
            model_id_field=cls.model_id_field,
            sheet_id_field=cls.sheet_id_field,
            batch_size=cls.batch_size,
            max_rows=cls.max_rows,
            max_col=cls.max_col,
            push_fields=cls.get_sheet_push_fields(),
            queryset=cls.get_sheet_queryset(),
            # credenciais_dic = cls.credenciais_dic,
            sheet = sheet,
        )

        

    @classmethod
    def get_interface(cls):
        """ Inicializa e retorna a instância da interface, reutilizando se já existir """                
        if cls._interface is None:
            cls._Gerar_interface()
        return cls._interface


    


    @classmethod
    def criar_worksheet(cls,nome = None):
        interface = cls.get_interface()
        return interface.Criar_worksheet(nome)       


    @classmethod
    def Pesquisar_no_worksheet(cls, tipo, valor,sheet_name):
        """ tipo: linha, coluuna, celula
                  
        """
        interface = cls.get_interface()
        return interface.read_range(tipo, valor,sheet_name)  


    @classmethod
    def Dados(cls,sheet_name):
        interface = cls.get_interface()
        return interface.All_datas(sheet_name)

    @classmethod
    def Up_dados(cls, linha,dados,sheet_name):
        interface = cls.get_interface()
        interface.up_data(linha,dados,sheet_name)



    @classmethod
    def Enviar_dados(cls, sheet_name):

        # cls.push_to_sheet()
        interface = cls.get_interface()
        interface.upsert_table(sheet_name)
   

    @classmethod
    def baixar_dados(cls):
        sheet = cls._Criar_Credencial()
        cls._interface = SheetPullInterface(
            cls,
            cls.spreadsheet_id,
            sheet_name=cls.sheet_name,
            data_range=cls.data_range,
            model_id_field=cls.model_id_field,
            sheet_id_field=cls.sheet_id_field,
            batch_size=cls.batch_size,
            max_rows=cls.max_rows,
            max_col=cls.max_col,
            push_fields='all',
            queryset=cls.get_sheet_queryset(),
            # credenciais_dic = cls.credenciais_dic,
            sheet = sheet,
        )        
        cls._interfac.pull_sheet()



    @classmethod
    def get_sheet_queryset(cls):
        return cls.objects.all()

    @classmethod
    def get_sheet_push_fields(cls):
        return [f.name for f in cls._meta.fields]    
    
