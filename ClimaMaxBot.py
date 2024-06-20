import telebot
import requests
import os

# Substitua pelos seus próprios tokens
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

cidade = False

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['clima'])
def clima(message):
    global cidade
    bot.reply_to(message, "Digite o nome da cidade: Exemplo: São Paulo,BR")
    cidade = True

@bot.message_handler(func=lambda message: cidade)
def cidade_v(message):
    global cidade
    params = {
        'APPID': WEATHER_API_KEY,
        'q': f"{message.text}",
        'units': 'metric'
    }
    
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        
        city_name = data['name']
        weather_desc = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        msg = (f'Cidade: {city_name}\n'
               f'Clima: {weather_desc}\n'
               f'Temperatura: {temperature}°C\n'
               f'Umidade: {humidity}%\n'
               f'Velocidade do Vento: {wind_speed} m/s')
        bot.reply_to(message, msg)
    else:
        bot.reply_to(message, "Não foi possível encontrar informações para essa cidade.")
    cidade = False

@bot.message_handler(commands=['me ajuda', 'olá', 'start', 'help'])
def bem_vindo(message):
    bot.reply_to(message, "Olá! Bem-vindo ao bot do ClimaMax. Digite /clima para ver o clima atual.")

if __name__ == '__main__':
    bot.polling()
