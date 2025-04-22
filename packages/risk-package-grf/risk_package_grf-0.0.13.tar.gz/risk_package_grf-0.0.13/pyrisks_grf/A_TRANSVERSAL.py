print('Módulo: TRANSVERSAL\nEste módulo contiene las funciones que son transversales a todos los procesos, así como las rutas más relevantes para el desarrollo de los mismos.')


import gcsfs
import pickle
import pandas as pd

from datetime import datetime, timedelta
from google.cloud import bigquery
from google.auth.transport.requests import Request
from google.oauth2 import service_account

# Requeridos gcsfs, pickle, google-cloud-bigquery, google-oauth2, google-auth-transport-requests

#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
# Sección de Objetos Fijos

project = "gestion-financiera-334002" # Fijado de proyecto
dataset_id = "DataStudio_GRF_Panama" # Fijado de dataset
mastertable = "Tabla_Maestra"

Riesgo_F = 'R'
festivos_dates = {
        "1/01/2025", "6/01/2025", "13/04/2025", "17/04/2025", "18/04/2025", "20/04/2025",
        "1/05/2025", "2/06/2025", "23/06/2025", "30/06/2025", "20/07/2025", "7/08/2025", "18/08/2025",
        "13/10/2025", "3/11/2025", "17/11/2025", "8/12/2025", "25/12/2025", "1/01/2026", "12/01/2026",
        "23/03/2026", "29/03/2026", "2/04/2026", "3/04/2026", "5/04/2026", "1/05/2026", "18/05/2026",
        "8/06/2026", "15/06/2026", "29/06/2026", "20/07/2026", "7/08/2026", "17/08/2026", "12/10/2026",
        "2/11/2026", "16/11/2026", "8/12/2026", "25/12/2026", "1/01/2027", "11/01/2027", "21/03/2027",
        "22/03/2027", "25/03/2027", "26/03/2027", "28/03/2027", "1/05/2027", "10/05/2027", "31/05/2027",
        "7/06/2027", "5/07/2027", "20/07/2027", "7/08/2027", "16/08/2027", "18/10/2027", "1/11/2027",
        "15/11/2027", "8/12/2027", "25/12/2027", "1/01/2028", "10/01/2028", "20/03/2028", "9/04/2028",
        "13/04/2028", "14/04/2028", "16/04/2028", "1/05/2028", "29/05/2028", "19/06/2028", "26/06/2028",
        "3/07/2028", "20/07/2028", "7/08/2028", "21/08/2028", "16/10/2028", "6/11/2028", "13/11/2028",
        "8/12/2028", "25/12/2028", "1/01/2029", "8/01/2029", "19/03/2029", "25/03/2029", "29/03/2029",
        "30/03/2029", "1/04/2029", "1/05/2029", "14/05/2029", "4/06/2029", "11/06/2029", "2/07/2029",
        "20/07/2029", "7/08/2029", "20/08/2029", "15/10/2029", "5/11/2029", "12/11/2029", "8/12/2029",
        "25/12/2029", "1/01/2030", "7/01/2030", "25/03/2030", "14/04/2030", "18/04/2030", "19/04/2030",
        "21/04/2030", "1/05/2030", "3/06/2030", "24/06/2030", "1/07/2030", "20/07/2030", "7/08/2030",
        "19/08/2030", "14/10/2030", "4/11/2030", "11/11/2030", "8/12/2030", "25/12/2030", "1/01/2031",
        "6/01/2031", "24/03/2031", "6/04/2031", "10/04/2031", "11/04/2031", "13/04/2031", "1/05/2031",
        "26/05/2031", "16/06/2031", "23/06/2031", "30/06/2031", "20/07/2031", "7/08/2031", "18/08/2031",
        "13/10/2031", "3/11/2031", "17/11/2031", "8/12/2031", "25/12/2031", "1/01/2032", "12/01/2032",
        "21/03/2032", "22/03/2032", "25/03/2032", "26/03/2032", "28/03/2032", "1/05/2032", "10/05/2032",
        "31/05/2032", "7/06/2032", "5/07/2032", "20/07/2032", "7/08/2032", "16/08/2032", "18/10/2032",
        "1/11/2032", "15/11/2032", "8/12/2032", "25/12/2032", "1/01/2033", "10/01/2033", "21/03/2033",
        "10/04/2033", "14/04/2033", "15/04/2033", "17/04/2033", "1/05/2033", "30/05/2033", "20/06/2033",
        "27/06/2033", "4/07/2033", "20/07/2033", "7/08/2033", "15/08/2033", "17/10/2033", "7/11/2033",
        "14/11/2033", "8/12/2033", "25/12/2033", "1/01/2034", "9/01/2034", "20/03/2034", "2/04/2034",
        "6/04/2034", "7/04/2034", "9/04/2034", "1/05/2034", "22/05/2034", "12/06/2034", "19/06/2034",
        "3/07/2034", "20/07/2034", "7/08/2034", "21/08/2034", "16/10/2034", "6/11/2034", "13/11/2034",
        "8/12/2034", "25/12/2034", "1/01/2035", "8/01/2035", "18/03/2035", "19/03/2035", "22/03/2035",
        "23/03/2035", "25/03/2035", "1/05/2035", "7/05/2035", "28/05/2035", "4/06/2035", "2/07/2035",
        "20/07/2035", "7/08/2035", "20/08/2035", "15/10/2035", "5/11/2035", "12/11/2035", "8/12/2035",
        "25/12/2035", "1/01/2036", "7/01/2036", "24/03/2036", "6/04/2036", "10/04/2036", "11/04/2036",
        "13/04/2036", "1/05/2036", "26/05/2036", "16/06/2036", "23/06/2036", "30/06/2036", "20/07/2036",
        "7/08/2036", "18/08/2036", "3/11/2036", "17/11/2036", "8/12/2036", "25/12/2036"
    }
