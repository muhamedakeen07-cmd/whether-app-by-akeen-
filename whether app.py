import sys 
import requests 
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit)



from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name:", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel("70°F", self)
        self.emoji_label = QLabel("☀️", self)
        self.description_label = QLabel("", self)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.addWidget(self.city_label)
        layout.addWidget(self.city_input)
        layout.addWidget(self.get_weather_button)
        layout.addWidget(self.temperature_label)
        layout.addWidget(self.emoji_label)
        layout.addWidget(self.description_label)
        self.setLayout(layout)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.setStyleSheet("""QLabel, QPushButton{
        font-family: calibri;
        }
        QLabel#city_label{font-size: 20px; font-weight: bold;}
        QLabel#temperature_label{font-size: 30px; font-weight: bold;
        font-style: italic; color: #333333;}

        QLineEdit#city_input{font-size: 20px; font-weight: bold; color: black; background-color: white; border: 2px solid gray; border-radius: 5px; padding: 5px;}

        QPushButton#get_weather_button{font-size: 20px; font-weight: bold; color: white;
          background-color: #007BFF; border: none; border-radius: 5px; padding: 10px;}

        QLabel#emoji_label{font-size: 50px; font-weight: bold;}
        QLabel#description_label{font-size: 20px; font-weight: bold; color: gray; font-style: italic;}
        """)
        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        api_key = "b9a772d9c0766a76098b277a237eb032"
        city = self.city_input.text().strip()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
            else:
                self.display_error(f"Error\n{data.get('message', 'Unknown error')}")
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 400:
                    self.display_error("Unauthorized\nInvalid API key")
                case 401:
                    self.display_error("Unauthorized\nInvalid API key")
                case 403:
                    self.display_error("Forbidden\nAccess is denied")
                case 404:
                    self.display_error("Not found\nCity not found")
                case 500:
                    self.display_error("Internal server error\nPlease try again later")
                case 502:
                    self.display_error("Bad gateway\nInvalid response from the server")
                case 503:
                    self.display_error("Service unavailable\nServer is down")
                case 504:
                    self.display_error("Gateway timeout\nNo response from the server")
                case _:
                    self.display_error(f"HTTP error occurred\n{http_error}")
        except requests.exceptions.ConnectionError:
            self.display_error("Connection error\nCheck your internet connection")
        except requests.exceptions.Timeout:
            self.display_error("Timeout error\nThe request timed out.")
        except requests.exceptions.TooManyRedirects:
            self.display_error("Too many redirects\nCheck the URL")
        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request error:\n{req_error}")

    def display_error(self, message):
        self.temperature_label.setText(message)
        self.emoji_label.setText("")
        self.description_label.setText("")

    def display_weather(self, data):
        temperature_c = data["main"]["temp"]
        weather_id = data["weather"][0]["id"]
        weather_description = data["weather"][0]["description"]

        self.temperature_label.setText(f"{temperature_c:.0f}°C")
        self.emoji_label.setText(self.get_wheather_emoji(weather_id))
        self.description_label.setText(weather_description)

    @staticmethod
    def get_wheather_emoji(wheather_id):
        if 200 <= wheather_id <= 232:
            return "⛈️"
        elif 300 <= wheather_id <= 321:
            return "🌦️"
        elif 500 <= wheather_id <= 531:
            return "🌧️"
        elif 600 <= wheather_id <= 622:
            return "❄️"
        elif 701 <= wheather_id <= 781:
            return "🌫️"
        elif wheather_id == 800:
            return "☀️"
        elif 801 <= wheather_id <= 802:
            return "⛅"
        elif 803 <= wheather_id <= 804:
            return "☁️"
        else:
            return "❓"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())


