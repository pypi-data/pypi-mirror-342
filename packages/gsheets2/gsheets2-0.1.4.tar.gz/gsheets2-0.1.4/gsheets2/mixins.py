# from googleapiclient.discovery import build

# from gsheets2 import SheetPullInterface, SheetPushInterface, SheetFindInterface, SheetSync
import string
import re
import logging


from gsheets2 import decorators
from googleapiclient.errors import HttpError
from django.core.exceptions import ObjectDoesNotExist
# from .signals import sheet_row_processed

# from gspread import  authorize #service_account_from_dict,
# from oauth2client.service_account import ServiceAccountCredentials
import gspread

# from typing import List
# from django.conf import settings

logger = logging.getLogger(__name__)

# ======================================================
from os import getenv
from dotenv import load_dotenv
load_dotenv('/etc/secrets/.env')
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




#=====================================================================


class BaseSheetInterface(object):
    def __init__(self, model_cls, spreadsheet_id, sheet_name=None, data_range=None, model_id_field=None,
                 sheet_id_field=None, batch_size=None, max_rows=None, max_col=None, sheet_headers = None,
                  sheet = None, **kwargs):
        """
        :param model_cls: `models.Model` subclass this interface applies to
        :param spreadsheet_id: `str` ID of a Google Sheets spreadsheet
        :param sheet_name: `str` name of the sheet inside the spreadsheet to use
        :param data_range: `str` range of data in the sheet
        :param model_id_field: `str` name of the field to use as the ID field for model instances in the sync'd sheet
        :param sheet_id_field: `str` name of the sheet column to use to store the ID of the Django model instance
        :param batch_size: `int` the batch size determines at what point sheet data is written-out to the Google sheet
        :param max_rows: `int` the max rows to support in the sheet
        :param max_col: `str` max column to support in the sheet
        """
        self.model_cls = model_cls
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name
        self.data_range = data_range
        self.model_id_field = model_id_field
        self.sheet_id_field = sheet_id_field
        self.batch_size = batch_size
        self.max_rows = max_rows
        self.max_col = max_col

        self._client = None
        self._credentials = None

        self._sheet_data = None
        self._sheet_headers = sheet_headers
        self._sheet = sheet
        self._worksheet = None

    @property
    def sheet_range(self):
        return BaseSheetInterface.get_sheet_range(self.sheet_name, self.data_range)

    @property
    def sheet_range_rows(self):
        """
        :return: `two-tuple`
        """
        row_match = re.search('[A-Z]+(\d+):[A-Z]+(\d*)', self.sheet_range)
        try:
            start, end = row_match.groups()
        except ValueError:
            start, end = row_match.groups()[0], self.max_rows

        if end == '':
            end = self.max_rows

        return int(start), int(end)

    @property
    def sheet_range_cols(self):
        """
        :return: `two-tuple`
        """
        col_match = re.search('([A-Z]+)\d*:([A-Z]+)\d*', self.sheet_range)
        try:
            start, end = col_match.groups()
        except ValueError:
            start, end = col_match.groups()[0], self.max_col

        return start, end



    def get_worksheet(self,sheet_name):
        if self._worksheet is not None:
            return self._worksheet
        
        self._worksheet = self._sheet.worksheet(sheet_name)
        lg(f'sheet_name = {self.sheet_name}')
        return self._worksheet    
    

    def get_credentials(self) -> dict:

        return {
            "type":self._credenciais_dic.get("type"),
            "project_id": self._credenciais_dic.get("project_id"),
            "private_key_id":self._credenciais_dic.get( "private_key_id"),
            "private_key": self._credenciais_dic.get("private_key"),
            "client_email": self._credenciais_dic.get("client_email"),
            "client_id": self._credenciais_dic.get("client_id"),
            "auth_uri": self._credenciais_dic.get("auth_uri"),
            "token_uri": self._credenciais_dic.get("token_uri"),
            "auth_provider_x509_cert_url": self._credenciais_dic.get("auth_provider_x509_cert_url"),
            "client_x509_cert_url": self._credenciais_dic.get("client_x509_cert_url"),
            "universe_domain": self._credenciais_dic.get("universe_domain"),
        }

    def get_sheet_data(self,sheet_name):
        if self._sheet_data is not None:
            return self._sheet_data       
        self.get_worksheet(sheet_name)  
        self._sheet_data = self._worksheet.get(self.data_range)

        self._sheet_headers = self._sheet_data[0]
        # remove the headers from the data
        self._sheet_data = self._sheet_data[1:]
        lg('passou aqui para setar sheet_data')
        lg(f'self._sheet_data = {self._sheet_data}')

    

    @staticmethod
    def convert_col_letter_to_number(col_letter):
        """ converts a column letter - like 'A' - to it's index in the alphabet """
        return string.ascii_lowercase.index(col_letter.lower())

    @staticmethod
    def convert_col_number_to_letter(col_number):
        """ converts a column index - like 1 - to it's alphabetic equivalent (like 'A') """
        return string.ascii_lowercase[col_number].upper()

    @staticmethod
    def get_sheet_range(sheet_name, data_range):
        return '!'.join([sheet_name, data_range])

    def column_index(self, field_name):
        """ given a canonical field name (like 'Name'), get the column index of that field in the sheet. This relies
        on the first row in the sheet having a cell with the name of the given field
        :param field_name: `str`
        :return: `int` index of the column in the sheet storing the given fields' data
        :raises: `ValueError` if the field name doesn't exist in the header row
        """
        # lg(f'got header row {self.sheet_headers}')
        lg(f'{field_name} está em {self._sheet_headers} ?? ')
        return self._sheet_headers.index(str(field_name))

    def existing_row(self, **data):
        """ given the data to be synced to a row, check if it already exists in the sheet and - if it does - return
        its index
        :param data: `dict` of fields/values
        :return: `int` the index of the row containing the ID if it exists, None otherwise
        :raises: `KeyError` if the data doesn't contain the ID field for the model
        :raises: `ValueError` if the columns don't contain the Sheet ID col
        """
        model_id = data[self.model_id_field]
        sheet_id_ix = self.column_index(self.sheet_id_field)

        # look through the sheet ID column for the model ID
        self._sheet_data = self.get_sheet_data()
        for i, r in enumerate(self._sheet_data):
            try:
                if r[sheet_id_ix] == str(model_id):
                    return i
            except IndexError:
                continue

        return None

    @decorators.backoff_on_exception(decorators.expo, HttpError)
    def writeout(self, range, data,sheet_name):
        """ writes the given data to the given range in the spreadsheet (without batching)
        :param range: `str` a range (like 'Sheet1!A2:B3') to write data to
        :param data: `list` of `list` the set of data to write
        """

        self.get_worksheet(sheet_name)

        return self._worksheet.update(data,range)

    @decorators.backoff_on_exception(decorators.expo, HttpError)
    def writeout_batch(self, ranges, data, sheet_name):
        """ writes the given data to the given ranges in the spreadsheet
        :param ranges: `list` of `str` ranges (like 'Sheet1!A2:B3') to write data to
        :param data: `list` of `list` of `list` the set of data to write to the list of ranges
        :raises: `ValueError` if the list of ranges and data don't have the same length
        """

        if len(ranges) != len(data):
            raise ValueError(f'the length of ranges ({len(ranges)} must equal the length of data ({len(data)})')
        self.get_worksheet(sheet_name)
        request_data = zip(ranges, data)
        request_body = [{'range': r, 'values': values} for r, values in request_data]

        return self._worksheet.batch_update(request_body)
    


