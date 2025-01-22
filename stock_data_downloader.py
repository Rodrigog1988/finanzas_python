import yfinance as yf

class StockDataDownloader:
    """
    Clase para descargar datos históricos de una acción y mostrar los primeros n registros.
    
    Parámetros:
    symbol (str): El símbolo de la acción (ej. "AAPL").
    start_date (str): Fecha de inicio para los datos (formato "YYYY-MM-DD").
    end_date (str): Fecha de fin para los datos (formato "YYYY-MM-DD").
    n (int): Número de registros a mostrar.
    """
    
    def __init__(self, symbol, start_date, end_date, n):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.n = n
        self.data = yf.download(self.symbol, start=self.start_date, end=self.end_date)
        self.show_head()

    def show_head(self):
        if self.data is not None:
            print(self.data.head(self.n))
        else:
            print("No se han descargado datos.")