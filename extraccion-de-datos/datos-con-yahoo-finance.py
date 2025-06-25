import yfinance as yf
import pandas as pd
import time
import matplotlib.pyplot as plt

# Definir parametros
ticker = "AMZN"
fecha_inicio = "2023-01-01"
fecha_final = "2025-01-01"
intervalo = "1d"

# Descargar datos historicos con rango de fechas y un intervalo de velas diarias
df = yf.download(ticker, start=fecha_inicio, end=fecha_final, interval=intervalo)

# Ejemplo 2: descargar datos para el ultimo mes con intervalo de 15 min
df = yf.download(tickers=ticker, period="1mo", interval="15m")
print(df)

# Ejemplo 3: Descargar datos e los ultimos 2 dias con pre y post mercado en intervalo de 1 min
df = yf.download(tickers=ticker, period="2d", interval="1m", prepost=True, progress=False)
print("Cantidad de datos descargados: ", df.shape[0])

# Separar los datos del horario regular y del horario extendido

# Convertir el indice  del dataframe de la zona horario en Horario de Nueva York
print("Timezone actual: ", df.index.tz)

if df.index.tz is None:
    df.index = pd.to_datetime(df.index).tz_localize("UTC").tz_convert("America/New_York")
else:
    df.index = df.index.tz_convert("America/New_York")
    
# Definir horario del pre market, eeuu session and post market
horario_pre_market_inicio = "04:00:00"
horario_pre_market_final = "09:30:00"
horario_normal_inicio = "09:30:00"
horario_normal_fin = "16:00:00"
horario_post_market_inicio = "16:00:00"
horario_post_market_final = "20:00:00"

# Separar los datos por fechas
datos_pre_mercado = df.between_time(start_time=horario_pre_market_inicio, end_time=horario_pre_market_final).iloc[:-1]
datos_session_americana = df.between_time(start_time=horario_normal_inicio, end_time=horario_normal_fin)
datos_post_mercado = df.between_time(start_time=horario_post_market_inicio, end_time=horario_post_market_final).iloc[1:]

    
# Mostrar los datos
print("Datos del Pre market")
print(datos_pre_mercado)

print("Datos de la session Americana")
print(datos_session_americana)

print("Datos post market")
print(datos_post_mercado)

# Ejemplo 4: Descarga de datos (Concurrrent) de multiple activos
tickers = ["AMZN", "AAPL", "MSFT", "META", "TSLA", "QCOM", "XYZ", "NVDA", "PYPL"]

tiempo_inicio = time.time()
df_activos = yf.download(tickers=tickers, start=fecha_inicio, end=fecha_final, interval=intervalo, threads=True)
tiempo_final = time.time()
print("La descarga tomo {}".format(tiempo_final -  tiempo_inicio))