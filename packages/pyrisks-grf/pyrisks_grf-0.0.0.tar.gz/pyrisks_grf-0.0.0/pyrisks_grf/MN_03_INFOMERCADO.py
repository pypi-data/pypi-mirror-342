print('Módulo Nube: INFOMERCADO\nEste módulo contiene la ejecución del cálculo en GCP de la hoja de INFOMERCADO.')

#-----------------------------------------------------------------
# Librerías

import pandas as pd
from datetime import datetime, timedelta

# Librerías de Gooogle
# Para instalar: pip install google-cloud-bigquery-storage
# Para instalar bidq: pip install google-cloud-bigquery pandas-gbq
from google.cloud import bigquery
from google.oauth2 import service_account

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

# Esta función recibe un dataframe y lo manda a GCP con el modo Append. 
def append_2_GCP(df, project_id, dataset_id, table_id, schema, nombre_fecha_GCP, fecha_corte, fecha_corte_ayer, Riesgo_F, ignorar_cargue_por_fecha_faltante = False):

    
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
            SELECT DISTINCT {nombre_fecha_GCP}
            FROM {table_ref}
            ORDER BY {nombre_fecha_GCP}
                """

        fechas_bq = client.query(query).to_dataframe()
        fechas_bq = fechas_bq[rf"{nombre_fecha_GCP}"].unique()
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

#-----------------------------------------------------------------
# Previos

# Carpeta: Riesgos GB
RGB_F = 'K'
# Carpeta: Riesgo
Riesgo_F = "R"

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

# Diccionario de rankeo de calificaciones crediticias
rating_map = {
    # Investment Grade
    "AAA": 1, "Aaa": 1,            # Best possible rating
    "AA+": 2, "Aa1": 2,
    "AA": 3, "Aa2": 3,
    "AA-": 4, "Aa3": 4,
    "A+": 5, "A1": 5,
    "A": 6, "A2": 6,
    "A-": 7, "A3": 7,
    "BBB+": 8, "Baa1": 8,
    "BBB": 9, "Baa2": 9,
    "BBB-": 10, "Baa3": 10,  # Lowest investment grade

    # Speculative Grade (High Yield)
    "BB+": 11, "Ba1": 11,
    "BB": 12, "Ba2": 12,
    "BB-": 13, "Ba3": 13,
    "B+": 14, "B1": 14,
    "B": 15, "B2": 15,
    "B-": 16, "B3": 16,
    "CCC+": 17, "Caa1": 17,
    "CCC": 18, "Caa2": 18,
    "CCC-": 19, "Caa3": 19,
    "CC": 20, "Ca": 20,
    "C": 21, "C": 21,
    "D": 22, "D": 22,  # Default (worst rating)

    # Short-Term Ratings
    "F1+": 1, "P-1": 1,  # Best short-term rating
    "F1": 2, "P-2": 2,
    "F2": 3, "P-3": 3,
    "F3": 4,
    "B": 5,
    "C": 6,
    "D": 7  # Default for short-term debt
}




def global_treatment_Infomercado_Pan():

    #-----------------------------------------------------------------
    # Calculo de Fechas Relevantes

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
    # Traer Inputs necesarios (Temporal)

    key_path = rf"{Riesgo_F}:\CONFIDENCIAL\Informes\Control Límites FICs\Automatizaciones\Herramienta APTs\gestion-financiera-334002-74adb2552cc5.json"

    # Cargar credenciales
    credentials = service_account.Credentials.from_service_account_file(
        key_path,
        scopes = ["https://www.googleapis.com/auth/cloud-platform"],
    )
    client = bigquery.Client(credentials = credentials)

    # Tabla 1: Portafolio
    project_id = 'gestion-financiera-334002'
    dataset_id = 'DataStudio_GRF_Panama'
    table_id = 'Portafolio_H_Pan'
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    query = f"""
        SELECT*
        FROM {table_ref}
        WHERE DATE(FECHAPORTAFOLIO) = '{fecha_corte}'
        """
    Portafolio = client.query(query).to_dataframe()

    # Tabla 2: VaR
    project_id = 'gestion-financiera-334002'
    dataset_id = 'DataStudio_GRF_Panama'
    table_id = 'VaR_H_Pan'
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    query = f"""
        SELECT*
        FROM {table_ref}
        WHERE DATE(FECHA) = '{fecha_corte}'
        """
    VaR = client.query(query).to_dataframe()

    # Tabla 3: Metricas_H_Pan
    project_id = 'gestion-financiera-334002'
    dataset_id = 'DataStudio_GRF_Panama'
    table_id = 'Metricas_H_Pan'
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    query = f"""
        SELECT*
        FROM {table_ref}
        WHERE DATE(FECHAPORTAFOLIO) = '{fecha_corte}'
        """
    Metricas = client.query(query).to_dataframe()

    # Input 4: Biblia
    project_id = 'gestion-financiera-334002'
    dataset_id = 'DataStudio_GRF'
    table_id = 'Biblia_H'
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    query = f"""
        SELECT FECHA, COMPANIA,  TIPO_LIMITE, LIMITE_NUM, FIJO
        FROM {table_ref}
        WHERE (PRODUCTO = 'CORREDORES PANAMA' AND TIPO_LIMITE = 'LIMITE DE INVERSION PP %  (95%)' AND FIJO = 'CORREDORES PANAMA')
        OR (PRODUCTO = 'CORREDORES PANAMA' AND TIPO_LIMITE = 'PLAZO INVERSION TITULOS' AND FIJO = 'CORREDORES PANAMA')
        """
    Biblia = client.query(query).to_dataframe()

    #-----------------------------------------------------------------
    # Carpintería: Calcular Valores Tabla

    # Consumo Mercado
    # Nominal Porta
    Pos_Max = Portafolio.loc[Portafolio['PORTAFOLIO'] == 'POSICION PROPIA', 'VALORMERCADO'].sum()
    # DV01
    Tot_DV01 = Portafolio.loc[Portafolio['PORTAFOLIO'] == 'POSICION PROPIA', 'DV1'].sum()
    # VaR
    Tot_VaR = VaR.loc[VaR['PORTAFOLIO'] == 'POSICION PROPIA PANAMA', 'VaR_95'].sum()
    # Duración
    Tot_Dur = Metricas.loc[Metricas['PORTAFOLIO'] == 'POSICION PROPIA', 'DURACIONMACAULAY'].iloc[0]

    # Consumo Límites de Inversión
    Pos_PP = pd.DataFrame(Portafolio.loc[Portafolio['PORTAFOLIO'] == 'POSICION PROPIA'].groupby('EMISOR')['VALORMERCADO'].sum()).reset_index(drop=False)
    # Calificación
    worst_rating = Portafolio['CALIF'].loc[Portafolio['CALIF'].map(rating_map).idxmax()]
    # Tipo de Activo
    tipo_activo = Portafolio.loc[Portafolio['PORTAFOLIO'] == 'POSICION PROPIA']['TIPO_ACTIVO']
    consumo_tipo_activo = ", ".join(map(str, set(tipo_activo)))

    # Consumo de Plazo
    # Se debe realizar un promedio ponderado de duraciones 
    Porta_PP = Portafolio[Portafolio['PORTAFOLIO'] == 'POSICION PROPIA']
    # weighted_avg_dur = Porta_PP.groupby('EMISOR').apply(lambda g: (g['DUR_MACA'] * g['VALORMERCADO']).sum() / g['VALORMERCADO'].sum()).reset_index(name = 'DURXEMISOR') # Easier to read but deprecated
    weighted_avg_dur = Porta_PP.groupby('EMISOR').agg(WEIGHTED_AVG = ('DUR_MACA', lambda x: (x * Porta_PP.loc[x.index, 'VALORMERCADO']).sum() / Porta_PP.loc[x.index, 'VALORMERCADO'].sum())).reset_index(drop=False)

    # Límites de Biblia
    # Se encuentran los límites 
    Biblia = Biblia[(Biblia['LIMITE_NUM'] != 0) & (Biblia['FECHA'] == Biblia['FECHA'].max())]

    # Mapeo de Formateo entre Biblia y Portafolio
    porta_map_biblia = {'REPUBLIC OF COLO': 'MINISTERIO DE HACIENDA', 'JPMORGAN CHASE & CO': 'J.P MORGAN CHASE BANK',
                        'SURA ASSET MANAGEMENT': 'GRUPO DE INVERSIONES SURAMERICANA (ANTES SURAMERICANA DE INVERSIONES)',
                        'Banco Davivienda Panama':'DAVIVIENDA PANAMA- FILIAL','Bladex YCD - NY Agency': 'BLADEX S.A. / PANAMA',
                        'BANCOLOMBIA SA':'B. BANCOLOMBIA'}
    biblia_map_porta = {v: k for k,v in porta_map_biblia.items()}
    emisores_biblia = Portafolio.loc[Portafolio['PORTAFOLIO'] == 'POSICION PROPIA', 'EMISOR'].map(porta_map_biblia)
    emisores_porta = emisores_biblia.map(biblia_map_porta)


    # Tabla de Límites Generales
    Tabla_riesgomercado = pd.DataFrame({'VALOR': ['Posición Máxima USD (USD MM)', 'VaR (USD)', 'DV01 Renta Fija (USD)', 'Duración (Años)']})
    limites_generales = pd.Series(['Posición Máxima (USD)','VaR (USD) ','DV01','Duración (Años)'])
    #Tabla_riesgomercado['LIMITE'] = limites_generales.map(Limites_PP.set_index('VALOR')['LIMITE'])


    # Tabla de Límites de Duración
    Tabla_limites_inversion = pd.DataFrame({'VALOR': emisores_porta.unique()})
    Tabla_limites_inversion['LIMITE'] = Tabla_limites_inversion['VALOR'].map(porta_map_biblia).map(Biblia[Biblia['TIPO_LIMITE'] == 'LIMITE DE INVERSION PP %  (95%)'].set_index('COMPANIA')['LIMITE_NUM'])

    # Tabla de Límites de Plazo
    Tabla_limites_plazo = pd.DataFrame({'VALOR': emisores_porta.unique()})
    Tabla_limites_plazo['LIMITE'] = Tabla_limites_plazo['VALOR'].map(porta_map_biblia).map(Biblia[Biblia['TIPO_LIMITE'] == 'PLAZO INVERSION TITULOS'].set_index('COMPANIA')['LIMITE_NUM'])

    # Tablas Finales
    # Tabla 1 Los Límites Principales Generales
    Tabla_riesgomercado['CONSUMO'] = [Pos_Max, Tot_VaR, Tot_DV01, Tot_Dur]
    #Tabla_riesgomercado['CONSUMOPOR'] = Tabla_riesgomercado['CONSUMO']/Tabla_riesgomercado['LIMITE']

    # Tabla 2 Los Límites de Inversión
    Tabla_limites_inversion['CONSUMO'] = Tabla_limites_inversion['VALOR'].map(Pos_PP.set_index('EMISOR')['VALORMERCADO'])/1e6 # MM USD
    Tabla_limites_inversion['CONSUMOPOR'] = Tabla_limites_inversion['CONSUMO']/Tabla_limites_inversion['LIMITE']

    # Se incluye las filas adicionales
    #limite_cal = pd.Series(['Calificación Mínima']).map(Limites_PP.set_index('VALOR')['LIMITE'])[0]
    calificacion_row_df = pd.DataFrame([{'VALOR': 'Calificación Mínima', 'CONSUMO2': worst_rating, 'TABLA': 2.1}])
    #limite_tipo = pd.Series(['Tipo de Activo']).map(Limites_PP.set_index('VALOR')['LIMITE'])[0]
    Tipo_de_activorow_df = pd.DataFrame([{'VALOR': 'Tipo de Activo', 'CONSUMO2': consumo_tipo_activo, 'TABLA': 2.1}])

    Tabla_limites_inversion_str = pd.concat([calificacion_row_df, Tipo_de_activorow_df], ignore_index= True)

    #Tabla 3 Los Límites de Plazo
    Tabla_limites_plazo['CONSUMO'] = Tabla_limites_plazo['VALOR'].map(weighted_avg_dur.set_index('EMISOR')['WEIGHTED_AVG'])
    Tabla_limites_plazo['CONSUMOPOR'] = Tabla_limites_plazo['CONSUMO']/Tabla_limites_plazo['LIMITE']
    # Realizar merge de las tablas para LookerStudio.
    Tabla_riesgomercado['TABLA'] = 1
    Tabla_limites_inversion['TABLA'] = 2
    Tabla_limites_plazo['TABLA'] = 3

    # Looker
    looker_df = pd.concat([Tabla_riesgomercado, Tabla_limites_inversion, Tabla_limites_inversion_str, Tabla_limites_plazo], ignore_index=True)
    looker_df['FECHA'] = fecha_corte
    looker_df['FECHA'] = pd.to_datetime(looker_df['FECHA'], dayfirst= False)

    #-----------------------------------------------------------------
    # Carga a GCP

    # El schema define cada uno de los formatos de las columnas que se carga. Portafolio
    schema_looker = [
        bigquery.SchemaField("VALOR", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("LIMITE", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("CONSUMO", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("CONSUMOPOR", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("TABLA", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("CONSUMO2", "STRING", mode="NULLABLE"),
        bigquery.SchemaField("FECHA", "TIMESTAMP", mode="NULLABLE")
        ]

    append_2_GCP(df = looker_df, project_id = 'gestion-financiera-334002', dataset_id = 'DataStudio_GRF_Panama',
                    table_id = 'Consumos_Pan_PP', schema = schema_looker, nombre_fecha_GCP = 'FECHA', fecha_corte = fecha_corte, 
                    fecha_corte_ayer = fecha_corte_ayer, Riesgo_F = Riesgo_F)

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








