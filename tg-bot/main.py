from file_work import read_json, write_json
from functions import add_user
import telebot

SETTINGS_JSON = read_json("bot-settings.json")
TOKEN = SETTINGS_JSON["TOKEN"]
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def main(message):
    bot.send_message(message.chat.id, "Привет")
    print(message.from_user.id)
    add_user(message.from_user.id, SETTINGS_JSON["user_db"])


if __name__ == "__main__":
    bot.polling(non_stop=True)