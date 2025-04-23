print('Módulo Local: Operaciones para IRL (Operaciones_H_Pan)\nEste módulo contiene la ejecución del cálculo local de las Operaciones del Hist de Pershing para así subirlo a GCP.')

#-----------------------------------------------------------------
# Librerias

import pandas as pd
from datetime import datetime, timedelta
import warnings

# Para BigQuery
# pip install google-cloud-bigquery-storage
from google.cloud import bigquery
from google.oauth2 import service_account

# Carpeta: Riesgos GB
RGB_F = 'K'
# Carpeta: Riesgo
Riesgo_F = 'R'

# Panama es K (Bloomberg)
# Colombia es R (Bloomberg)

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

def global_treatment_Operaciones_H_Pan():
    #-----------------------------------------------------------------
    # OPeraciones para IRL

    run_Oper = True
    # La información se encuentra desagregada por carpetas
    # Necesitamos el siguiente diccionario para definir el directorio.
    if run_Oper:

        month_map = { '01': 'Enero', '02': 'Febrero', '03': 'Marzo',
                    '04': 'Abril', '05': 'Mayo', '06': 'Junio', 
                    '07': 'Julio', '08': 'Agosto', '09': 'Septiembre',
                    '10': 'Octubre', '11': 'Noviembre', '12': 'Diciembre' }

        año_corte_str = str(fecha_corte[0:4])
        mes_corte_str = month_map[str(fecha_corte[5:7])]
        day_corte_str = str(fecha_corte[8:10])

        Operac_day_folder = rf"{RGB_F}:\Privada\Panama\Sistemas de Negociación\PERSHING"
        Operac_file = rf"Operaciones - {mes_corte_str} {day_corte_str}"
        Operac_day_path = rf"{Operac_day_folder}\{año_corte_str}\{mes_corte_str}\{Operac_file}.xlsx"

        # Se leen las información de operaciones del día que viene de Pershing
        warnings.filterwarnings("ignore", message="Workbook contains no default style")
        Operac_day = pd.read_excel(Operac_day_path, skiprows= 7, engine='openpyxl')

        # Se eliminan las dos últimas filas que son vacías
        Operac_day = Operac_day.iloc[:-2]

        # Carpintería
        # Se deben definir en primera instancia los nombres de la columna, pues el archivo no los trae en un formato aceptable.
        nombres_cols_operac = ['Trade_Date', 'Process_Date', 'Account', 'Short_Name', 'Office', 'IP', 'Symbol', 'Product_Type',
                            'Source_of_input', 'Buy_Sell', 'Number_Of_Shares', 'Execution_Price', 'Total_Amount', 'Cusip_Number',
                            'Security_Name',	'Account_Type',	'Commission_Amount', 'Issue_Currency', 'Order_Quantity', 'Principal_Amount',
                            'Trade_Ref', 'Trade_Type', 'Settlement_Date']

        Operac_day.columns = nombres_cols_operac

        # Incluir la fecha por completitud, aunque este archivo se va a reemplazar todos los días
        Operac_day['FECHA'] = fecha_corte

        # Formateo de columnas previo a GCP
        # Formateo para fechas
        Operac_day['Trade_Date'] = pd.to_datetime(Operac_day['Trade_Date'], format='%m/%d/%Y')
        Operac_day['Process_Date'] = pd.to_datetime(Operac_day['Process_Date'], format='%m/%d/%Y')
        Operac_day['Settlement_Date'] = pd.to_datetime(Operac_day['Settlement_Date'], format='%m/%d/%Y')
        Operac_day['FECHA'] =  pd.to_datetime(Operac_day['FECHA'])

        # Formateo de strings
        cols_to_string = ['Account', 'Short_Name', 'Office', 'IP', 'Symbol', 'Product_Type',
                        'Source_of_input', 'Buy_Sell', 'Cusip_Number', 'Security_Name',
                        'Account_Type', 'Issue_Currency', 'Trade_Ref', 'Trade_Type']
        Operac_day[cols_to_string] = Operac_day[cols_to_string].astype(str)

        # Formateo de valores numéricos
        cols_to_float = ['Number_Of_Shares', 'Execution_Price', 'Total_Amount', 'Commission_Amount',
                        'Order_Quantity', 'Principal_Amount']
        Operac_day[cols_to_float] = Operac_day[cols_to_float]

    #-----------------------------------------------------------------
    # Cargue a GCP

    # El schema define cada uno de los formatos de las columnas que se carga. Operaciones
    schema_operac = [
        bigquery.SchemaField("Trade_Date", "TIMESTAMP", mode="NULLABLE"),
        bigquery.SchemaField("Process_Date", "TIMESTAMP", mode="NULLABLE"),
        bigquery.SchemaField("Account", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("Short_Name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("Office", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("IP", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("Symbol", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("Product_Type", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("Source_of_input", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("Buy_Sell", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("Number_Of_Shares", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("Execution_Price", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("Total_Amount", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("Cusip_Number", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("Security_Name", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("Account_Type", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("Commission_Amount", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("Issue_Currency", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("Order_Quantity", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("Principal_Amount", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("Trade_Ref", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("Trade_Type", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("Settlement_Date", "TIMESTAMP", mode="NULLABLE"),
        bigquery.SchemaField("FECHA", "TIMESTAMP", mode="NULLABLE")
        ]



    # Se realiza la carga de información vía TRUNCATE a GCP
    if run_Oper:
        
        append_2_GCP(df = Operac_day, project_id = 'gestion-financiera-334002', dataset_id = 'DataStudio_GRF_Panama',
                    table_id = 'Operaciones_H_Pan', schema = schema_operac, fecha_corte = fecha_corte,
                    fecha_corte_ayer= fecha_corte_ayer, ignorar_cargue_por_fecha_faltante = False)


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



