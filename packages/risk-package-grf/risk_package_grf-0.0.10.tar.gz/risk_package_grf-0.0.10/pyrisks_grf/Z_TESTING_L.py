# Esto se ejecuta en el local
from .A_ESTRUCTURA import cargador_estructura,obtencion_tabla_maestra,obtener_registro_actual
from .ML_01_VaR import global_treatment_VaR_Pan
from .ML_02_PLANO import global_treatment_Plano_Pan
from .ML_03_OPERACIONES_H_PAN import global_treatment_Operaciones_H_Pan
from .ML_04_OPERACIONES_BLOTTER import global_treatment_Operaciones_Blotter_Pan


Checker = obtencion_tabla_maestra() # Se obtiene el registro con fecha más nueva en la tabla maestra.
Checker = obtener_registro_actual(Checker=Checker) # Se utiliza el mismo registro si es el de la fecha actual o se reinicia     
#Checker = obtener_registro_actual(Checker=Checker,fecha='2025-04-11') # Se utiliza el mismo registro si es el de la fecha actual o se reinicia     

# Se ejecuta el VaR
global_treatment_VaR_Pan()
# Actualiza la tabla maestra
Checker['VaR_H_Pan'] = True

# Se ejecuta el plano. 
global_treatment_Plano_Pan()
# Actualiza la tabla maestra
Checker['Liquidez_H_Pan'] = True
Checker['Portafolio_H_Pan'] = True

# Se ejecuta la hoja de Operaciones de Pershing
global_treatment_Operaciones_H_Pan()
# Actualiza la tabla maestra
Checker['Operaciones_H_Pan'] = True

# Se ejecutan las Hojas de Operaciones Blotter
global_treatment_Operaciones_Blotter_Pan()
# Actualiza la tabla maestra
Checker['Operac_Cerradas_H_Blotter'] = True
Checker['Operac_Abiertas_H_Blotter'] = True

matriz = Checker.to_frame().T # Se pasa el pd.Series a un dataframe que puede ser concatenado a la tabla maestra
cargador_estructura(matriz=matriz) # Se concatena el registro a la tabla maestra