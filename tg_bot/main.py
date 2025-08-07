from database.db_work import DataBase
from file_work import read_json
import telebot
from IPGenerator import IPGenerator
from client_scripts.client_scripts import make_keys, make_new_user_conf, add_new_peer_to_server_conf,make_restart_vpn

SETTINGS_JSON = read_json("settings.json")
TOKEN = SETTINGS_JSON["TOKEN"]
bot = telebot.TeleBot(TOKEN)

db = DataBase(SETTINGS_JSON["user_db"])
db.make_users_table(SETTINGS_JSON["user_db"])


ip_generator = IPGenerator()

@bot.message_handler(commands=["start"])
def main(message):
    bot.send_message(message.chat.id, "Привет")
    print(message.from_user.id)
    db.insert_new_user(message.from_user.id, SETTINGS_JSON["user_db"])


@bot.message_handler(commands=["get_conf"])
def get_conf(message):
    try:
        bot.send_message(message.chat.id, "Держи конфиг")
        with open(f"client_conf/{str(message.from_user.id)}wg.conf", "rb") as file:
            bot.send_document(message.chat.id, file)
    except Exception as exc:
        print(f"ERROR! in func get_conf: {exc}")
        bot.send_message(message.chat.id, '''Не нашел твой конфиг, сорян
        Ты его создавал?''')


@bot.message_handler(commands=["make_conf"])
def make_conf(message):
    try:
        user_id = message.from_user.id
        if not db.is_activ(SETTINGS_JSON["user_db"], user_id):
            bot.send_message(message.chat.id, "Подключаю к системе")
            bot.send_message(message.chat.id, "Создаю ключи")
            make_keys(user_id)
            bot.send_message(message.chat.id, "Добавляю информацию на сервер")
            new_user_ip = ip_generator.get_new_ip(db, SETTINGS_JSON["user_db"])
            add_new_peer_to_server_conf(user_id, new_user_ip)
            bot.send_message(message.chat.id, "Создаю ваш конфиг")
            make_new_user_conf(user_id, new_user_ip)
            db.add_used_ip(SETTINGS_JSON["user_db"], new_user_ip, user_id)
            with open(f"client_conf/{user_id}wg.conf", "rb") as file:
                    bot.send_document(message.chat.id, file)
            make_restart_vpn()
        else:
            get_conf(message)
    except Exception as exc:
        print(f"ERROR!Can not make config for user({user_id}): {exc}")


if __name__ == "__main__":
    bot.polling(non_stop=True)
