# importaciones
from alpha_vantage.timeseries import TimeSeries # pip install alpha-vantage
import json
import dash
from dash import dcc, html
import plotly.graph_objects as go
import webbrowser
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# API KEY desde variable de entorno
API_KEY_ALPHA = os.getenv("API_KEY_ALPHA")

# Verificar que la API key esté configurada
if not API_KEY_ALPHA:
    raise ValueError("API_KEY_ALPHA no está configurada en las variables de entorno")

# Crear un objeto de timeseries
ts = TimeSeries(key=API_KEY_ALPHA, output_format="pandas")

# Obtener datos de una accion especifica
datos, metadata = ts.get_daily(symbol="AAPL", outputsize="compact")

#Mostrar REsultados
print("Metadata:\n\n", json.dumps(metadata, indent=4))
print("Datos Descargados:\n\n", datos)

# Descargar todos los datos que se encuentren disponible con esta API
datos, metadata = ts.get_daily(symbol="AAPL", outputsize="full")

#Mostrar REsultados
print("Metadata:\n\n", json.dumps(metadata, indent=4))
print("Datos Descargados:\n\n", datos)

# Descargar datos Intradia
datos, metadata = ts.get_intraday(symbol="TSLA", interval="1min", outputsize="compact")

# Los intervalos disponibles para esta api
# son "1min", "5min", "30min", "60min"
print("Metadata:\n\n", json.dumps(metadata, indent=4))
print("Datos Descargados:\n\n", datos)

# Datos intradia pero para un mes en particular
datos, metadata = ts.get_intraday(symbol="TSLA", interval="1min", outputsize="full", extended_hours=True, month="2020-01")
print("Metadata:\n\n", json.dumps(metadata, indent=4))
print("Datos Descargados:\n\n", datos)

# Datos en Ventanas temporales mas Amplias
datos, metadata = ts.get_monthly(symbol="AAPL")
print("Metadata:\n\n", json.dumps(metadata, indent=4))
print("Datos Descargados:\n\n", datos)

# Generar una Visualizacion avanzada
datos = datos.rename(columns={
    "1. open": "Open",
    "2. high": "High",
    "3. low": "Low",
    "4. close": "Close",
    "5. volume": "Volume"
    })

datos = datos[::-1]

# Crear la aplicacion de Dash
app = dash.Dash(__name__)

# Definir el disenio de la aplicacion
app.layout = html.Div([
    html.H1("Grafico de Velas de AAPL", style={"textAlign": "center"}),
    dcc.Graph(id="grafico-velas",
              figure={
                  "data": [
                      go.Candlestick(
                          x=datos.index,
                          open=datos["Open"],
                          high=datos["High"],
                          low=datos["Low"],
                          close=datos["Close"],
                          name="AAPL"
                      )
                   ],
                  "layout": go.Layout(
                          title="Grafico de Velas",
                          xaxis={"title": "Fecha"},
                          yaxis={"title": "Precio ($)"},
                          template="plotly_dark"
                      )
              })
    ])

# ejecutar el servidor
host = "127.0.0.1"
port = "8050"
app.run(debug=True, host=host, port=port)
url_completa = "http://" + host + ":" + port + "/"
webbrowser.open(url_completa)

# Recordatorio
# - Alpha Vantage es una plataforma datos financieros gratuitos y tambien tiene sy plan de pagos
#  Su plan gratuito tiene 25 peticiones por dia
# - Dash es un framework util para crear aplicaciones web interactivas en python, especialmente especializaco en observacion de datos


















