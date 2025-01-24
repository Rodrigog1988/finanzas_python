import yfinance as yf
import plotly.graph_objects as go
from datetime import datetime, timedelta

class SMA200Analysis:
    """
    Clase para analizar el ETF especificado usando la Media Móvil Simple (SMA) de 200 períodos
    y generar un gráfico interactivo con una recomendación de compra basada en el último cierre.
    """
    def __init__(self, ticker, days_back):
        """
        Inicializa la clase con el ticker del ETF y el rango de días hacia atrás.

        :param ticker: Símbolo del ETF (str).
        :param days_back: Número de días atrás desde hoy para el análisis (int).
        """
        self.ticker = ticker
        self.start_date = datetime.today() - timedelta(days=days_back)
        self.end_date = datetime.today()
        self.data = None
        self.advice_message = ""

    def fetch_data(self):
        """Descarga los datos históricos del ETF desde Yahoo Finance."""
        self.data = yf.download(self.ticker, start=self.start_date, end=self.end_date)

    def calculate_sma200(self):
        """Calcula la Media Móvil Simple (SMA) de 200 períodos."""
        self.data['SMA_200'] = self.data[('Close', self.ticker)].rolling(window=200).mean()

    def generate_advice(self):
        """
        Genera el mensaje de recomendación basado en la comparación del cierre más reciente
        con la SMA de 200 períodos.
        """
        last_close = self.data[('Close', self.ticker)].iloc[-1]
        last_sma_200 = self.data['SMA_200'].iloc[-1]
        last_date = self.data.index[-1].strftime('%Y-%m-%d')

        if last_close < last_sma_200:
            self.advice_message = f"Conviene comprar {self.ticker} - Cierre: {last_close:.2f}, SMA 200: {last_sma_200:.2f}, Fecha: {last_date}."
        else:
            self.advice_message = f"No conviene comprar {self.ticker} - Cierre: {last_close:.2f}, SMA 200: {last_sma_200:.2f}, Fecha: {last_date}."

    def plot_graph(self):
        """
        Genera un gráfico de velas con la SMA de 200 períodos y añade anotaciones con información
        relevante y el mensaje de recomendación.
        """
        last_close = self.data[('Close', self.ticker)].iloc[-1]
        last_sma_200 = self.data['SMA_200'].iloc[-1]
        last_date = self.data.index[-1].strftime('%Y-%m-%d')

        fig = go.Figure(data=[
            go.Candlestick(
                x=self.data.index,
                open=self.data[('Open', self.ticker)],
                high=self.data[('High', self.ticker)],
                low=self.data[('Low', self.ticker)],
                close=self.data[('Close', self.ticker)],
                name=self.ticker
            ),
            go.Scatter(
                x=self.data.index,
                y=self.data['SMA_200'],
                mode='lines',
                line=dict(color='orange', width=2),
                name='SMA 200'
            )
        ])

        fig.add_annotation(
            x=self.data.index[-1], y=last_close,
            text=f"Último Cierre: {last_close:.2f}<br>SMA 200: {last_sma_200:.2f}<br>Fecha: {last_date}",
            showarrow=True,
            arrowhead=2,
            ax=0,
            ay=-40,
            font=dict(size=12, color="black"),
            bgcolor="white",
            borderpad=4
        )

        fig.add_annotation(
            xref="paper", yref="paper",
            x=0.5, y=1.1,
            text=self.advice_message,
            showarrow=False,
            font=dict(size=14, color="black"),
            align="center",
            bgcolor="lightyellow",
            bordercolor="black",
            borderwidth=1,
            borderpad=5
        )

        fig.update_layout(
            title=f"{self.ticker} ETF - Gráfico de Velas con SMA 200 (Último Año)",
            xaxis_title="Fecha",
            yaxis_title="Precio (USD)",
            xaxis_rangeslider_visible=True
        )

        fig.show()
        fig.write_html("C:/Users/u632915/Desktop/output_sma200.html")

    def run_analysis(self):
        """
        Ejecuta todo el análisis: descarga de datos, cálculo de SMA 200, generación de recomendación y gráfico.
        """
        self.fetch_data()
        self.calculate_sma200()
        self.generate_advice()
        self.plot_graph()
