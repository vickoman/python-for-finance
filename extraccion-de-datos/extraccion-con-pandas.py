#importtar librarias
import pandas_datareader as pdr
import datetime
import mplfinance as mpf
import matplotlib.pyplot as plt

# Definir el rango de fechas para los historicos
start_date = datetime.datetime(2020, 1, 1)
end_date = datetime.datetime(2025, 5, 31)

# Obtener datos historicos de acciones
print("--------------------------------")
print("Obteniendo datos historicos Fuentes: Stooq")
print("--------------------------------")

# stooq = pdr.get_data_stooq(symbols=["AMZN"], start=start_date, end=end_date)
# print("Datos \n\n", stooq)

# Extraer Datos. Fuente: stooq
stooq_df = pdr.stooq.StooqDailyReader(symbols=["AMZN"], start="2020-01-01", end="2025-05-01")
df = stooq_df.read()
df = df[::-1]
# print("Datos \n\n", df)

#  Eliminar el nivel de Columnas
df.columns = df.columns.droplevel(level=1)
# print("Datos con un solo nivel de columnas\n\n", df)

#Opciones dentro de Pandas Data Reader para descargar datos
# opciones = [ i for i in dir(pdr) if "get_data" in i]
# print("Opciones disponibles para descargar datos\n\n", opciones)
# for opcion in opciones:
#     print("Opcion: ", opcion)
# Opcion:  get_data_alphavantage
# Opcion:  get_data_enigma
# Opcion:  get_data_famafrench
# Opcion:  get_data_fred
# Opcion:  get_data_moex
# Opcion:  get_data_quandl
# Opcion:  get_data_stooq  # No Requiere API
# Opcion:  get_data_tiingo
# Opcion:  get_data_yahoo  # Requiere API (Usar Yahoo Finance)
# Opcion:  get_data_yahoo_actions

# Graficar Datos en formato de velas
mpf.plot(data=df, style="yahoo", type="candle", volume=True, title="Precios de Amazon", figsize=(22, 6), warn_too_much_data=df.shape[0], figscale=3.0, panel_ratios=(7, 3))
plt.show()

# Recordatorio
#   - Pandas Data Reader es una alternativa viable para obtener datos del mercado, sin embargo su tiempo de descarga
#     Puede tomar mas tiempo si se compara por ejemplo con Yahoo Finance.