class SheetFindInterface(BaseSheetInterface):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = kwargs.pop('queryset')
        self.push_fields = kwargs.pop('push_fields', [f.name for f in self.model_cls._meta.fields])

    
    @decorators.backoff_on_exception(decorators.expo, HttpError)
    def read_range(self, tipo, valor,sheet_name):
        """
        Reads data based on the specified type (row, column, cell, or range).
        Adds row numbers and formats column responses as a dictionary.
        :param tipo: `str` specifies the type ('linha', 'coluna', 'celula', 'range')
        :param valor: `str` or `int` specifies the value: row number, column letter, cell (e.g., 'E2'), or range (e.g., 'A1:C5')
        :return: `list` for 'linha' or 'coluna', `str` or `int` for 'celula', `dict` for 'range' or for column-specific data
        :raises: `ValueError` if the type is invalid
        """
        # Define the range based on the type and value
        if tipo == 'linha':
            range_to_read = f'{valor}:{valor}'  # Exemplo: '2:2'
        elif tipo == 'coluna':
            range_to_read = f'{valor}:{valor}'  # Exemplo: 'Sheet1!B:B'
        elif tipo == 'celula':
            range_to_read = f'{valor}'          # Exemplo: 'Sheet1!E2'
        elif tipo == 'range' and isinstance(valor, list):
            # Validação para garantir que todos os elementos da lista são strings
            for item in valor:
                if not isinstance(item, str) or ":" not in item:
                    raise ValueError(f"Invalid range format: {item}")
            range_to_read = valor  # Passe a lista diretamente
        else:
            raise ValueError("Invalid type specified. Must be 'linha', 'coluna', 'celula', or 'range'.")

        try:

            # Retrieve the data from the response
            self.get_worksheet(sheet_name)
            data = self._worksheet.get(range_to_read) if tipo != 'range' else self._worksheet.batch_get(range_to_read)


            # Process the result based on the type
            if tipo == 'linha' or tipo == 'coluna':
                return [item for sublist in data for item in sublist]
            elif tipo == 'celula':
                # Return a single value for a cell
                if len(data) > 0 and len(data[0]) > 0:
                    value = data[0][0]
                    # Return as string or convert to int if applicable
                    return int(value) if value.isdigit() else value
                else:
                    return None  # If the cell is empty
            elif tipo == 'range':
                result = []

                for row in data:
                    if len(row) > 0:  # Verifica se há dados na linha
                       result.append(row[0])  # Adiciona o primeiro valor da linha


                return result

        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            raise

    @decorators.backoff_on_exception(decorators.expo, HttpError)
    def All_datas(self,sheet_name):

        try:
            self.get_worksheet(sheet_name)
            self._sheet_data = self._worksheet.get(self.data_range)

            self._sheet_headers = self._sheet_data[0]
            # remove the headers from the data
            self._sheet_data = self._sheet_data[1:]

            return self._sheet_data

        except HttpError as error:
            logger.error(f"An error occurred: {error}")
            raise

    @decorators.backoff_on_exception(decorators.expo, HttpError)
    def find_word_and_get_row(self, palavra,sheet_name):
        """ Finds a specific word in the spreadsheet and retrieves the corresponding row data
        :param palavra: `str` the word to search for in the spreadsheet
        :return: `list` containing the data of the row where the word was found
        :raises: `ValueError` if the word is not found
        """
        self.get_sheet_data(sheet_name)
        rows = self._sheet_data

        # Search for the word in each row
        for row in rows:
            if palavra in row:  # Check if the word exists in the row
                logger.debug(f'Found word "{palavra}" in row: {row}')
                return row

        # Raise an exception if the word is not found
        raise ValueError(f'Word "{palavra}" not found in the spreadsheet')
    
    @decorators.backoff_on_exception(decorators.expo, HttpError)
    def Criar_worksheet(self, nome):
        """
        Cria uma aba (worksheet) na planilha, insere os cabeçalhos das colunas na primeira linha,
        e verifica se a aba já existe utilizando a biblioteca `gspread`.
        :param sheet_headers: Lista de cabeçalhos para a aba
        """
        nome = self.sheet_name if nome == None else nome
        sheet_headers = self.push_fields[1:]
        # Obter a lista de abas existentes
        spreadsheet = self._sheet  # A planilha já foi aberta anteriormente com self.client.open_by_key
        existing_sheets = spreadsheet.worksheets()
        existing_titles = [sheet.title for sheet in existing_sheets]

        # Verificar se a aba já existe
        if nome not in existing_titles:
            # Cria uma nova aba (worksheet)
 
            new_sheet = spreadsheet.add_worksheet(title=nome, rows=self.max_rows, cols=self.convert_col_letter_to_number(self.max_col))  # Ajuste o tamanho conforme necessário
            print(f"Aba '{nome}' criada com sucesso!")

            # Inserir os nomes das colunas na primeira linha da aba criada
            colunas = [self.sheet_id_field] + sheet_headers  # Adiciona o campo ID às colunas
            lg(f'Colunas: {colunas}')
            new_sheet.insert_row(colunas, index=1)  # Insere os nomes das colunas na primeira linha
            print(f"Os nomes das colunas foram adicionados à aba '{nome}'.")

        else:
            print(f"A aba '{nome}' já existe.")
    
    def up_data(self, linha,data,sheet_name):
        cols_start, cols_end = self.sheet_range_cols
        # rows_start, rows_end = self.sheet_range_rows

        cols_end = self.convert_col_number_to_letter(len(data)-1)

        # writeout_range = BaseSheetInterface.get_sheet_range(
        #     self.sheet_name, f'{cols_start}{linha}:{cols_end}'
        # )
        # print(f'writeout_range {writeout_range}')
        self.writeout_batch([f'{cols_start}{linha}:{cols_end}'], [[data]],sheet_name)

        lg('FINISHED WITH TABLE UPSERT')

    def upsert_table(self,sheet_name):
        """ upserts objects of this instance type to Sheets """
        queryset = self.queryset
        last_writeout = 0
        cols_start, cols_end = self.sheet_range_cols
        rows_start, rows_end = self.sheet_range_rows
        # lg(f'self._sheet_data = {self._sheet_data}')
        self.get_sheet_data(sheet_name)
        for i, obj in enumerate(queryset):
            if i > 0 and i % self.batch_size == 0:
                # p('obj', obj)
                # p('self.batch_size', self.batch_size)
                writeout_range_start_row = (rows_start + 1) + i
                writeout_range_end_row = writeout_range_start_row + self.batch_size

                writeout_data_start_row = (rows_start - 1) + i
                writeout_data_end_row = writeout_data_start_row + self.batch_size
                writeout_data = self._sheet_data[writeout_data_start_row:writeout_data_end_row]


                self.writeout_batch([f'{cols_start}{writeout_range_start_row}:{cols_end}{writeout_range_end_row}'], [writeout_data],sheet_name)
                last_writeout = i

            push_data = {f: getattr(obj, f) for f in self.push_fields}
            lg(f'push_data = {push_data} -  obj = {obj} ')
            self.upsert_sheet_data(**push_data)

        # writeout any remaining data
        if last_writeout < len(queryset):

            self.writeout_batch([f'{cols_start}{max(2, last_writeout)}:{cols_end}{rows_end}'], [self._sheet_data[last_writeout:]],sheet_name)

        lg('FINISHED WITH TABLE UPSERT')

    def upsert_sheet_data(self, **data):
        """ upserts the data, given as a dict of field/values, to the sheet. If the data already exists, replaces
        its previous value
        :param data: `dict` of field/value
        """
        field_indexes = []
        # lg(f'self.model_id_field = {self.model_id_field}')
        # lg(f'self.sheet_id_field = {self.sheet_id_field}')
        for field in data.keys():
            lg(f'campo = {field}')
            try:
                field_indexes.append((field, self.column_index(field if field != self.model_id_field else self.sheet_id_field)))
            except ValueError:
                lg(f'skipping field {field} because it has no header')
        # p('data.keys()', data.keys())
        # order the field indexes by their col index
        sorted_field_indexes = sorted(field_indexes, key=lambda x: x[1])

        row_data = []
        for field, ix in sorted_field_indexes:
            logger.debug(f'writing data in field {field} to col ix {ix}')
            row_data.append(data[field])

        # get the row to update if it exists, otherwise we will add a new row
        existing_row_ix = self.existing_row(**data)
        if existing_row_ix is not None:
            self._sheet_data[existing_row_ix] = row_data
        else:
            self._sheet_data.append(row_data)


