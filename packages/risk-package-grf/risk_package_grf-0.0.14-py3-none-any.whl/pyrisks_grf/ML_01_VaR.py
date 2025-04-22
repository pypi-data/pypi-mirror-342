print('Módulo Local: VaR\nEste módulo contiene la ejecución del cálculo local del VaR para así subirlo a GCP.')

#-----------------------------------------------------------------
# Librerias

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
#from openpyxl import load_workbook
#from difflib import get_close_matches, SequenceMatcher
#import os
#import warnings
#from difflib import get_close_matches, SequenceMatcher
#import ipywidgets as widgets
#from IPython.display import display, clear_output

# Para BigQuery
# pip install google-cloud-bigquery-storage
from google.cloud import bigquery
from google.oauth2 import service_account

Riesgo_F = 'R'

# Función para encontrar el día hábil anterior.
def previous_business_day(fecha, festivos_dates):

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

# Los valores con 0 son portafolios inactivos, con lo cual no se desea incluir la información a GCP.
# También se elimina la segunda columna que no tiene información alguna 
def format_VaR_excel(df, var_conf):

    df.replace(0, np.nan, inplace= True)
    df.drop(df.columns[1], axis = 1, inplace = True)

    # Formateo de las fechas
    df.iloc[0,1:]
    dates = pd.to_datetime(df.columns[1:])
    df.columns = [df.columns[0]] + dates.strftime("%Y-%m-%d").tolist()

    # Carpintería
    VaR_df= df.melt(id_vars=df.columns[0], var_name="FECHA", value_name= var_conf)
    VaR_df = VaR_df.dropna().reset_index(drop= True)

    # Formateo
    VaR_df.rename(columns={VaR_df.columns[0]: "PORTAFOLIO"}, inplace= True)
    VaR_df['PORTAFOLIO'] = VaR_df['PORTAFOLIO'].astype(str)
    VaR_df['FECHA'] = pd.to_datetime(VaR_df['FECHA'])
    VaR_df[var_conf] = VaR_df[var_conf].astype(float)

    return(VaR_df)

# Esta función recibe un dataframe y lo manda a GCP con el modo Append. 
def append_2_GCP(df, project_id, dataset_id, table_id, schema, fecha_corte, fecha_corte_ayer, ignorar_cargue_por_fecha_faltante = False):

    
    key_path = rf"{Riesgo_F}:\CONFIDENCIAL\Informes\Control Límites FICs\Automatizaciones\Herramienta APTs\gestion-financiera-334002-74adb2552cc5.json"

    # Cargar credenciales
    credentials = service_account.Credentials.from_service_account_file(
        key_path,
        scopes = ["https://www.googleapis.com/auth/cloud-platform"],
    )
    
    # Inicializamos el client
    client = bigquery.Client(credentials = credentials)

    table_ref = f"{project_id}.{dataset_id}.{table_id}"


    if ignorar_cargue_por_fecha_faltante == False:
            # Extraemos todas las fechas de BQ
        query = f"""
            SELECT DISTINCT FECHA
            FROM {table_ref}
            ORDER BY FECHA
                """

        fechas_bq = client.query(query).to_dataframe()
        fechas_bq = fechas_bq["FECHA"].unique()
        fechas_bq = [i.date() for i in fechas_bq]
        fechas_bq = pd.Series(fechas_bq).dropna().tolist()
        
        last_updated_date = max(fechas_bq)
        shouldbe_last_updated_date = datetime.strptime(fecha_corte_ayer, "%Y-%m-%d").date()
        fecha_a_cargar_hoy = datetime.strptime(fecha_corte, "%Y-%m-%d").date()

        if last_updated_date == shouldbe_last_updated_date:
            print("La última fecha cargada antecede de forma correcta a la que se cargará, se procede a incluir la información")

            schema = schema

            # Configura la configuración para la carga de datos
            job_config = bigquery.LoadJobConfig(
                schema = schema,
                write_disposition = "WRITE_APPEND",  # Importante, no queremos sobreescribir.
            )


            df.columns = df.columns.str.replace('á|é|í|ó|ú|Á|É|Í|Ó|Ú', '__', regex=True)
            df.columns = df.columns.str.replace(' ', '_', regex=True)

            # Carga el DataFrame a BigQuery
            job = client.load_table_from_dataframe(
                df, table_ref, job_config = job_config
            )

            # Espera a que la carga termine
            print(job.result())
            print(f"Carga Exitosa para la fecha: {fecha_corte}")

        elif last_updated_date == fecha_a_cargar_hoy:
            raise Warning(f"Está intentando incluir dos veces la información del: {last_updated_date}")

        else:
            raise Warning(f"La fecha que antecede ({last_updated_date})a la que desea cargar no coincide, debe revisar.")
    
    else:
        schema = schema

        # Configura la configuración para la carga de datos
        job_config = bigquery.LoadJobConfig(
            schema = schema,
            write_disposition = "WRITE_APPEND",  # Importante, no queremos sobreescribir.
        )


        df.columns = df.columns.str.replace('á|é|í|ó|ú|Á|É|Í|Ó|Ú', '__', regex=True)
        df.columns = df.columns.str.replace(' ', '_', regex=True)

        # Carga el DataFrame a BigQuery
        job = client.load_table_from_dataframe(
            df, table_ref, job_config = job_config
        )

        # Espera a que la carga termine
        print(job.result())
        print(f"Carga Exitosa para la fecha: {fecha_corte}")


