from database.db_work import DataBase
from file_work import read_json, write_json
import telebot

SETTINGS_JSON = read_json("settings.json")
TOKEN = SETTINGS_JSON["TOKEN"]
bot = telebot.TeleBot(TOKEN)

db = DataBase(SETTINGS_JSON["user_db"])
db.make_users_table(SETTINGS_JSON["user_db"])

@bot.message_handler(commands=["start"])
def main(message):
    bot.send_message(message.chat.id, "Привет")
    print(message.from_user.id)
    db.insert_new_user(message.from_user.id, SETTINGS_JSON["user_db"])


@bot.message_handler(commands=["get_conf"])
def get_conf(message):
    bot.send_message(message.chat.id, "Держи конфиг")
    with open("wg_zero.conf", "rb") as file:
        bot.send_document(message.chat.id, file)


if __name__ == "__main__":
    bot.polling(non_stop=True)