festivos_dates = pd.to_datetime(list(festivos_dates), dayfirst= True).strftime("%d/%m/%Y")

ideas_querys = {'extraccion':["SELECT * FROM `id_tabla` WHERE FECHA = (SELECT MAX(FECHA) FROM `id_tabla`)",
                              "SELECT DISTINCT FECHAPORTAFOLIO FROM {} WHERE FECHAPORTAFOLIO NOT IN (SELECT FECHAPORTAFOLIO FROM {})"],
                'borrado':["DELETE FROM `id_tabla` WHERE FECHAPORTAFOLIO=TIMESTAMP('2025-04-08 00:00:00')"]
                }
#-----------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------
# Sección de Funciones

# Funcion para correr con cloud_functions
def create_serv(project,path_to_json, service_name, version,
              SCOPES=["https://www.googleapis.com/auth/cloud-platform"]):
  '''Esta función permite hacer el ingreso a la información de BigQuery al crear el client cuando se quiere hacer usando el usuario de
  servicio en caso de correrse el proceso en automático.'''
  creds = None
  fs = gcsfs.GCSFileSystem(project = project)

  with fs.open(f'credenciales_api/{path_to_json}', 'rb') as token:
        creds = pickle.load(token)

  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
  return bigquery.Client(project=project,credentials=creds)
  #return build(service_name, version, credentials=creds)


def charge_serv(where_to_run,project,dataset_id,tables_names):
  '''Esta función devuelve las referencias de las tablas a utilizar basado en su nombre.
  Inputs:
    where_to_run: str, determina el entorno en el que se corre.

    project: str. Nombre del proyecto a buscar en BigQuery.

    dataset_id: str. Nombre del conjunto de datos dentro del proyecto que se quiere usar.

    tables_names: list. Lista que contiene los nombres de las hojas que están dentro del conjunto de datos, que serán llamadas y para las
    que se entregarán referencias al usuario.

  Output:
    client: BigQuery client. Debe ser el client en el que se está trabajando.

    dataset_ref: BigQuery reference. Referencia que contiene la información (referencias) de las tablas dentro del conjunto de datos de interés.

    tables_ref: list. Contiene como entradas BigQuery references asociadas a las tablas que se quieren consultar.
  '''
  key_path = rf"{Riesgo_F}:\CONFIDENCIAL\Informes\Control Límites FICs\Automatizaciones\Herramienta APTs\gestion-financiera-334002-74adb2552cc5.json"
  # Cargue del proyecto de GCS
  if where_to_run == 'cloud_run':
    client = create_serv(project,'gcs_riesgos_2.pickle', 'bigquery', 'v2') # Creación del BigQuery.client
  elif 'local' in where_to_run:
    # Cargar credenciales
    credentials = service_account.Credentials.from_service_account_file(
        key_path,
        scopes = ["https://www.googleapis.com/auth/cloud-platform"],
    )
    client = bigquery.Client(credentials = credentials)
  #elif where_to_run == 'colab':
  #  from google.colab import auth
  #  auth.authenticate_user() # Se solicitan las credenciales para tener acceso a un usuario que tenga permisos en BigQuery
  #  client = bigquery.Client(project) # Creación del BigQuery.client
  dataset_ref = bigquery.DatasetReference(project, dataset_id)
  # Se obtienen las referencias de las Tablas a utilizar
  tables_ref = [dataset_ref.table(k) for k in tables_names]
  return client,dataset_ref,tables_ref

# Revisión de Fechas existentes. Se crea una función que hace multiples querys
def multiple_query(client,query_list):
  '''Esta función permite obtener un listado con las bases de datos obtenidas de un listado de querys que obtienen bases de datos.
  Abstenerse de utilizar querys distintos a estos, pues harán que la lista tenga vacios.
  Inputs:
    client: BigQuery client. Debe ser el client en el que se está trabajando.

    query_list: list. Sus entradas deben ser querys de SQL que carguen tablas, las cuales serán entregadas dentro de otra lista.

  Output:
    list. Contiene como entradas pd.Dataframe, los cuales contienen las tablas cargadas según el listado de querys.'''
  lista = [client.query(q).to_dataframe() for q in query_list]
  return lista

def simple_query_sender(client,query):
   client.query(query)

