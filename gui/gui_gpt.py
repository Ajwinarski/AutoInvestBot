import sys
import csv
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QSizePolicy
from PyQt5.QtCore import Qt
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtWebEngineCore import QWebEngineSettings


class StockChartWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Stock Chart")
        self.setGeometry(200, 200, 800, 600)

        self.chart_view = QWebEngineView(self)
        self.chart_view.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
        # self.chart_view.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.setCentralWidget(self.chart_view)

        self.load_chart_data()

    def load_chart_data(self):
        # Read stock data from CSV
        data = []
        with open('db/S&P500-Info.csv', 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                date = datetime.strptime(row[0], '%Y-%m-%d')
                open_price = float(row[1])
                high = float(row[2])
                low = float(row[3])
                close = float(row[4])
                data.append([date, open_price, high, low, close])

        # Prepare candlestick chart data
        dates = [row[0] for row in data]
        opens = [row[1] for row in data]
        highs = [row[2] for row in data]
        lows = [row[3] for row in data]
        closes = [row[4] for row in data]

        # Create a candlestick chart using Plotly
        fig = make_subplots(rows=1, cols=1)
        fig.add_trace(go.Candlestick(x=dates, open=opens,
                      high=highs, low=lows, close=closes), row=1, col=1)

        fig.update_layout(
            title="Stock Candlestick Chart",
            xaxis_title="Date",
            yaxis_title="Price",
            template="plotly_white"
        )

        # Convert the chart to HTML
        chart_html = fig.to_html(full_html=False)

        # Load the chart HTML into the web view
        self.chart_view.setHtml(chart_html)

    def keyPressEvent(self, event):
        # Handle key press events (e.g., Ctrl+Q)
        if event.key() == Qt.Key_Q and event.modifiers() == Qt.ControlModifier:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StockChartWindow()
    window.show()
    sys.exit(app.exec_())
