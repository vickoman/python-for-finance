import wallstreet
import threading
import time

#Definir parametros
ticker = "AAPL"
stock = wallstreet.Stock(quote=ticker)

#Mostrar el precio en tiempo real
print(f"Precio de {stock.name}: {stock.price} en {stock.currency}")

# Obtener el cambio porcentual y el cambio en el precio que abrio el mercado
print(f"Cambio porcentual desde que abrio el mercado de {stock.name}: {stock.cp:.2f}%")
print(f"Cambio en el precio desde que abrio el mercado de {stock.name}: {stock.change:.2f} ")

# Caclular el precio de Cierre del dia anterior
precio_anterior = stock.price - stock.change
print(f"Precio de cierre de {stock.name} del dia de ayer fue: {precio_anterior:.2f}")

#Obtener y desplegar precios en segundo plano 
detenerse = False

def get_precio_en_tiempo_real(tickers: list, n_segundos: float):
    """
    Esta funcion obtiene y muestra los precios de los tickers en tiempo real
    """
    while True:
        print("**************************************************")
        for ticker in tickers:
            ticker_precio = wallstreet.Stock(quote=ticker)
            print(f"Precio en tiempo real de {ticker_precio.name}: {ticker_precio.price} en {ticker_precio.currency}")

        if detenerse:
            break
        time.sleep(n_segundos)

#Definir lista de tickers
tickers = ["AAPL", "MSFT", "GOOG", "AMZN", "TSLA"]
# Iniciar el hilo para obtener los precios en tiempo real
hilo = threading.Thread(target=get_precio_en_tiempo_real, args=(tickers, 5))
hilo.start()

# Descomentar la varibale de abajo para que el bucle traiga el precio cada 5 segundos
# detenerse = True

# Record
# - El modulo de wallstreet nos permite obtener datos en tiempo real para una variedad de activos financieros
# - El modulo de threading nos permite ejecutar de manera simultanea multiples hilos de ejecucion











