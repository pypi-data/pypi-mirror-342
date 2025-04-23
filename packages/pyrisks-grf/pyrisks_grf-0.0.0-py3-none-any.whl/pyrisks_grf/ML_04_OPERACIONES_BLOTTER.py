print('Módulo Local: Operaciones para Informe Contraparte (Operaciones_Cerradas_H_Blotter y Operac_Abiertas_Blotter)\nEste módulo contiene la ejecución del cálculo local de las Operaciones Abiertas y Cerradas para así subirlo a GCP.')

import pandas as pd
from datetime import datetime, timedelta
from openpyxl import load_workbook
from difflib import get_close_matches, SequenceMatcher
import os
import warnings
from difflib import get_close_matches, SequenceMatcher
import ipywidgets as widgets
from IPython.display import display, clear_output

# Para BigQuery
# pip install google-cloud-bigquery-storage
from google.cloud import bigquery
from google.oauth2 import service_account

# Cartpeta: Riesgos
Riesgo_F = 'R'

# Carpeta: Riesgos GB
RGB_F = 'K'

# Boolean Para Correr Operaciones Contraparte
run_Oper_C = True

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
# Objetos


#-----------------------------------------------------------------
# Funciones

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

# Función para encontrar el día hábil anterior.
def next_business_day(fecha, festivos_dates, days):

    """
    Encuentra el día anterior hábil para Colombia.

    Parámetros: Fecha base en formato 'DD-MM-YYYY' y la lista con los festivos.

    Output: El día hábil anterior en formato 'DD-MM-YY'.
    """
    today = pd.to_datetime(fecha, dayfirst= False)
    next_day = today + timedelta(days = days)

    while next_day.weekday() in (5,6) or next_day.strftime("%Y-%m-%d") in festivos_dates:
        next_day += timedelta(days= 1)

    return next_day.strftime("%Y-%m-%d")


def best_guess(word, possibilities, cutoff=0.0):
    """Returns best match and similarity score."""
    matches = get_close_matches(word, possibilities, n=1, cutoff=cutoff)
    if matches:
        match = matches[0]
        score = SequenceMatcher(None, word, match).ratio()
        return match, score
    else:
        return None, 0.0
def build_guess_df(new_names, valid_names, cutoff=0.6):
    results = []
    for name in new_names:
        guess, score = best_guess(name, valid_names, cutoff=cutoff)
        results.append({
            'original_name': name,
            'suggested_match': guess,
            'similarity_score': round(score, 2)
        })
    return pd.DataFrame(results)

def match_names(df, name_list, name_columns=None):
    """
    Para una serie de nombres, realiza el match del nombre con el original, dado el formato
    del Excel 'Nombres_Contraparte'. Retorna el nombre original, es decir homogeneiza distintos nombres
    para la misma contraparte.

    Parameters:
    - df: pandas DataFrame
    - name_list: list of names to search for
    - name_columns: list of columns to search in (e.g., ['NOMBRE 1', 'NOMBRE 2', ...]).
      If None, it automatically uses columns that start with 'NOMBRE'.

    Returns:
    - List of matched values from 'NOMBRE 1'
    """
    if name_columns is None:
        name_columns = [col for col in df.columns if col.startswith('NOMBRE')]

    result = []

    for name in name_list:
        match = df[df[name_columns].apply(lambda row: name in row.values, axis=1)]
        if not match.empty:
            result.append(match.iloc[0]['NOMBRE 1'])  # First name
        else:
            result.append(None)  

    return result

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