def global_treatment_VaR_Pan():
    #-----------------------------------------------------------------
    # Nombre de los Folder

    # Carpeta: Riesgos GB
    RGB_F = 'K'
    # Carpeta: Riesgo
    Riesgo_F = 'R'
    # Boolean Para Correr VaR
    run_VaR = True
    # Boolean Para Correr Operaciones
    run_Oper = True
    # Boolean Para Correr Operaciones Contraparte
    run_Oper_C = True

    #-----------------------------------------------------------------
    # Festivos

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

    #-----------------------------------------------------------------
    # Fechas relevantes

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

    #-----------------------------------------------------------------
    # Path

    VaR_folder = rf"{RGB_F}:\Privada\Panama\Planos Integrados Panamá"
    VaR_path = rf"{VaR_folder}\VaR Histórico.xlsx"

    # Se leen las dos hojas de VaR, al 95 y al 99.
    VaR95_excel = pd.read_excel(VaR_path, sheet_name="VaR EWMA (95%)", skiprows= 1)
    VaR99_excel = pd.read_excel(VaR_path, sheet_name="VaR EWMA (99%)", skiprows= 1)

    #-----------------------------------------------------------------
    # Carpinteria

    if run_VaR:

        VaR95 = format_VaR_excel(VaR95_excel, var_conf= "VaR_95")
        VaR99 = format_VaR_excel(VaR99_excel, var_conf= "VaR_99")
        VaR = VaR95.merge(VaR99[['PORTAFOLIO', 'FECHA', 'VaR_99']], on=['PORTAFOLIO', 'FECHA'], how='left')

        # Filtrar únicamente para la fecha de corte
        #VaR_carga = VaR[VaR['FECHA'] == fecha_corte].copy()
        VaR_carga = VaR.copy()
        
        manual_data_folder = rf"{RGB_F}:\Privada\Panama\Planos Integrados Panamá\Automatización Plano Panamá\Auto_Plano_Panama\Input"
        manual_data_path = rf"{manual_data_folder}\Input_Manual.xlsx"

        Porta_df = pd.read_excel(manual_data_path, sheet_name="Input", usecols=list(range(5)), skiprows= 1, dtype={'NUMERO':str})
        Porta_df = Porta_df.dropna(how = "all")

        VaR_carga['PERFIL'] = VaR_carga['PORTAFOLIO'].map(Porta_df.drop_duplicates(subset= 'PORTAFOLIO').set_index('PORTAFOLIO')['PERFIL'])
        VaR_carga = VaR_carga[VaR_carga['PORTAFOLIO'] != 'TOTAL ADPT']

    #-----------------------------------------------------------------
    # Revisar antes de cargar

    print(rf"El VaR que se cargará tiene el siguiente shape: {VaR_carga.shape}")

    # El schema define cada uno de los formatos de las columnas que se carga. Portafolio
    schema_Var = [
        bigquery.SchemaField("PORTAFOLIO", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("FECHA", "TIMESTAMP", mode="REQUIRED"),
        bigquery.SchemaField("VaR_95", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("VaR_99", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("PERFIL", "STRING", mode="NULLABLE")
        ]

    # Se realiza la carga de información vía APPEND a GCP
    if run_VaR:
        
        append_2_GCP(df = VaR_carga, project_id = 'gestion-financiera-334002', dataset_id = 'DataStudio_GRF_Panama',
                    table_id = 'VaR_H_Pan', schema = schema_Var, fecha_corte = fecha_corte, 
                    fecha_corte_ayer = fecha_corte_ayer)
        
        print("Fin de corrida del VaR")


#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