def upload_table(client,big_query_table_ref,table_to_append,schema):
  '''Esta función permite hacer el append de la table_to_append a la tabla de big query con referencia big_query_table_ref, usando el esquema schema.
  Inputs:
    client: BigQuery client. Debe ser el client en el que se está trabajando.

    big_query_table_ref: BigQuery table reference de la tabla en la que se va a hacer el append. Esta debe estar dentro del client.

    table_to_append: pd.Dataframe que contiene la tabla (que hace match con el esquema a utilizar para realizar el append).

    schema: Listado cuyas entradas son objetos tipo BigQuery.SchemaField. Esquema a utilizar para el cargue de información.
    Debe coincidir con las variables y características de las mismas en la tabla de BigQuery.

  Output:
    No aplica.'''
  # Configuración del cargue
  job_config = bigquery.LoadJobConfig(
              schema = schema,
              write_disposition = 'WRITE_APPEND' # Importante, no queremos sobreescribir.
              )
  # Ejecución del cargue
  job = client.load_table_from_dataframe(table_to_append,big_query_table_ref, job_config = job_config)
  print(job.result())
  

def create_schema(variables_characteristics):
   '''
   Esta función crea un esquema para bigquery a partir de un diccionario con variables y sus características:
   input:
        variables_characteristics: Diccionario que contiene en cada llave (que es un str con el nombre de la variable 
        a crear, i.e. el 'name') y el value de cada llave es un diccionario con las llaves 'type' y 'mode' que tendrán
        dentro estas características. Por ejemplo debe ser:
            {'var1':{'type':'STR','mode':'REQUIRED'},
            'var2':{'type':'BOOL','mode':'NULLABLE'}}
   '''
   if type(variables_characteristics) is dict:
    schema = [bigquery.SchemaField(j,variables_characteristics[j]['type'],
                                   mode = variables_characteristics[j]['mode']) for j in variables_characteristics]
    return schema
   else:
      raise Exception('Introduzca un diccionario.') 

def create_table(client,big_query_table_ref,table_to_append,schema):
   '''
   Esta función toma un pd.DataFrame y lo sube como una nueva tabla en BigQuery. Si la tabla ya existe, la elimina 
   y crea una nueva con la información deseada.
   inputs:
        client: cliente de BigQuery que realizará las modificaciones. Debe tener cuidado en configurarlo con permisos
        de modificación, pues de lo contrario esta función no se ejecutará correctamente. 
        big_query_table_ref: id de la tabla (exista o no). Este define el proyecto y dataset donde la nueva tabla 
        se creará.
        table_to_append: pd.DataFrame que contiene los registros que se subiran a una tabla de BigQuery.
        schema: Esquema de BigQuery que es consistente con las variables y estructura de table_to_append'''
   client.delete_table(big_query_table_ref, not_found_ok=True)  # Pide que la tabla se elimine si ya está creada. De lo contrario no pasa nada y se sigue con el resto del código
   print("Deleted table '{}'.".format(big_query_table_ref))
   table = bigquery.Table(big_query_table_ref) # Se propone la ruta de la tabla
   table = client.create_table(table) # Se crea la tabla
   print(f"Created table: {big_query_table_ref}")
   upload_table(client,big_query_table_ref,table_to_append,schema) # Se carga la información nueva a la tabla. 

# Función para encontrar el día hábil anterior.
def previous_business_day(fecha, festivos_dates=festivos_dates):

    """
    Encuentra el día anterior hábil para Colombia.

    Parámetros: Fecha base en formato 'DD-MM-YYYY' y la lista con los festivos.

    Output: El día hábil anterior en formato 'DD-MM-YY'.
    """
    today = pd.to_datetime(fecha, dayfirst= True)
    previous_day = today - timedelta(days = 1)

    while previous_day.weekday() in (5,6) or previous_day.strftime("%d/%m/%Y") in festivos_dates:
        previous_day -= timedelta(days= 1)

    return previous_day.strftime("%d/%m/%Y")

def fechas_relevantes():
   # Fechas hábiles
    fecha_analisis = datetime.today().strftime("%d/%m/%Y") # Fecha en la que se correrá la macro.
    #fecha_analisis = (datetime.today() - timedelta(days = 1)).strftime("%d/%m/%Y")
    fecha_corte_d = previous_business_day(fecha_analisis, festivos_dates) # Fecha de consolidación de la información.
    fecha_corte_ayer_d = previous_business_day(fecha_corte_d, festivos_dates) # Fecha anterior al día de consolidación.

    # El formato para la lectura de exceles se debe manejar 'YYYY-MM-DD'.
    fecha_analisis = pd.to_datetime(fecha_analisis, dayfirst= True).strftime("%Y-%m-%d")
    fecha_corte = pd.to_datetime(fecha_corte_d, dayfirst= True).strftime("%Y-%m-%d")
    fecha_corte_ayer = pd.to_datetime(fecha_corte_ayer_d, dayfirst= True).strftime("%Y-%m-%d")

    print('Fecha analisis  :',fecha_analisis)
    print('Fecha corte     :',fecha_corte)
    print('Fecha corte ayer:',fecha_corte_ayer)
    diccionario = {'hoy':fecha_analisis,
                   'corte':fecha_corte,
                   'corte_ayer':fecha_corte_ayer}
    return diccionario