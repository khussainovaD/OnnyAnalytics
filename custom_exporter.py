"""
Custom Exporter для Open-Meteo API (Погода в Астане)
Собирает 10+ метрик и обновляется каждые 20 секунд.
"""

from prometheus_client import start_http_server, Gauge, Info
import requests
import time
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Определяем метрики Prometheus (10+ метрик) ---
# Мы используем 'city' и 'country' как лейблы

weather_temperature = Gauge(
    'weather_temperature_celsius', 'Current temperature', ['city', 'country']
)
weather_apparent_temperature = Gauge(
    'weather_apparent_temperature_celsius', 'Feels like temperature', ['city', 'country']
)
weather_humidity = Gauge(
    'weather_humidity_percent', 'Current humidity', ['city', 'country']
)
weather_windspeed = Gauge(
    'weather_windspeed_kmh', 'Current wind speed', ['city', 'country']
)
weather_wind_direction = Gauge(
    'weather_wind_direction_degrees', 'Current wind direction', ['city', 'country']
)
weather_pressure_msl = Gauge(
    'weather_pressure_msl_hpa', 'Mean sea level pressure', ['city', 'country']
)
weather_cloudcover = Gauge(
    'weather_cloudcover_percent', 'Cloud cover', ['city', 'country']
)
weather_precipitation = Gauge(
    'weather_precipitation_mm', 'Precipitation amount (rain, showers)', ['city', 'country']
)
weather_surface_pressure = Gauge(
    'weather_surface_pressure_hpa', 'Surface pressure', ['city', 'country']
)
weather_is_day = Gauge(
    'weather_is_day', 'Is day (1) or night (0)', ['city', 'country']
)

# Статус API
weather_api_status = Gauge(
    'weather_api_status', 'Weather API status (1=up, 0=down)'
)
weather_api_request_duration = Gauge(
    'weather_api_request_duration_seconds', 'Weather API request duration'
)

# Info
exporter_info = Info('custom_exporter', 'Info about the custom exporter')


def fetch_weather_data():
    """
    Получить данные с Open-Meteo API и обновить метрики.
    """
    logging.info("Fetching weather data...")
    start_time = time.time()
    
    # Координаты Астаны
    latitude = 51.1694
    longitude = 71.4491
    city = 'Astana'
    country = 'Kazakhstan'

    # URL и параметры для Open-Meteo. 
    # Мы запрашиваем 10+ текущих погодных метрик.
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'current': [
            'temperature_2m', 'apparent_temperature', 'relative_humidity_2m', 
            'precipitation', 'cloud_cover', 'pressure_msl', 'surface_pressure', 
            'wind_speed_10m', 'wind_direction_10m', 'is_day'
        ],
        'timezone': 'Asia/Almaty'
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status() # Вызовет ошибку, если код не 2xx
        
        data = response.json()
        current = data['current']

        # Обновляем все 10 метрик
        labels = {'city': city, 'country': country}
        
        weather_temperature.labels(**labels).set(current['temperature_2m'])
        weather_apparent_temperature.labels(**labels).set(current['apparent_temperature'])
        weather_humidity.labels(**labels).set(current['relative_humidity_2m'])
        weather_windspeed.labels(**labels).set(current['wind_speed_10m'])
        weather_wind_direction.labels(**labels).set(current['wind_direction_10m'])
        weather_pressure_msl.labels(**labels).set(current['pressure_msl'])
        weather_cloudcover.labels(**labels).set(current['cloud_cover'])
        weather_precipitation.labels(**labels).set(current['precipitation'])
        weather_surface_pressure.labels(**labels).set(current['surface_pressure'])
        weather_is_day.labels(**labels).set(current['is_day'])
        
        weather_api_status.set(1) # API в порядке
        logging.info("Successfully updated 10+ weather metrics.")

    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to fetch data: {e}")
        weather_api_status.set(0) # Ошибка сети или HTTP
        
    finally:
        # Записываем длительность запроса в любом случае
        duration = time.time() - start_time
        weather_api_request_duration.set(duration)
        logging.info(f"Request duration: {duration:.4f} seconds")


if __name__ == '__main__':
    exporter_info.info({
        'version': '2.0', # Версия 2.0
        'author': 'Student',
        'source': 'open-meteo.com'
    })
    
    start_http_server(8000)
    logging.info("Prometheus metrics server started on http://localhost:8000/metrics")
    
    while True:
        try:
            fetch_weather_data()
        except KeyboardInterrupt:
            logging.info("Exporter shutting down.")
            break
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
        
        # Обновлять каждые 20 секунд (согласно требованию)
        logging.info("Waiting 20 seconds for next update...")
        time.sleep(20)