# Esta función recibe un dataframe y lo manda a GCP con el modo Truncate (reemplaza)
def append_2_GCP_truncate(df, project_id, dataset_id, table_id, schema, fecha_corte):

    key_path = rf"{Riesgo_F}:\CONFIDENCIAL\Informes\Control Límites FICs\Automatizaciones\Herramienta APTs\gestion-financiera-334002-74adb2552cc5.json"

    # Cargar credenciales
    credentials = service_account.Credentials.from_service_account_file(
        key_path,
        scopes = ["https://www.googleapis.com/auth/cloud-platform"],
    )
    
    # Inicializamos el client
    client = bigquery.Client(credentials = credentials)

    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    schema = schema

    # Configura la configuración para la carga de datos
    job_config = bigquery.LoadJobConfig(
        schema = schema,
        write_disposition = "WRITE_TRUNCATE",  # Importante, no queremos sobreescribir.
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


# Función para formatear el df antes de realizar su carga a GCP.
def Formateo_df2GCP(df, cols_to_datetime, cols_to_float64, cols_to_string, dayfirst):
    """
    Format specified columns in a DataFrame.

    Parameters:
    df : DataFrame to format
    cols_to_datetime : list of columns to convert to datetime (dayfirst=True)
    cols_to_float64 : list of columns to convert to float64
    cols_to_string : list of columns to convert to string

    Returns:
    The formatted DataFrame.
    """
    if not df.empty:

        if cols_to_datetime:
            df[cols_to_datetime] = df[cols_to_datetime].apply(pd.to_datetime, dayfirst=dayfirst, errors='coerce')

        if cols_to_float64:
            df[cols_to_float64] = df[cols_to_float64].apply(lambda x: pd.to_numeric(x, errors='coerce'))

        if cols_to_string:
            df[cols_to_string] = df[cols_to_string].astype(str)

    return df


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


def global_treatment_Operaciones_Blotter_Pan():
    #-----------------------------------------------------------------
    # Cargar Insumos

    key_path = rf"{Riesgo_F}:\CONFIDENCIAL\Informes\Control Límites FICs\Automatizaciones\Herramienta APTs\gestion-financiera-334002-74adb2552cc5.json"

    # Cargar credenciales
    credentials = service_account.Credentials.from_service_account_file(
        key_path,
        scopes = ["https://www.googleapis.com/auth/cloud-platform"],
    )
    client = bigquery.Client(credentials = credentials)

    # Insumo 1: Operaciones Blotter Abiertas 
    project_id = 'gestion-financiera-334002'
    dataset_id = 'DataStudio_GRF_Panama'
    table_id = 'Operac_Abiertas_Blotter'
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    query = f"""
        SELECT*
        FROM {table_ref}
        """
    Operaciones_Activas_Viejas = client.query(query).to_dataframe()

    # Formatear la fecha de trade_date
    Operaciones_Activas_Viejas['Trade_Date'] = Operaciones_Activas_Viejas['Trade_Date'].dt.tz_localize(None)
    Operaciones_Activas_Viejas['Settlement_Date'] = Operaciones_Activas_Viejas['Settlement_Date'].dt.tz_localize(None)

    # Insumo 2: Nuevas operaciones abiertas
    formato_ruta_operaciones = rf'{RGB_F}:\Privada\Panama\Sistemas de Negociación\POSICION PROPIA\%d-%m-%Y.xlsx'
    path_ruta_operaciones = pd.to_datetime(fecha_corte).strftime(formato_ruta_operaciones)
    nuevas_operaciones = pd.read_excel(path_ruta_operaciones, skiprows= 2)

    # Renombrar las columnas
    # Renombrar columna
    original_names = ['Trade Dt', 'Exec Time (GMT)', 'Qty (M)', 'BrkrName', 'Ord/Inq',
                    'Dlr Alias', 'Brkr', 'Seq#', 'SetDt', 'C/Firm', 
                    'Exec Time', 'SalesFirm', 'SetDt Real', 'Diferencia en días']
    new_names = ['Trade_Date','Execution_Time','Quantity_M','Contraparte_Name','Ord_Inq',
                'Dlr_Alias', 'Contraparte_Code', 'Sec_Number', 'Settlement_Date', 'C_Firm',
                'Exec_Time', 'Sales_Firm', 'Real_Settlement_Date', 'Days_Difference']

    rename_dict = dict(zip(original_names, new_names))
    nuevas_operaciones = nuevas_operaciones.rename(columns=rename_dict)

    # Si la trade date no coincida se debe a que no hubo operaciones en la fecha anterior y se repite el mismo operaciones ya viejo de fecha corte ayer.
    condicion_si_no_hay_nuevasop = (nuevas_operaciones['Trade_Date'] == fecha_corte_ayer).all()
    if condicion_si_no_hay_nuevasop:
        nuevas_operaciones.drop(nuevas_operaciones.index, inplace=True)

    # Insumo 3: Incumplimientos de operaciones abiertas
    formato_ruta_cumplimientos = r"D:\bloomberg10\Downloads\Cuadro Riesgo-Cumplimientos %d.%m.%Y.xlsx"
    #formato_ruta_cumplimientos = r"C:\Users\cadiaard\Documents\Panama\Informe Contraparte\Cuadro Riesgo-Cumplimientos %d.%m.%Y.xlsx"
    ruta_cumplimientos = pd.to_datetime(fecha_corte_d, dayfirst = True).strftime(formato_ruta_cumplimientos)
    operac_incumplimientos = pd.read_excel(ruta_cumplimientos)

    # Renombrar las columas para hacer el merge con operaciones activas
    operac_incumplimientos.rename(columns= {'TRADE DATE':'Trade_Date','PRICE': 'Price', 'NET CASH':'Net'}, inplace=True)
    #operac_incumplimientos['Net'] = operac_incumplimientos['Net'].round(0)    

    print(rf"Total de incumplimientos: {operac_incumplimientos.shape[0]}") 

    # Input 4: Parámetros Nombres
    # Este input se debe a que los nombres de las contrapartes a veces difiere, aunque haga referencia a la misma contraparte.
    code_path = os.getcwd()
    manual_data_folder = rf"{RGB_F}:\Privada\Panama\Informes\Control Contrapartes\Auto_Control_Contraparte\Input"
    manual_data_path = rf"{manual_data_folder}\Nombres_Contraparte.xlsx"
    Nombres_Contrap = pd.read_excel(manual_data_path)


    #-----------------------------------------------------------------
    # Identificar las nuevas operacioes activas y las nuevas cerradas

    if operac_incumplimientos.shape[0] == 0:

        # Si no hay operaciones incumplidas. Entonces simplemente son activas todas con settlement posterior a la fecha de corte.
        New_Operaciones_Activas_Viejas = Operaciones_Activas_Viejas[Operaciones_Activas_Viejas['Settlement_Date'] > fecha_corte]
        # El complemento serán las operaciones que se cerraron.
        Operaciones_Cerradas =  Operaciones_Activas_Viejas[Operaciones_Activas_Viejas['Settlement_Date'] <= fecha_corte]
    else:
        # Se identifican de las operaciones realizadas cuales corresponden a retrasos y por ende siguen activas.
        Retrasos = Operaciones_Activas_Viejas.merge(operac_incumplimientos[['ISIN', 'Trade_Date','Net']], on= ['ISIN', 'Trade_Date','Net'], how='inner')

        if operac_incumplimientos.shape[0] != Retrasos.shape[0]:
            warnings.warn(f"Se encontraron {operac_incumplimientos.shape[0]}incumplimientos en el insumo pero se encontró match con solo {Retrasos.shape[0]} retrasos")

        # Se incluyen aquellas operaciones activas.
        Op_activas_sin_retraso = Operaciones_Activas_Viejas[Operaciones_Activas_Viejas['Settlement_Date'] > fecha_corte]
        New_Operaciones_Activas_Viejas = pd.concat([Op_activas_sin_retraso, Retrasos])

        # Piénselo, no deberian haber duplicates pero por si acaso
        New_Operaciones_Activas_Viejas.drop_duplicates()
        
        # El complemento de lo anterior, corresponde a las operaciones cerradas
        Operaciones_Cerradas = Operaciones_Activas_Viejas[(Operaciones_Activas_Viejas['Settlement_Date'] <= fecha_corte) & (~Operaciones_Activas_Viejas.isin(Retrasos).all(axis=1))].copy()



    #-----------------------------------------------------------------
    # Realizar Merge con las nuevas operaciones

    # Si no hay operaciones nuevas solo se toman las viejas que siguen activas.
    # Si las hay, se incluyen ambas.

    if not condicion_si_no_hay_nuevasop:
        # Únicamente se tienen en cuenta para activas de hoy, aquellas operaciones cuyo status sea aceptado.
        nuevas_operaciones = nuevas_operaciones[nuevas_operaciones['Status'] == 'Accepted']

        # Se incluyen las operaciones raras de hoy en cerradas:
        operaciones_diferentes = nuevas_operaciones[nuevas_operaciones['Status'] != 'Accepted']

        if not operaciones_diferentes.empty:
            Operaciones_Cerradas = pd.concat([Operaciones_Cerradas, operaciones_diferentes])

        # Posteriormente se realiza el merge entre las nuevas y las viejas que siguen activas.
        if not New_Operaciones_Activas_Viejas.empty:

            Operaciones_Activas = pd.concat([New_Operaciones_Activas_Viejas, nuevas_operaciones])
        else:
            Operaciones_Activas = nuevas_operaciones.copy()

    else:
        if not New_Operaciones_Activas_Viejas.empty:

            Operaciones_Activas = New_Operaciones_Activas_Viejas
        else:
            Operaciones_Activas = nuevas_operaciones.copy()

    #-----------------------------------------------------------------
    # Cálculo del Real Settlement Date y Days_Difference por incumplimientos

    if not Operaciones_Activas.empty:

        # Este valor solo se llena con el Excel de incumplimientos, pero se crea por garantizar consistencia entre tablas.
        Operaciones_Activas['Observaciones'] = [''] * len(Operaciones_Activas)
        Operaciones_Activas['Days_Difference'] = (pd.to_datetime(fecha_analisis) - pd.to_datetime(Operaciones_Activas['Settlement_Date'])).dt.days.clip(lower=0)

        # Calculo de Real Settlement Date, piénselo, será la suma de Settlement Date y Days_Difference en el espacio de
        # días hábiles.

        Operaciones_Activas['Real_Settlement_Date'] = Operaciones_Activas.apply(lambda row: next_business_day(row['Settlement_Date'], festivos_dates, row['Days_Difference']), axis=1)

        # Días de tardanza de las operaciones.
        print(rf"Tardanza de días de las operaciones: {Operaciones_Activas['Days_Difference'].tolist()}")

    #-----------------------------------------------------------------
    # Identificar cada una de las contrapartes

    # En el siguiente fragmento se intenta hacer match de los nuevos nombres (si los hay) con los existentes. El usuario puede revisar los match propuestos y aceptar o denegar los mismos.
    # En caso de denegar, se debe modificar manualmente el Archivo de Excel de 'Nombres_Contrapartes'. 

    # Lista nombres simplemente pone en una lista todos los nombres de contrapartes mapeados en el insumo de Parámetros Nombres.
    # Este será la lista de posibilidades con quien realizar match.
    if not Operaciones_Activas.empty:

        lista_nombres = pd.Series(Nombres_Contrap[Nombres_Contrap.columns[Nombres_Contrap.columns.str.contains('NOMBRE')]].values.ravel().tolist())
        lista_nombres.dropna(inplace = True)

        # Luego, verificamos si existen nuevos nombres en Operaciones Abiertas.
        new_names = [x for x in Operaciones_Activas['Sales_Firm'].drop_duplicates().to_list() if x not in lista_nombres.to_list()]
        #new_names = ['BANK OF New YorkM','SCOTIA INC','DAV PANAMA']

    else:
        new_names = []

    if new_names:

        df_matches = build_guess_df(new_names, lista_nombres.to_list(), cutoff=0.4)
        print(df_matches)

    else:
        print("No hay nombres nuevos, se procede a finalizar la ejecución sin problemas")


    if new_names:

        # === 1. Match logic ===
        def best_guess(word, possibilities, cutoff=0.0):
            matches = get_close_matches(word, possibilities, n=1, cutoff=cutoff)
            if matches:
                match = matches[0]
                score = SequenceMatcher(None, word, match).ratio()
                return match, score
            else:
                return None, 0.0

        def build_guess_df(new_names, valid_names, cutoff=0.6):
            results = []
            for name in new_names:
                guess, score = best_guess(name, valid_names, cutoff=cutoff)
                results.append({
                    'original_name': name,
                    'suggested_match': guess,
                    'similarity_score': round(score, 2)
                })
            return pd.DataFrame(results)

        # === 2. Review interface ===
        def review_matches(df_matches):
            output = widgets.Output()
            display(output)

            current_index = [0]
            accepted_rows = []
            rejected_rows = []

            def show_next():
                with output:
                    clear_output(wait=True)

                    if current_index[0] < len(df_matches):
                        row = df_matches.iloc[current_index[0]]
                        print(f"\n🔍 Reviewing match {current_index[0]+1} of {len(df_matches)}")
                        print(f"Original name   : {row['original_name']}")
                        print(f"Suggested match : {row['suggested_match']}")
                        print(f"Similarity score: {row['similarity_score']}")

                        # Buttons
                        yes_button = widgets.Button(description="Yes ✅", button_style="success")
                        no_button = widgets.Button(description="No ❌", button_style="danger")

                        def on_yes_clicked(b):
                            accepted_rows.append(row)
                            current_index[0] += 1
                            show_next()

                        def on_no_clicked(b):
                            rejected_rows.append(row)
                            current_index[0] += 1
                            show_next()

                        yes_button.on_click(on_yes_clicked)
                        no_button.on_click(on_no_clicked)

                        display(widgets.HBox([yes_button, no_button]))
                    else:
                        print("Name matching review complete!")
                        print(f"✅ Accepted: {len(accepted_rows)}")
                        print(f"❌ Rejected: {len(rejected_rows)}")
                        global accepted_df, rejected_df
                        accepted_df = pd.DataFrame(accepted_rows)
                        rejected_df = pd.DataFrame(rejected_rows)

            show_next()

        # === 4. Launch interface ===
        review_matches(df_matches)

    if new_names:
        accepted_df

    if new_names:    
        rejected_df
    if new_names:
        if not accepted_df.empty: 

            for index, row in accepted_df.iterrows():
                
                    nombre_match = row['suggested_match'] # Este es el nombre con el que se hizo match. El verdadero identificador si se quiere.
                    nombre_original = row['original_name'] # Este es el nombre recibido nuevo por el blotter.

                    fila = Nombres_Contrap[Nombres_Contrap.apply(lambda row: row.str.contains(nombre_match).any(), axis = 1)]

                    if fila.isna().sum(axis = 1).all() > 0:
                        columna = Nombres_Contrap.iloc[fila.index[0]].index[Nombres_Contrap.iloc[fila.index[0]].isna()].to_list()[0]
                        Nombres_Contrap.loc[fila.index[0],columna] = nombre_original
                    else:
                        columna = 'NOMBRE ' + str(len(Nombres_Contrap.columns) - 1)
                        Nombres_Contrap.loc[fila.index[0],columna] = nombre_original  
            
            # Guardar ajuste en el Excel nuevamente
            if os.path.exists(manual_data_path): 
            # Load the existing Excel file
                with pd.ExcelWriter(manual_data_path, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                    # Load the workbook
                    workbook = load_workbook(manual_data_path)
                    # Check if the sheet already exists
                    Nombres_Contrap.to_excel(writer, sheet_name='Nombres_Contrap', index = False) 
                    print(f"Sheet 'Nombres_Contrap' has been successfully appended.") 
        else: 
            print(f"Warning: The file '{manual_data_path}' does not exist.")



    #-----------------------------------------------------------------
    # Si hay matches rechazados, se debe volver a correr el código despues de realizar el ajuste manualmente 

    # Solamente si no hay nombres nuevos o si se aceptan todos los nombres nuevos, se permite la homogeneización
    # y carga a GCP.

    if not new_names:
        matches_done = True
    else:
        if rejected_df.shape[0] == 0:
            matches_done = True
        else:
            matches_done = False

    # Se homogeneizan los nombres.

    if matches_done:

        # Homogeneizar los nombres para las operaciones activas.
        nombres_correctos_Ac = match_names(Nombres_Contrap, Operaciones_Activas['Sales_Firm'])
        Operaciones_Activas['Sales_Firm'] = nombres_correctos_Ac
        # Incluir el NIT para luego mapear a la biblia
        Operaciones_Activas['NIT'] = Operaciones_Activas['Sales_Firm'].map(Nombres_Contrap.set_index('NOMBRE 1')['NIT'])

        # Homogeneizar los nombres para las operaciones cerradas.
        nombres_correctos_Ce = match_names(Nombres_Contrap, Operaciones_Cerradas['Sales_Firm'])
        Operaciones_Cerradas['Sales_Firm'] = nombres_correctos_Ce
        Operaciones_Cerradas['NIT'] = Operaciones_Cerradas['Sales_Firm'].map(Nombres_Contrap.set_index('NOMBRE 1')['NIT'])


    #-----------------------------------------------------------------
    # Cargue a GCP

    if matches_done:

        # Formateo de Operaciones Activas a Cargar
        cols_to_datetime = ['Trade_Date','Execution_Time','Settlement_Date','Real_Settlement_Date']
        cols_to_float64 = ['Yield','Quantity_M','Principal','Sec_Number','Net','Days_Difference','NIT']
        cols_to_string = ['Status', 'Side','UserName','Customer','Security','ISIN','Contraparte_Name', 'Ord_Inq',
                        'Platform','App','Dlr_Alias','Contraparte_Code','C_Firm','Sales_Firm','Observaciones', 
                        'Exec_Time','Price']

        if not Operaciones_Activas.empty:
            Operaciones_Activas = Formateo_df2GCP(Operaciones_Activas, cols_to_datetime, cols_to_float64, cols_to_string, dayfirst=False)

        # Formateo de Operaciones Cerradas a Cargar
        cols_to_datetime = ['Trade_Date','Execution_Time','Settlement_Date','Real_Settlement_Date']
        cols_to_float64 = ['Yield','Quantity_M','Principal','Sec_Number','Net','Days_Difference','NIT']
        cols_to_string = ['Status', 'Side','UserName','Customer','Security','ISIN','Contraparte_Name', 'Ord_Inq',
                        'Platform','App','Dlr_Alias','Contraparte_Code','C_Firm','Sales_Firm','Observaciones', 
                        'Exec_Time','Price']

        if not Operaciones_Cerradas.empty:
            Operaciones_Cerradas = Formateo_df2GCP(Operaciones_Cerradas, cols_to_datetime, cols_to_float64, cols_to_string, dayfirst=False)

        schema_operac_contr = [
            bigquery.SchemaField("Status", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("Side", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("UserName", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("Customer", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("Trade_Date", "TIMESTAMP", mode="NULLABLE"),
            bigquery.SchemaField("Execution_Time", "TIMESTAMP", mode="NULLABLE"),
            bigquery.SchemaField("Security", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("Price", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("Yield", "FLOAT64", mode="NULLABLE"),
            bigquery.SchemaField("ISIN", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("Quantity_M", "FLOAT64", mode="NULLABLE"),
            bigquery.SchemaField("Principal", "FLOAT64", mode="NULLABLE"),
            bigquery.SchemaField("Contraparte_Name", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("Ord_Inq", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("Platform", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("App", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("Dlr_Alias", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("Contraparte_Code", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("Sec_Number", "FLOAT64", mode="NULLABLE"),
            bigquery.SchemaField("Net", "FLOAT64", mode="NULLABLE"),
            bigquery.SchemaField("Settlement_Date", "TIMESTAMP", mode="NULLABLE"),
            bigquery.SchemaField("C_Firm", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("Exec_Time", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("Sales_Firm", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("Real_Settlement_Date", "TIMESTAMP", mode="NULLABLE"),
            bigquery.SchemaField("Days_Difference", "FLOAT64", mode="NULLABLE"),
            bigquery.SchemaField("Observaciones", "STRING", mode="NULLABLE"),
            bigquery.SchemaField("NIT", "FLOAT64", mode="NULLABLE")
            ]

        # Create buttons
        run_button = widgets.Button(description="Run Upload to GCP", button_style='success')
        cancel_button = widgets.Button(description="Do NOT Upload", button_style='danger')

        # Output area
        output = widgets.Output()

        # Define upload action
        def on_run_clicked(b):
            with output:
                clear_output()
                print("Running upload code...")
                
                        # Cargue Operaciones Activas
                if not Operaciones_Activas.empty:
                    if run_Oper_C:
                        
                        append_2_GCP_truncate(df = Operaciones_Activas, project_id = 'gestion-financiera-334002', dataset_id = 'DataStudio_GRF_Panama',
                                    table_id = 'Operac_Abiertas_Blotter', schema = schema_operac_contr, fecha_corte = fecha_corte)
                        
                # Cargue Operaciones Cerradas
                if not Operaciones_Cerradas.empty:
                    if run_Oper_C:
                        
                        append_2_GCP(df = Operaciones_Cerradas, project_id = 'gestion-financiera-334002', dataset_id = 'DataStudio_GRF_Panama',
                                    table_id = 'Operac_Cerradas_H_Blotter', schema = schema_operac_contr, fecha_corte = fecha_corte, 
                                    fecha_corte_ayer = fecha_corte_ayer, ignorar_cargue_por_fecha_faltante= True)
                        
        # Define cancel action
        def on_cancel_clicked(b):
            with output:
                clear_output()
                print("No upload will be done.")

        # Link buttons to actions
        run_button.on_click(on_run_clicked)
        cancel_button.on_click(on_cancel_clicked)

        # Display both buttons and the output
        buttons = widgets.HBox([run_button, cancel_button])
        display(buttons, output)

    #-----------------------------------------------------------------
    # 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 



#-----------------------------------------------------------------
# 




