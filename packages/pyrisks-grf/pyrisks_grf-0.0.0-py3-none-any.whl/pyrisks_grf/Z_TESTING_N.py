# Esto irá a Cloud Run Function:
from .A_ESTRUCTURA import cargador_estructura,obtencion_tabla_maestra,obtener_registro_actual
from .MN_01_METRICAS import global_treatment_Metricas_H_Pan
from .MN_02_IRL import global_treatment_IRL_Pan
from .MN_03_INFOMERCADO import global_treatment_Infomercado_Pan

Checker = obtencion_tabla_maestra() # Se obtiene el registro con fecha más nueva en la tabla maestra.
Checker = obtener_registro_actual(Checker=Checker) # Se utiliza el mismo registro si es el de la fecha actual o se reinicia     

if (Checker['Liquidez_H_Pan']) & (Checker['Portafolio_H_Pan']) & (not Checker['Metricas_H_Pan']):
        #global_treatment_Metricas_H_Pan()
        global_treatment_Metricas_H_Pan(where_to_run='local')
        Checker['Metricas_H_Pan']=True
elif (Checker['Liquidez_H_Pan']) & (Checker['Portafolio_H_Pan']) & (Checker['Operaciones_H_Pan']) & (not Checker['Metricas_IRL_H_Pan']):
        global_treatment_IRL_Pan()
        Checker['Metricas_IRL_H_Pan']=True
elif (Checker['VaR_H_Pan']) & (Checker['Liquidez_H_Pan']) & (Checker['Portafolio_H_Pan']) & (Checker['Metricas_H_Pan']) & (not Checker['Consumos_Pan_PP']):
        global_treatment_Infomercado_Pan()
        Checker['Consumos_Pan_PP']=True

matriz = Checker.to_frame().T # Se pasa el pd.Series a un dataframe que puede ser concatenado a la tabla maestra
cargador_estructura(matriz=matriz) # Se concatena el registro a la tabla maestra


# NO CORRER LO DE ABAJO

#from datetime import datetime
#d = list(matriz['FECHA'])[0]
#d = datetime.strftime(d,"%Y-%m-%d")
#obtencion_tabla_maestra(fecha=d)

