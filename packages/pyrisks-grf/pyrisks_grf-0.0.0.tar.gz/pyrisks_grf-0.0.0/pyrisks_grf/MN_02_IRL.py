print('Módulo Nube: IRL\nEste módulo contiene la ejecución del cálculo en GCP de la hoja de IRL.')

#---------------------------------------------------------
# Librerías

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
# Para BigQuery
# pip install google-cloud-bigquery-storage
from google.cloud import bigquery #storage
from google.oauth2 import service_account


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

def global_treatment_IRL_Pan():
    #---------------------------------------------------------
    # Inputs Manuales: Haircuts, Bandas y Pr de Impago de Terceros

    # Definición de Haircuts
    tipo_Haircut = ['HC normal', 'HC Moderado', 'HC Severo', 'HC Severo Macroeconómico']
    activos_rows = ['Dólar', 'Acciones', 'Deuda Privada']

    inputH = [
        [0.07, 0.07, 0.07, 0.07],
        [0.15, 0.15, 0.15, 0.15],
        [0.04, 0.04, 0.04, 0.04]
    ]

    Haircuts = pd.DataFrame(inputH, index=activos_rows, columns=tipo_Haircut)
    Haircuts;

    # Definición de días de las bandas
    cols_rangod = ['Desde', 'Hasta']
    numb_rows = ['Banda 1', 'Banda 2', 'Banda 3']

    inputBandas = [
        [1, 3],
        [1, 7],
        [1, 30]
    ]

    Bandas = pd.DataFrame(inputBandas, index=numb_rows, columns=cols_rangod)
    Bandas;

    # Definición de probabilidad de impago de terceros
    cols_escenarios = ['Normal', 'Moderado', 'Severo', 'Severo Macroeconómico']
    P_row = ['Pr']
    input_prob_impago_terceros = [[0.0401451612903226, 0.0533192071086808, 0.0871878211716342, 0.0971878211716342]]

    Prob_Impago_Ter = pd.DataFrame(input_prob_impago_terceros, index=P_row, columns=cols_escenarios)
    Prob_Impago_Ter;

    #---------------------------------------------------------
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

    #---------------------------------------------------------
    # Fechas Relevantes

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

    #---------------------------------------------------------
    # Lectura de Inputs (Temporal)

    # Provisional Garantía Pershing
    gar_Pershing = 299980

    key_path = rf"{Riesgo_F}:\CONFIDENCIAL\Informes\Control Límites FICs\Automatizaciones\Herramienta APTs\gestion-financiera-334002-74adb2552cc5.json"

    # Cargar credenciales
    credentials = service_account.Credentials.from_service_account_file(
        key_path,
        scopes = ["https://www.googleapis.com/auth/cloud-platform"],
    )
    client = bigquery.Client(credentials = credentials)

    # Tabla 1: Operaciones_Pan
    project_id = 'gestion-financiera-334002'
    dataset_id = 'DataStudio_GRF_Panama'
    table_id = 'Operaciones_H_Pan'
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    query = f"""
        SELECT*
        FROM {table_ref}
        WHERE DATE(Settlement_Date) > '{fecha_corte}'
        """
    Operaciones = client.query(query).to_dataframe()

    # Tabla 2: Portafolio
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

    # Tabla 3: Liquidez
    project_id = 'gestion-financiera-334002'
    dataset_id = 'DataStudio_GRF_Panama'
    table_id = 'Liquidez_H_Pan'
    table_ref = f"{project_id}.{dataset_id}.{table_id}"

    query = f"""
        SELECT PORTAFOLIO, NOMINAL_ACTUAL
        FROM {table_ref}
        WHERE DATE(FECHAPORTAFOLIO) = '{fecha_corte}'
        """
    Liquidez = client.query(query).to_dataframe()

    #---------------------------------------------------------
    # Contabilización de ALAC


    # Escenario Normal y Moderado van de la mano.
    # La única diferencia con los Escenarios Severo y Severo Macroneconómico es que 
    # a los segundos se les suma las garantías de Pershing.

    # Se diseña Moderado y posteriormente se agrega la diferencia.
    bandas_columns = ['Banda 1', 'Banda 2', 'Banda 3']
    activos_rows = ['Liquidez', 'Portafolio', 'Acciones']
    ALAC_M = pd.DataFrame(index=activos_rows, columns=bandas_columns)


    ALAC_dicc = {}
    suffixes = ['Normal', 'Moderado', 'Severo', 'Severo Macroeconómico']
    gar_Pershing_escenarios = [gar_Pershing, gar_Pershing, 0, 0]
    Haircuts_escenarios = ['HC normal', 'HC Moderado', 'HC Severo', 'HC Severo Macroeconómico']

    conteo = 0

    for escenario in suffixes:

        gar_Pershing_es = gar_Pershing_escenarios[conteo]
        Haircut_es = Haircuts_escenarios[conteo]

        bandas_columns = ['Banda 1', 'Banda 2', 'Banda 3']
        activos_rows = ['Liquidez', 'Portafolio', 'Acciones']
        ALAC = pd.DataFrame(index=activos_rows, columns=bandas_columns)

        ALAC.loc['Liquidez'] = Liquidez.loc[Liquidez['PORTAFOLIO'] == 'POSICION PROPIA', 'NOMINAL_ACTUAL'].sum() - gar_Pershing_es
        ALAC.loc['Portafolio'] = Portafolio[(Portafolio['PORTAFOLIO'] == 'POSICION PROPIA') &
                                            (Portafolio['CLASIFICACION2'] != 'ACCIONES') & 
                                            (Portafolio['IF_TRADE'] == 1)]['VALORMERCADO'].sum() * (1 - Haircuts.at['Deuda Privada', Haircut_es])
        ALAC.loc['Acciones'] = Portafolio[(Portafolio['PORTAFOLIO'] == 'POSICION PROPIA') &
                                            (Portafolio['CLASIFICACION2'] == 'ACCIONES') & 
                                            (Portafolio['IF_TRADE'] == 1)]['VALORMERCADO'].sum() * (1  - Haircuts.at['Acciones', Haircut_es])
        
        ALAC.loc['Total'] = ALAC.sum()

        ALAC_dicc[f'ALAC_{escenario}'] = ALAC

        conteo += 1

    ALAC_dicc['ALAC_Moderado']

    #---------------------------------------------------------
    # Salidas de efectivo netas totales

    # Necesitamos realizar el cálculo de nuevas columnas en operaciones.
    # Valoración final para cada título en operaciones
    renta_f_cond = Operaciones['Product_Type'] == "FIXED INCOME"
    Operaciones['VALOR_FINAL'] = (Operaciones['Number_Of_Shares'] * Operaciones['Execution_Price'])/(100 * renta_f_cond +~ renta_f_cond)

    # Días para la definición de bandas
    Operaciones['Trade_Date'] = pd.to_datetime(Operaciones['Trade_Date'])
    Operaciones['Settlement_Date'] = pd.to_datetime(Operaciones['Settlement_Date']) 
    Operaciones['Days'] = (pd.to_datetime(Operaciones['Settlement_Date'].dt.date) - pd.to_datetime(fecha_corte)).dt.days

    # Definición de banda a partir de días
    conditions_d = [
        (Operaciones['Days'] >= (Bandas.at['Banda 1', 'Desde'])) & (Operaciones['Days'] <= Bandas.at['Banda 1', 'Hasta']),
        (Operaciones['Days'] >= Bandas.at['Banda 2', 'Desde']) & (Operaciones['Days'] <= Bandas.at['Banda 2', 'Hasta']),
        (Operaciones['Days'] >= Bandas.at['Banda 3', 'Desde']) & (Operaciones['Days'] <= Bandas.at['Banda 3', 'Hasta'])
    ]
    bandas_nom = [1,2,3]

    Operaciones['Banda'] = np.select(conditions_d, bandas_nom, default=np.nan).astype(int)

    # Se crea la columna de portafolio para diferenciar posición propia de Terceros.
    Operaciones['PORTAFOLIO'] = np.where(Operaciones['Short_Name'] == "CORREDORES", "POSICION PROPIA", "TERCEROS")

    #---------------------------------------------------------
    # Salidas de efectivo: Posicion propia y terceros

    # Calculamos las entradas y salidas de efectivo.
    Req_PPyTer_dicc = {}
    suffixes = ['Normal', 'Moderado', 'Severo', 'Severo Macroeconómico']
    bandas_columns = ['Banda 1', 'Banda 2', 'Banda 3']
    activos_rows = ['Venta_in', 'Compra_in', 'Venta_out','Compra_out','Terceros']
    bandas_nom_py = [1,2,3]
    bandas_to_check = []
    conteo = 0

    # Iteración sobre los escenarios
    for escenario in suffixes:

        Haircut_es = Haircuts_escenarios[conteo]
        bandas_to_check = []
        Req_PPyTer = pd.DataFrame(index=activos_rows, columns=bandas_columns)

        # Dentro de cada escenario se itera
        for banda_i in bandas_nom_py: 

            bandas_to_check.append(banda_i)

            # Plata que me entra por vender un título.
            Req_PPyTer.iloc[Req_PPyTer.index.get_loc('Venta_in'), banda_i - 1] = Operaciones[(Operaciones['PORTAFOLIO'] == 'POSICION PROPIA') &
                                                                                    (Operaciones['Banda'].isin(bandas_to_check)) & 
                                                                                    (Operaciones['Buy_Sell'] == 'SELL')]['Total_Amount'].abs().sum()
            
            # Compra_in - Compra_out calcula la diferencia entre lo que vale en t-1 el título y lo que pague. Lo que
            # me entra de título se pondera por haircut.
            Req_PPyTer.iloc[Req_PPyTer.index.get_loc('Compra_in'), banda_i - 1] = Operaciones[(Operaciones['PORTAFOLIO'] == 'POSICION PROPIA') &
                                                                                    (Operaciones['Banda'].isin(bandas_to_check)) & 
                                                                                    (Operaciones['Buy_Sell'] == 'BUY')]['VALOR_FINAL'].abs().sum() * (1 - Haircuts.at['Dólar', Haircut_es])

            # Paralelamente, Venta_in - Venta_out, corresponde a lo que lo que le vendí menos lo que vale hoy.
            # No hay ponderación porque lo que me entra es efectivo líquido.
            
            Req_PPyTer.iloc[Req_PPyTer.index.get_loc('Venta_out'), banda_i - 1] = Operaciones[(Operaciones['PORTAFOLIO'] == 'POSICION PROPIA') &
                                                                        (Operaciones['Banda'].isin(bandas_to_check)) & 
                                                                        (Operaciones['Buy_Sell'] == 'SELL')]['VALOR_FINAL'].abs().sum()
            # Plata que sale por compra de un título.
            
            Req_PPyTer.iloc[Req_PPyTer.index.get_loc('Compra_out'), banda_i - 1] = Operaciones[(Operaciones['PORTAFOLIO'] == 'POSICION PROPIA') &
                                                                                    (Operaciones['Banda'].isin(bandas_to_check)) & 
                                                                                    (Operaciones['Buy_Sell'] == 'BUY')]['Total_Amount'].abs().sum() 
            # Cálculo para terceros
            Req_PPyTer.iloc[Req_PPyTer.index.get_loc('Terceros'), banda_i - 1] = Operaciones[(Operaciones['PORTAFOLIO'] == 'TERCEROS') &
                                                                                    (Operaciones['Banda'].isin(bandas_to_check))]['VALOR_FINAL'].abs().sum() * Prob_Impago_Ter[escenario].values[0]
        # Sumamos entradas - salidas.
        Req_PPyTer.loc['Total_PP'] = (Req_PPyTer.loc['Venta_out'] + Req_PPyTer.loc['Compra_out']) - (Req_PPyTer.loc['Venta_in'] + Req_PPyTer.loc['Compra_in'])
            
        # Si lo anterior es mayor a cero, entonces el requerimiento es cero y caso contrario el requirimiento es el valor.
        Req_PPyTer.loc['Final_PP'] = np.where(Req_PPyTer.loc['Total_PP'] < 0, 0, Req_PPyTer.loc['Total_PP'])


        Req_PPyTer_dicc[f'Req_{escenario}'] = Req_PPyTer
        
        conteo += 1

    Req_PPyTer_dicc['Req_Moderado']
    Req_PPyTer_dicc['Req_Severo Macroeconómico']

    #---------------------------------------------------------
    # Calculo de IRL e IRL%

    cols_IRL = bandas_columns
    rows_IRL = ['ALAC', 'REQ_PP','REQ_TERCEROS','IRL_absoluto','IRL_relativo']
    df_IRL_dicc = {}

    for escenario in suffixes:

        df_IRL = pd.DataFrame(0.1, index  = rows_IRL, columns= cols_IRL)

        for banda_i in bandas_columns: 
        
            Req_PPyTer = Req_PPyTer_dicc[f'Req_{escenario}']
            
            df_IRL.loc['ALAC', banda_i]  = ALAC_dicc[f'ALAC_{escenario}'].loc['Total', banda_i] # ALAC.
            df_IRL.at['REQ_PP', banda_i] = Req_PPyTer.at['Final_PP', banda_i] # Requerimientos de posición propia
            df_IRL.at['REQ_TERCEROS', banda_i]  = Req_PPyTer.at['Terceros', banda_i] # Requerimiento de Terceros

            # IRL Absoluto
            df_IRL.at['IRL_absoluto', banda_i] = df_IRL.at['ALAC', banda_i] - df_IRL.at['REQ_TERCEROS', banda_i] - df_IRL.at['REQ_PP', banda_i]
            
            # IRL Relativo
            df_IRL.at['IRL_relativo', banda_i] = df_IRL.at['ALAC', banda_i] /(df_IRL.at['REQ_TERCEROS', banda_i] + df_IRL.at['REQ_PP', banda_i])

            df_IRL_dicc[escenario] = df_IRL

    df_IRL_dicc['Moderado']
    df_IRL_dicc['Severo']

    #---------------------------------------------------------
    # Crear Tabla para GCP y looker

    # Combinar la información de los cuatro escenarios en un solo df
    IRL_combined = pd.concat([df.T.reset_index().assign(source = key) for key, df in df_IRL_dicc.items()],
                            ignore_index=True)

    # Renombrar la columna de valores relevantes
    IRL_combined.rename(columns={'index':'BANDA'}, inplace=True)
    IRL_combined.rename(columns={'source':'ESCENARIO'}, inplace=True)

    # Meltear con base a banda para un único df de una sola columna también para todas las bandas.
    #df_IRL_long = df_combined.melt(id_vars=['VALOR','ESCENARIO'], var_name = 'BANDA', value_name = 'VALORNUM')
    IRL_combined['FECHA'] = fecha_corte

    #---------------------------------------------------------
    # Revisar tabla antes de cargar

    IRL_combined
    # Querie para extraer la última fecha de IRL
    project_id = 'gestion-financiera-334002'
    dataset_id = 'DataStudio_GRF_Panama'
    table_id = 'Metricas_IRL_H_Pan'
    table_ref = f"{project_id}.{dataset_id}.{table_id}"


    query = f"""
        SELECT*
        FROM {table_ref}
        WHERE FECHA = (SELECT MAX(FECHA) FROM {table_ref})
            """
    IRL_ayer = client.query(query).to_dataframe() # Ultima fecha cargada
    # Ordenar IRL_ayer para que haga match con hoy
    IRL_ayer = IRL_ayer.set_index(['ESCENARIO','BANDA'])
    IRL_ayer = IRL_ayer.loc[IRL_combined.set_index(['ESCENARIO','BANDA']).index].reset_index()

    IRL_combined['VARIACIONP_IRL'] = (IRL_combined['IRL_absoluto']/IRL_ayer['IRL_absoluto']) - 1
    #IRL_combined['VARIACIONP_IRL'] = 0

    # IRL a cargar
    IRL_combined.head(3)

    # IRL de t-1.
    IRL_ayer.head(3)

    # El schema define cada uno de los formatos de las columnas que se carga. Operaciones
    schema_metr_IRL = [
        bigquery.SchemaField("BANDA", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("ALAC", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("REQ_PP", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("REQ_TERCEROS", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("IRL_absoluto", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("IRL_relativo", "FLOAT64", mode="REQUIRED"),
        bigquery.SchemaField("ESCENARIO", "STRING", mode="REQUIRED"),
        bigquery.SchemaField("VARIACIONP_IRL", "FLOAT64", mode="NULLABLE"),
        bigquery.SchemaField("FECHA", "TIMESTAMP", mode="REQUIRED")
        ]

    # Formateo de la tabla antes de cargar
    IRL_combined['FECHA'] = pd.to_datetime(IRL_combined['FECHA'])

    # Se realiza la carga de información vía APPEND a GCP
    append_2_GCP(df = IRL_combined, project_id = 'gestion-financiera-334002', dataset_id = 'DataStudio_GRF_Panama',
                table_id = 'Metricas_IRL_H_Pan', schema = schema_metr_IRL, fecha_corte = fecha_corte, 
                fecha_corte_ayer = fecha_corte_ayer)

#---------------------------------------------------------
#