class SheetPullInterface(BaseSheetInterface):
    """ functionality to pull data from a google sheet and use that data to keep model data updated. Notes:
    * won't delete rows that are in the DB but not in the sheet
    * won't delete rows that are in the sheet but not the DB
    * will update existing row values with values from the sheet
    """
    def __init__(self, *args, **kwargs):
        # super(SheetPullInterface, self).__init__(*args, **kwargs)
        super().__init__(*args, **kwargs)
        self.pull_fields = kwargs.pop('pull_fields', 'all')

    def pull_sheet(self,sheet_name):
        sheet_fields = self.pull_fields
        rows_start, rows_end = self.sheet_range_rows
        field_indexes = {self.column_index(f): f for f in self.sheet_headers if f in sheet_fields or sheet_fields == 'all'}
        instances = []
        writeout_batch = []
        self.get_sheet_data(sheet_name)
        # lg(f'field_indexes = {field_indexes}')
        # lg(f'self.sheet_data = {self.sheet_data}')
        for row_ix, row in enumerate(self._sheet_data):
            if len(writeout_batch) >= self.batch_size:
                logger.debug('writing out a batch of instance IDs')
                self.writeout_created_instance_ids(writeout_batch)
                writeout_batch = []

            row_data = {}

            for col_ix in range(len(row)):
                if col_ix in field_indexes:
                    field = field_indexes[col_ix]
                    value = row[col_ix]

                    row_data[field] = value

            cleaned_row_data = getattr(self.model_cls, 'clean_row_data')(row_data) if hasattr(self.model_cls, 'clean_row_data') else row_data

            # give the model the ability to prevent a row from running through upsert
            if hasattr(self.model_cls, 'should_upsert_row') and not getattr(self.model_cls, 'should_upsert_row')(cleaned_row_data):
                logger.debug(f'model prevented upsert of row {row_ix}')
                continue

            instance, created = self.upsert_model_data(row_ix, **cleaned_row_data)

            instances.append(instance)
            if created:
                writeout_batch.append((instance, rows_start + row_ix + 1)) # + 1 to not count header

        if len(writeout_batch) > 0:
            logger.debug(f'writing out remaining {len(writeout_batch)} instance IDs')
            self.writeout_created_instance_ids(writeout_batch)

        return instances

    def upsert_model_data(self, row_ix, **data):
        """ takes a dict of field/value information from the sheet and inserts or updates a model instance
        with that data
        :param row_ix: `int` index of the row which is being upserted into a model instance
        :param data: `dict`
        """
        model_fields = {f.name for f in self.model_cls._meta.get_fields()}
        # cleaned data
        cleaned_data = {
            field: getattr(self.model_cls, f'clean_{field}_data')(value) if hasattr(self.model_cls, f'clean_{field}_data') else value
            for field, value in data.items() if field != self.sheet_id_field and field in model_fields
        }

        try:
            row_id = data[self.sheet_id_field]

            model_filter = {
                self.model_id_field: row_id
            }
            instance, created = self.model_cls.objects.get(**model_filter), False
        except (KeyError, ObjectDoesNotExist, ValueError):
            logger.debug(f'creating new model instance')
            # if there's no ID field in the row or the ID doesnt exist
            instance, created = self.model_cls.objects.create(**cleaned_data), True

        if not created:
            logger.debug(f'updating instance {instance} with data')
            [setattr(instance, field, value) for field, value in cleaned_data.items() if field != self.model_id_field]
            instance.save()

        sheet_row_processed.send(sender=self.model_cls, instance=instance, created=created, row_data=data)

        return instance, created

    def writeout_created_instance_ids(self, created_instances, sheet_name):
        cols_start, cols_end = self.sheet_range_cols
        start_row = created_instances[0][1]

        # find the column letter where the sheet ID lives
        sheet_id_ix = self.column_index(self.sheet_id_field)
        sheet_id_col_ix = BaseSheetInterface.convert_col_letter_to_number(cols_start) + sheet_id_ix
        sheet_id_col_name = BaseSheetInterface.convert_col_number_to_letter(sheet_id_col_ix)

        writeout_ranges = []
        writeout_data = []
        last_writeout_ix = 0
        # we segment the created instances into contiguous blocks of rows for the batch update
        for i in range(len(created_instances)):
            instance, row_ix = created_instances[i]
            last_row_ix = created_instances[i - 1][1] if i > 0 else row_ix

            # if we're at the end of a block of rows or on the last row, it delineates a writeout block
            if row_ix > last_row_ix + 1:
                writeout_ranges.append(BaseSheetInterface.get_sheet_range(
                    self.sheet_name,
                    f'{sheet_id_col_name}{start_row}:{sheet_id_col_name}{last_row_ix}'
                ))
                writeout_data.append(
                    [[str(getattr(instance, self.model_id_field))] for instance, noop in created_instances[last_writeout_ix:i]]
                )

                start_row = row_ix
                last_writeout_ix = i
            elif i == len(created_instances) - 1:
                writeout_ranges.append(BaseSheetInterface.get_sheet_range(
                    self.sheet_name,
                    f'{sheet_id_col_name}{start_row}:{sheet_id_col_name}{row_ix}'
                ))
                writeout_data.append(
                    [[str(getattr(instance, self.model_id_field))] for instance, noop in created_instances[last_writeout_ix:]]
                )

        logger.debug(f'writing out {writeout_ranges} data ranges')
        return self.writeout_batch(writeout_ranges, writeout_data,sheet_name)



