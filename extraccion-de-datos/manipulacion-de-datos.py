# Importaciones
import yfinance as yf
import numpy as np
import pytz

# Descargar datos de yahoo
df = yf.download(tickers="TSLA", period="1d", interval="1m", multi_level_index=False, ignore_tz="America/New_York")
print("Numbero de registros que tenemos descargados", df.shape[0])
print(df)

# Realizar un Resampleo a temporalidad de 2 minutos
temporalidad = "2T"

operaciones_dict = {
    "Open": "first",
    "High": "max",
    "Low": "min",
    "Close": "last",
    "Volume": "sum"
    }

df_2min = df.resample(temporalidad, closed="left").agg(operaciones_dict)
print("Numero de registros descargados", df_2min.shape[0])
print(df_2min)

# Comprobar los precios que traeria yf con 2 min
df_new = yf.download(tickers="TSLA", period="1d", interval="2m", multi_level_index=False, ignore_tz="America/New_York")
# Ajustar en el mismo orden de columas
df_new = df_new[["Open", "High", "Low", "Close", "Volume"]]

# Validar que los datos son iguales los del resampleo vs los nuevos descargados
if np.mean(df_2min.loc[df_new.index] == df_new) == 1:
    print("Los datos son Identicos")
    

# Ampliando el tiempo de descarga de los datos
df = yf.download(tickers="TSLA", period="3d", interval="1m", multi_level_index=False, ignore_tz="America/New_York")
print("Numero de registros descargados", df.shape[0])
print(df)

# Realizar resampleo
temporalidad = "5T"
df_5min = df.resample(temporalidad).agg(operaciones_dict)
print("Numero de registros descargados", df_5min.shape[0])
print(df_5min)

# Comprobar precios

df_new = yf.download(tickers="TSLA", period="3d", interval="5m", multi_level_index=False, ignore_tz="America/New_York")

#Ajustar orden de columnas
df_new = df_new[["Open", "High", "Low", "Close", "Volume"]]

# Validar la longuitudde nuestros dataframes
if df_new.shape[0] != df_5min.shape[0]:
    print("La extension de ambos dataframes es distinta")
    

# Obteniendo los registros con valores Nans
df_nans = df_5min.loc[df_5min.isna().any(axis=1)]
print(df_nans)

# Eliminar los datos con los valores de Nan despues de realizar el resampleo
temporalidad = "5T"
df_5min = df.resample(temporalidad).agg(operaciones_dict).dropna(axis=0)
print("Numero de registros descargados", df_5min.shape[0])
print(df_5min)

# ahora si validamos datos
if np.mean(df_5min.loc[df_new.index] == df_new) == 1:
    print("Los datos han sido cambiados exitosamente")
    
    
    
# Resamplear con datos descargados de 5 min y lo convertiremos a 1 hora
temporalidad = "1H"
df_1h = df_5min.resample(temporalidad, origin="start").agg(operaciones_dict).dropna(axis=0)

# Descargar datos intervalos de 1h
df = yf.download(tickers="TSLA", period="3d", interval="1h", multi_level_index=False, ignore_tz="America/New_York")
df = df[["Open", "High", "Low", "Close", "Volume"]]

# Validar que nuestros datos de 1 hora resampleados sin iguales a los de 1 hora descargados
if np.mean(df_1h == df) == 1:
    print("Los datos han sido cambiados exitosamente")

# Explorar las diferentes zonas horarios 
print("Diferentes zonas horarios", pytz.all_timezones)

# Localizar una zona horario pero aplicada a nuestros datos
df.index = df.index.tz_localize("America/New_York")
print("Zona horarios", df.index.tz)
print(df)

# Cambiar a nuestra zona horraio
df.index = df.index.tz_convert("America/Mexico_City")
print("Zona horarios", df.index.tz)
print(df)

# Cambiar a Guayaquil
df.index = df.index.tz_convert("America/Guayaquil")
print("Zona horarios", df.index.tz)
print(df)

# Recordatorio
# - Los datos pueden ser resampleados y agregaods para cambiar su frencuencia temporal, facilitando el analisis temporales. El
#   Resampleo ajusta la granularidad de los daots, mientras que la agregacion permite resumirlos en funciones como promedio
#   suma, maximo o minimo, proporcionando una vision mas clara de tendencias o patrones