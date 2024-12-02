from telegram import BotCommand,KeyboardButton,ReplyKeyboardMarkup
from telegram.ext import Updater,MessageHandler,Filters,CommandHandler

def start_message(update, context):
    buttons = [[KeyboardButton(text="Current weather",request_location=True)]]
    update.message.reply_text(text="Hello my friend, welcome to <b>Husniyor</b>'s weather-bot",parse_mode="HTML",reply_markup=ReplyKeyboardMarkup(buttons,True,True))

def weather(lon,lat):
    import requests

    url = "https://weatherapi-com.p.rapidapi.com/current.json"

    querystring = {"q": f"{lat},{lon}"}

    headers = {
        "x-rapidapi-key": "your rapid api key",
        "x-rapidapi-host": "weatherapi-com.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    print(response.json())
    return response.json()

def location_handler(update,context):
    location = update.message.location
    longitude = location.longitude
    latitude = location.latitude
    update.message.reply_text(f"Your longitude: {longitude}, your latitude: {latitude}.<i> Checking the current weather</i>...",parse_mode="HTML")
    data = weather(lon=longitude,lat=latitude)['current']
    datac = data["temp_c"]
    datad = data["condition"]['text']
    datai = data['condition']['icon']
    update.message.reply_photo(photo=f"https:{datai}",caption=f"<b>Current temp</b>: {datac} C`\n<b>Day is</b>: {datad}",parse_mode="HTML")

updater = Updater(token="your telegram bot token")
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler(command="start",callback=start_message))
dispatcher.add_handler(MessageHandler(Filters.location,location_handler))
updater.start_polling()
updater.idle()