#=====================================================================






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
            queryset=cls.get_sheet_queryset()
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


# class SheetSyncableMixin(SheetPushableMixin):
class SheetSyncableMixin:
    """ mixes in ability to 2-way sync data from/to a google sheet """

    _interface = None  # Cache para a instância da interface
    _client = None

    @classmethod
    def reset_interface(cls):
        cls._interface = None

    @classmethod
    def _Criar_client(cls):
        cls._client = gspread.service_account_from_dict(info = cls.credenciais_dic, scopes = ['https://www.googleapis.com/auth/spreadsheets'])

    

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
        # lg('gerar interface')
        # lg(f'sheet_name = {cls.sheet_name}')
        

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
    def Up_dados(cls, linha,dados):
        interface = cls.get_interface()
        interface.up_data(linha,dados)



    @classmethod
    def Enviar_dados(cls, sheet_name):
        lg('passou em mixins sync_sheet')
        # cls.push_to_sheet()
        interface = cls.get_interface()
        interface.upsert_table()
   

    @classmethod
    def baixar_dados(cls):
        lg('passou em mixins sync_sheet')
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


    # @classmethod
    # def sync_sheet(cls):
    #     lg('passou em mixins sync_sheet')
    #     cls.pull_sheet()
    #     cls.push_to_sheet()

    @classmethod
    def get_sheet_queryset(cls):
        return cls.objects.all()

    @classmethod
    def get_sheet_push_fields(cls):
        return [f.name for f in cls._meta.fields]    
    
