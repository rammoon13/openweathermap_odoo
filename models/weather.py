# openweathermap_odoo/models/weather.py
from odoo import models, fields
from odoo.exceptions import UserError
import requests
import logging

_logger = logging.getLogger(__name__)

class WeatherInfo(models.Model):
    _name = 'weather.info'
    _description = 'Weather Information'

    _rec_name = 'city'

    city = fields.Char(string='City', required=True)
    api_key = fields.Char(string='API Key', required=True)
    temperature = fields.Float(string='Temperature', readonly=True)
    description = fields.Char(string='Description', readonly=True)

    def get_weather_data(self):
        api_url = f"http://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={self.api_key}&units=metric&lang=es"
        
        try:
            response = requests.get(api_url)
            if response.status_code == 200:
                data = response.json()
                self.temperature = data['main']['temp']
                self.description = data['weather'][0]['description']
            else:
                raise UserError(f"Error al obtener los datos del clima. Código: {response.status_code}")
        except requests.exceptions.RequestException as e:
            _logger.error("Error al conectar con la API: %s", str(e))
            raise UserError(f"Error al conectarse a OpenWeatherMap: {str(e)}")
