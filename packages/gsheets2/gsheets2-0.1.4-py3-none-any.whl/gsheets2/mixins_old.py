from googleapiclient.discovery import build
from django.core.exceptions import ObjectDoesNotExist
from .auth import get_gapi_credentials
from .gsheets2 import SheetPullInterface, SheetPushInterface, SheetFindInterface, SheetSync
import string
import re
import logging

logger = logging.getLogger(__name__)

# ======================================================
from os import getenv
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level=logging.WARNING)
try:
    log = getenv('LOG')
except:
    log = False

exibirlog = True if log == 'True' else False
exibirlog = False 
def lg( texto):
    if exibirlog:
        logging.warning("\n")
        logging.warning("===========================================")
        logging.warning(texto)
        logging.warning("===========================================")
        logging.warning("\n")

# ======================================================

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


class SheetPushableMixin(BaseGoogleSheetMixin):
    """ mixes in functionality to push data from a Django model to a google sheet. """
    @classmethod
    def push_to_sheet(cls):
        interface = SheetPushInterface(
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
            # queryset=cls.get_sheet_queryset()
        )
        
        lg(f'spreadsheet_id = {cls.spreadsheet_id}')
        lg(f'sheet_name = {cls.sheet_name}')
        lg(f'data_range = {cls.data_range}')
        lg(f'model_id_field = {cls.model_id_field}')
        lg(f'sheet_id_field = {cls.sheet_id_field}')
        lg(f'batch_size = {cls.batch_size}')
        lg(f'max_rows = {cls.max_rows}')
        lg(f'max_col = {cls.max_col}')
        lg(f'push_fields = {cls.get_sheet_push_fields()}')
        lg(f'queryset = {cls.get_sheet_queryset()}')
        return interface.upsert_table()

    @classmethod
    def get_sheet_queryset(cls):
        return cls.objects.all()

    @classmethod
    def get_sheet_push_fields(cls):
        return [f.name for f in cls._meta.fields]


    # @classmethod
    # def criar_worksheet(cls, nomes_colunas):
    #     interface = SheetPushInterface(
    #         cls, 
    #         cls.spreadsheet_id, 
    #         sheet_name=cls.sheet_name, 
    #         data_range=cls.data_range,
    #         model_id_field=cls.model_id_field, 
    #         sheet_id_field=cls.sheet_id_field,
    #         batch_size=cls.batch_size, 
    #         max_rows=cls.max_rows, 
    #         max_col=cls.max_col,
    #         push_fields=cls.get_sheet_push_fields(), 
    #         queryset=cls.get_sheet_queryset(),
    #         sheet_headers=nomes_colunas
    #     )
        
    #     lg(f'spreadsheet_id = {cls.spreadsheet_id}')
    #     lg(f'sheet_name = {cls.sheet_name}')
    #     lg(f'data_range = {cls.data_range}')
    #     lg(f'model_id_field = {cls.model_id_field}')
    #     lg(f'sheet_id_field = {cls.sheet_id_field}')
    #     lg(f'batch_size = {cls.batch_size}')
    #     lg(f'max_rows = {cls.max_rows}')
    #     lg(f'max_col = {cls.max_col}')
    #     lg(f'push_fields = {cls.get_sheet_push_fields()}')
    #     lg(f'queryset = {cls.get_sheet_queryset()}')
    #     return interface.Criar_worksheet()




class SheetPullableMixin(BaseGoogleSheetMixin):
    """ mixes in functionality to pull data from a google sheet and use that data to keep model data updated. Notes:
    * won't delete rows that are in the DB but not in the sheet
    * won't delete rows that are in the sheet but not the DB
    * will update existing row values with values from the sheet
    """
    @classmethod
    def pull_sheet(cls):
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

        return interface.pull_sheet()

    @classmethod
    def get_sheet_pull_fields(cls):
        """ get the field names from the sheet which are to be pulled. MUST INCLUDE THE sheet_id_field """
        return 'all'


class SheetSyncableMixin(SheetPushableMixin, SheetPullableMixin):
    """ mixes in ability to 2-way sync data from/to a google sheet """

    _interface = None  # Cache para a instância da interface

    @classmethod
    def get_interface(cls):
        """ Inicializa e retorna a instância da interface, reutilizando se já existir """
        if cls._interface is None:
            # Inicializa a interface apenas uma vez
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
            )
        return cls._interface
    
    @classmethod
    def sync_sheet(cls):
        lg('passou em mixins sync_sheet')
        cls.pull_sheet()
        cls.push_to_sheet()

    @classmethod
    def criar_worksheet(cls):
        interface = cls.get_interface()
        return interface.Criar_worksheet()       


    @classmethod
    def Pesquisar_no_worksheet(cls, tipo, valor):
        """ tipo: linha, coluuna, celula
                  
        """
        interface = cls.get_interface()
        return interface.read_range(tipo, valor)  


    @classmethod
    def Dados(cls):
        interface = cls.get_interface()
        return interface.All_datas()

    @classmethod
    def Up_dados(cls, linha,dados):
        interface = cls.get_interface()
        return interface.up_data(linha,dados)



    @classmethod
    def Enviar_dados(cls):
        lg('passou em mixins sync_sheet')
        cls.push_to_sheet()

    @classmethod
    def baixar_dados(cls):
        lg('passou em mixins sync_sheet')
        cls.pull_sheet()
