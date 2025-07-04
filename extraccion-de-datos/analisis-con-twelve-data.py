from twelvedata import TDClient
import pandas as pd
import json
import plotly.io as pio 
import threading
import time
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuracion inicial
api_key = os.getenv("API_KEY_TWELVE")

if not api_key:
    raise ValueError("API_KEY_TWELVE no está configurada en las variables de entorno")

td = TDClient(apikey=api_key)

# Imprimir Estado actual de la API
uso_api = td.api_usage().as_json()
print(json.dumps(uso_api, indent=4))

# Obtener todas las acciones disponibles
stocks_list = td.get_stocks_list().as_json()
stocks_df = pd.DataFrame(stocks_list)
print("Número total de acciones:", stocks_df.shape[0])

# Contar Acciones Disponibles por país
stocks_df_grouby = stocks_df[["country", "name"]].groupby(by=["country"]).count().sort_values(by=["name"], ascending=False)
print(stocks_df_grouby)

# Definir parámetros
simbolo = "AAPL"
intervalo = "1day" # Intervalos permitidos: 1min, 5min, 15min, 30min, 45min, 1h, 2h, 4h, 8h, 1day, 1week, 1month
inicio = "2024-01-01"
fin = "2025-01-01"

# Ejemplo 1: Realizar petición en intervalo de fechas
df = td.time_series(
    symbol=simbolo,
    interval=intervalo,
    start_date=inicio,
    end_date=fin,
    outputsize=None
    ).as_pandas()
print(df)

# Ejemplo 2: Realizar Petición con un número definido de datos a recuperar en intervalo intradía
df = td.time_series(
    symbol=simbolo,
    interval="1min",
    outputsize=100
    ).as_pandas()
print(df)

# Ejemplo 3: Realizar Petición con un número definido de datos a recuperar con una fecha final y zona horaria
df = td.time_series(
    
    symbol=simbolo,
    interval="1min",
    end_date="2024-12-31",
    outputsize=100,
    timezone="America/New_York"
    
    ).as_pandas()
print(df)

# Graficar Series Temporales
ts = td.time_series(
    symbol="MSFT",
    outputsize=252,
    interval="1day"
    )

# Graficar Dentro de Spyder
ts.as_pyplot_figure().show()

# Graficar en Navegador
pio.renderers.default = "browser"
ts.as_plotly_figure().show()

# Calcular Indicadores Técnicos
indicadores = ts.with_bbands().with_ema(time_period=7).with_rsi()
calculo_indicadores = indicadores.as_pandas()
print(calculo_indicadores.iloc[:, 5:])

# Graficar indicadores
indicadores.as_plotly_figure().show()

# OBtener precios en tiempo real

rl_data = td.price(symbol=["AMZN", "AAPL"])
print(rl_data.as_json())

# Definiendo funcion que realizara las peticines
def datos_tiempo_teal(tickers, n_datos):
    """
    Esta funcion solicita los datos en tiempo real para los tickers especificados
    """
    contador = 0
    while contador < n_datos:
        rl_data = td.price(symbol=tickers)
        datos = rl_data.as_json()
        print("datos:", datos)
        contador += 1
        time.sleep(5)
        
t = threading.Thread(target=datos_tiempo_teal, kwargs={"tickers": ["AMZN", "TSLA", "MSFT", "GOOGL"],
                                                       "n_datos": 1})
t.start()

# Recordatorios
#   - Twelve Data es una API poderosa para obtener datos financierso, pero tiene ciertas limitaciones en su plan gratuito,
#       Por ejemplo estamos limitados a 8 peticiones por minutos y 800 solicitudes por dia
    






